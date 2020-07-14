# -*- coding: utf-8 -*-

from .context import EveFitParser


import unittest


class ParserTestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        self.maxDiff = None

        self.efp = EveFitParser()

    def test_section_iterator(self):
        lines = '''Damage Control II
1600mm Steel Plates II
Energized Adaptive Nano Membrane II
[Empty Low slot]
Drone Damage Amplifier II
Drone Damage Amplifier II

Faint Epsilon Scoped Warp Scrambler
[Empty Med slot]
Small F-RX Compact Capacitor Booster
10MN Afterburner II

Medium Infectious Scoped Energy Neutralizer
[Empty High slot]
[Empty High slot]
Medium Infectious Scoped Energy Neutralizer

Medium Trimark Armor Pump I
[Empty Rig slot]
Medium Explosive Armor Reinforcer I



Hobgoblin II x5
Hammerhead II x5
Ogre II x5

Navy Cap Booster 400 x20

Cenobite II x23
Dromi II x2

'''.splitlines()

        sections = self.efp._sectionsIter(lines)

        loSlots = next(sections)
        medSlots = next(sections)
        hiSlots = next(sections)
        rigSlots = next(sections)
        subsystemSlots = next(sections)
        serviceSlots = next(sections)
        droneBay = next(sections)
        cargoBay = next(sections)
        fighterBay = next(sections)

        assert len(loSlots) == 6
        assert len(medSlots) == 4
        assert len(hiSlots) == 4
        assert len(rigSlots) == 3
        assert len(subsystemSlots) == 0
        assert len(serviceSlots) == 0
        assert len(droneBay) == 3
        assert len(cargoBay) == 1
        assert len(fighterBay) == 2

    def test_line_parser(self):
        lines = '''Damage Control II
1600mm Steel Plates II
Energized Adaptive Nano Membrane II
[Empty Low slot]
Ogre II x5
Navy Cap Booster 400 x20
Capital Capacitor Booster II,Cap Booster 3200'''.splitlines()

        parsed = self.efp._parseLines(lines)

        assert len(parsed) == 7

        assert parsed[0] == dict(type='Damage Control II')
        assert parsed[1] == dict(type='1600mm Steel Plates II')
        assert parsed[2] == dict(type='Energized Adaptive Nano Membrane II')
        assert parsed[3] == dict(empty=True)
        assert parsed[4] == dict(type='Ogre II', count=5)
        assert parsed[5] == dict(type='Navy Cap Booster 400', count=20)
        assert parsed[6] == dict(type='Capital Capacitor Booster II', charge='Cap Booster 3200')

    def test_full_parser_ragnarok(self):
        lines = '''[Ragnarok, OKE STARS's Ragnarok]
Abyssal Gyrostabilizer
Abyssal Gyrostabilizer
Abyssal Gyrostabilizer
Republic Fleet Tracking Enhancer
Republic Fleet Tracking Enhancer
Syndicate Damage Control

10000MN Afterburner II
CONCORD Capital Shield Extender
CONCORD Capital Shield Extender
Pithum A-Type Multispectrum Shield Hardener
Pithum A-Type Multispectrum Shield Hardener
Pithum A-Type Multispectrum Shield Hardener
Capital Capacitor Booster II,Cap Booster 3200

'Gjallarhorn' Explosive Doomsday
Dread Guristas Cloaking Device
Hexa 2500mm Repeating Cannon II,EMP XL
Hexa 2500mm Repeating Cannon II,EMP XL
Hexa 2500mm Repeating Cannon II,EMP XL
Hexa 2500mm Repeating Cannon II,EMP XL
Hexa 2500mm Repeating Cannon II,EMP XL
Hexa 2500mm Repeating Cannon II,EMP XL

Capital Core Defense Field Extender II
Capital Core Defense Field Extender II
Capital Core Defense Field Extender II'''
        results = self.efp.parse_fit(lines)

        self.assertDictEqual(results, dict(
            name='OKE STARS\'s Ragnarok',
            type='Ragnarok',
            loSlots=[
                dict(
                    type='Abyssal Gyrostabilizer'
                ),
                dict(
                    type='Abyssal Gyrostabilizer'
                ),
                dict(
                    type='Abyssal Gyrostabilizer'
                ),
                dict(
                    type='Republic Fleet Tracking Enhancer'
                ),
                dict(
                    type='Republic Fleet Tracking Enhancer'
                ),
                dict(
                    type='Syndicate Damage Control'
                )
            ],
            medSlots=[
                dict(
                    type='10000MN Afterburner II'
                ),
                dict(
                    type='CONCORD Capital Shield Extender'
                ),
                dict(
                    type='CONCORD Capital Shield Extender'
                ),
                dict(
                    type='Pithum A-Type Multispectrum Shield Hardener'
                ),
                dict(
                    type='Pithum A-Type Multispectrum Shield Hardener'
                ),
                dict(
                    type='Pithum A-Type Multispectrum Shield Hardener'
                ),
                dict(
                    type='Capital Capacitor Booster II',
                    charge='Cap Booster 3200'
                )
            ],
            hiSlots=[
                dict(
                    type='\'Gjallarhorn\' Explosive Doomsday'
                ),
                dict(
                    type='Dread Guristas Cloaking Device'
                ),
                dict(
                    type='Hexa 2500mm Repeating Cannon II',
                    charge='EMP XL'
                ),
                dict(
                    type='Hexa 2500mm Repeating Cannon II',
                    charge='EMP XL'
                ),
                dict(
                    type='Hexa 2500mm Repeating Cannon II',
                    charge='EMP XL'
                ),
                dict(
                    type='Hexa 2500mm Repeating Cannon II',
                    charge='EMP XL'
                ),
                dict(
                    type='Hexa 2500mm Repeating Cannon II',
                    charge='EMP XL'
                ),
                dict(
                    type='Hexa 2500mm Repeating Cannon II',
                    charge='EMP XL'
                )
            ],
            rigSlots=[
                dict(
                    type='Capital Core Defense Field Extender II'
                ),
                dict(
                    type='Capital Core Defense Field Extender II'
                ),
                dict(
                    type='Capital Core Defense Field Extender II'
                )
            ],
            subsystemSlots=list(),
            serviceSlots=list(),
            droneBay=list(),
            cargoBay=list(),
            fighterBay=list()
        ))

    def test_full_parser_vni(self):
        lines = '''[Vexor Navy Issue, *Vexor Navy Issue PvP]
Damage Control II
1600mm Steel Plates II
Energized Adaptive Nano Membrane II
[Empty Low slot]
Drone Damage Amplifier II
Drone Damage Amplifier II

Faint Epsilon Scoped Warp Scrambler
[Empty Med slot]
Small F-RX Compact Capacitor Booster
10MN Afterburner II

Medium Infectious Scoped Energy Neutralizer
[Empty High slot]
[Empty High slot]
Medium Infectious Scoped Energy Neutralizer

Medium Trimark Armor Pump I
[Empty Rig slot]
Medium Explosive Armor Reinforcer I



Hobgoblin II x5
Hammerhead II x5
Ogre II x5

Navy Cap Booster 400 x20'''

        results = self.efp.parse_fit(lines)

        self.assertDictEqual(results, dict(
            type='Vexor Navy Issue',
            name='*Vexor Navy Issue PvP',
            loSlots=[
                dict(
                    type='Damage Control II'
                ),
                dict(
                    type='1600mm Steel Plates II'
                ),
                dict(
                    type='Energized Adaptive Nano Membrane II'
                ),
                dict(
                    empty=True
                ),
                dict(
                    type='Drone Damage Amplifier II'
                ),
                dict(
                    type='Drone Damage Amplifier II'
                )
            ],
            medSlots=[
                dict(
                    type='Faint Epsilon Scoped Warp Scrambler',
                ),
                dict(
                    empty=True
                ),
                dict(
                    type='Small F-RX Compact Capacitor Booster'
                ),
                dict(
                    type='10MN Afterburner II'
                )
            ],
            hiSlots=[
                dict(
                    type='Medium Infectious Scoped Energy Neutralizer'
                ),
                dict(
                    empty=True
                ),
                dict(
                    empty=True
                ),
                dict(
                    type='Medium Infectious Scoped Energy Neutralizer'
                )
            ],
            rigSlots=[
                dict(
                    type='Medium Trimark Armor Pump I'
                ),
                dict(
                    empty=True
                ),
                dict(
                    type='Medium Explosive Armor Reinforcer I'
                )
            ],
            subsystemSlots=list(),
            serviceSlots=list(),
            droneBay=[
                dict(
                    type='Hobgoblin II',
                    count=5
                ),
                dict(
                    type='Hammerhead II',
                    count=5
                ),
                dict(
                    type='Ogre II',
                    count=5
                )
            ],
            cargoBay=[
                dict(
                    type='Navy Cap Booster 400',
                    count=20
                )
            ],
            fighterBay=list()
        ))
    
    def test_full_parser_no_loslot(self):
        lines = '''[Test,Test Fit]

10MN Afterburner II

Medium Energy Neutralizer I

Medium Trimark Armor Pump I



Ogre II x3'''

        results = self.efp.parse_fit(lines)

        self.assertDictEqual(results, dict(
            name='Test Fit',
            type='Test',
            loSlots=list(),
            medSlots=[dict(type='10MN Afterburner II')],
            hiSlots=[dict(type='Medium Energy Neutralizer I')],
            rigSlots=[dict(type='Medium Trimark Armor Pump I')],
            subsystemSlots=list(),
            serviceSlots=list(),
            droneBay=[dict(type='Ogre II', count=3)],
            cargoBay=list(),
            fighterBay=list()
        ))

    def test_full_parser_no_slots(self):
        lines = '''[Test,Test Fit]






Ogre II x3'''

        results = self.efp.parse_fit(lines)

        self.assertDictEqual(results, dict(
            name='Test Fit',
            type='Test',
            loSlots=list(),
            medSlots=list(),
            hiSlots=list(),
            rigSlots=list(),
            subsystemSlots=list(),
            serviceSlots=list(),
            droneBay=[dict(type='Ogre II', count=3)],
            cargoBay=list(),
            fighterBay=list()
        ))

    def test_full_parser_structure(self):
        lines = '''[Raitaru, Fit Raitaru]
Standup Layered Armor Plating I

Standup Focused Warp Disruptor I

Standup Heavy Energy Neutralizer I
Standup Multirole Missile Launcher I

Standup M-Set Basic Medium Ship Manufacturing Material Efficiency II


Standup Invention Lab I
Standup Manufacturing Plant I



Dromi II x27'''

        results = self.efp.parse_fit(lines)

        self.assertDictEqual(results, dict(
            name='Fit Raitaru',
            type='Raitaru',
            loSlots=[dict(type='Standup Layered Armor Plating I')],
            medSlots=[dict(type='Standup Focused Warp Disruptor I')],
            hiSlots=[
                dict(type='Standup Heavy Energy Neutralizer I'),
                dict(type='Standup Multirole Missile Launcher I')
            ],
            rigSlots=[dict(type='Standup M-Set Basic Medium Ship Manufacturing Material Efficiency II')],
            subsystemSlots=list(),
            serviceSlots=[
                dict(type='Standup Invention Lab I'),
                dict(type='Standup Manufacturing Plant I')
            ],
            droneBay=list(),
            cargoBay=list(),
            fighterBay=[dict(type='Dromi II', count=27)]
        ))


if __name__ == '__main__':
    unittest.main()