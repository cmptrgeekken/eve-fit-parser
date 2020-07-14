# -*- coding: utf-8 -*-

import re

OFFLINE_SUFFIX = '/OFFLINE'
NAME_CHARS = '[^,/\[\]]'
STUB_PATTERN = '^\[.+?\]$'

class EveFitParser(object):
    def __init__(self):
        pass

    def parse_fit(self, input, summarize=False):
        shipNamePattern = '\[(?P<shipType>[\w\s]+),\s*(?P<fitName>.+)\]'

        lines = input.splitlines()

        lines = self._prepareInput(lines)

        fit = dict(
            name=None,
            type=None,
            loSlots=list(),
            medSlots=list(),
            hiSlots=list(),
            rigSlots=list(),
            subsystemSlots=list(),
            serviceSlots=list(),
            droneBay=list(),
            cargoBay=list(),
            fighterBay=list()
        )

        shipInfo = lines.pop(0)

        m = re.match(shipNamePattern, shipInfo)

        if not m:
            raise Exception('Invalid fit header.')

        fit['name'] = m.group('fitName').strip()
        fit['type'] = m.group('shipType').strip()

        sections = self._sectionsIter(lines)

        try:
            fit['loSlots'] = self._parseLines(next(sections))
            fit['medSlots'] = self._parseLines(next(sections))
            fit['hiSlots'] = self._parseLines(next(sections))
            fit['rigSlots'] = self._parseLines(next(sections))
            fit['subsystemSlots'] = self._parseLines(next(sections))
            fit['serviceSlots'] = self._parseLines(next(sections))
            fit['droneBay'] = self._parseLines(next(sections))
            fit['cargoBay'] = self._parseLines(next(sections))
            fit['fighterBay'] = self._parseLines(next(sections))

        except StopIteration:
            # If we reach this point, the fit is not an Eve-exported fit, but rather from another application
            # such as ZKB or Pyfa.
            self._fixThirdPartyExports(fit)
            pass

        return fit

    def _fixThirdPartyExports(self, fit):
        # ZKB exports serviceSlots in the same spot as subsystemSlots. 
        # We'll swap the two values if only `Standup` service modules are present 
        # in the `subsystemSlots` array. 
        if fit['subsystemSlots'] and not fit['serviceSlots']:
            swap = False
            if all(s['type'].startswith('Standup') or re.match(STUB_PATTERN, s['type']) for s in fit['subsystemSlots']):
                fit['serviceSlots'] = fit['subsystemSlots']
                fit['subsystemSlots'] = list()

    def _parseLines(self, lines):
        modulePattern = '^(?P<typeName>{0}+?)(,\s*(?P<chargeName>{0}+?))?(?P<offline>\s*{1})?(\s*\[(?P<mutation>\d+?)\])?$'.format(NAME_CHARS, OFFLINE_SUFFIX)
        droneCargoPattern = '^(?P<typeName>{}+?) x(?P<count>\d+?)$'.format(NAME_CHARS)

        parsedLines = list()

        for line in lines:
            if re.match(STUB_PATTERN, line):
                parsedLines.append(dict(empty=True))
                continue
            
            m = re.match(droneCargoPattern, line)
            if m:
                parsedLines.append(dict(
                    type=m.group('typeName').strip(),
                    count=int(m.group('count')),
                ))
                continue

            m = re.match(modulePattern, line)
            if m:
                entry = dict(type=m.group('typeName').strip())
                if m.group('chargeName'):
                    entry['charge'] = m.group('chargeName').strip()
                if m.group('offline'):
                    entry['offline'] = True
                if m.group('mutation'):
                    entry['mutation_id'] = int(m.group('mutation'))

                parsedLines.append(entry)
        return parsedLines


    def _sectionsIter(self, lines):
        sections = list()
        section = list()
        for line in lines:
            if not line:
                yield section
                section = list()
            else:
                section.append(line)

        if section:
            yield section

    # Removes extra whitespace and blank lines at beginning and end
    def _prepareInput(self, lines):
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
        while lines and not lines[0]:
            del lines[0]
        while lines and not lines[-1]:
            del lines[-1]
        return lines