Eve Fit Export Parser
========================

This module takes Eve Online exports (via `Copy to Clipboard`) and parses them into an iterable format with slot information. Per [Eve's documentation](https://www.eveonline.com/article/import-export-fittings) (and based off some additional experimenting), the Eve Fit export has the following structure:

1. Ship or Structure Type and Fit Name (sample: `[Ragnarok,KenGeorge's Ragnarok]`)
1. Low slot modules
1. Mid slot modules
1. High slot modules
1. Rigs
1. Subsystems
1. Service modules (e.g., Clone Bay)
1. Drones in drone bay with amount (i.e., Warrior II x2)
1. Items in cargo bay with amount(i.e., Antimatter Charge M x1)
1. Fighters in fighter bay with amount (i.e., Dromi II x27)

If a module group has no items defined, it has a single blank space. Additionally, the following keywords are used to identify when an empty slot is before a filled slot:

* [Empty Low slot]
* [Empty Med slot]
* [Empty High slot]
* [Empty Rig slot]

Sample input:

```txt
[Ragnarok, OKE STARS's Ragnarok]
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
Capital Core Defense Field Extender II
```

Sample output:

```py
dict(
    name='OKE STARS\'s Ragnarok',
    type='Ragnarok',
    loSlots=list(
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
    ),
    medSlots=list(
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
    ),
    hiSlots=list(
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
    ),
    rigSlots=list(
        dict(
            type='Capital Core Defense Field Extender II'
        ),
        dict(
            type='Capital Core Defense Field Extender II'
        ),
        dict(
            type='Capital Core Defense Field Extender II'
        )
    ),
    subsystemSlots=list(),
    serviceSlots=list(),
    droneBay=list(),
    cargoBay=list()
)
```

Sample Input:

```txt
[Vexor Navy Issue, *Vexor Navy Issue PvP]
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

Navy Cap Booster 400 x20

```

Sample Output:

```py
dict(
    type='Vexor Navy Issue',
    name='*Vexor Navy Issue PvP',
    loSlots=list(
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
    ),
    medSlots=list(
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
    ),
    hiSlots=list(
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
    ),
    rigSlots=list(
        dict(
            type='Medium Trimark Armor Pump I'
        ),
        dict(
            empty=True
        ),
        dict(
            type='Medium Explosive Armor Reinforcer I'
        )
    ),
    subsystemSlots=list(),
    serviceSlots=list(),
    droneBay=list(
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
    ),
    cargoBay=list(
        dict(
            type='Navy Cap Booster 400',
            count=20
        )
    )
)
```
