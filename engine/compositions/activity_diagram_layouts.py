from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ActivityLayout:
    width: int = 6000
    height: int = 8400
    title_y: int = 190
    action_width: int = 1800
    action_height: int = 310
    decision_width: int = 660
    decision_height: int = 440
    note_width: int = 1500
    note_height: int = 280


# A composition has the following maps:
# initial/final: semantic ID -> (centre x, centre y)
# actions/decisions/merges/notes: semantic ID -> (top-left x, top-left y)
# routes: relation ID -> {points: [(x, y), ...], label: (x, y)}
# Individual diagrams are registered only after their preceding diagram has passed QA.
AD01_LAYOUT = ActivityLayout(width=7800, height=8800, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD01 = {
    'initial': {'activity.ad01.initial': (3600, 550)},
    'actions': {
        'activity.ad01.a01': (2700, 750),
        'activity.ad01.a02': (2700, 1250),
        'activity.ad01.a03': (4800, 1830),
        'activity.ad01.a04': (2700, 2400),
        'activity.ad01.a05': (4800, 3000),
        'activity.ad01.a06': (2700, 3550),
        'activity.ad01.a07': (2700, 4050),
        'activity.ad01.a08': (4800, 4650),
        'activity.ad01.a09': (2700, 5200),
        'activity.ad01.a10': (2700, 5700),
        'activity.ad01.a11': (2700, 6200),
        'activity.ad01.a12': (2700, 6700),
    },
    'decisions': {
        'activity.ad01.d01': (3270, 1750),
        'activity.ad01.d02': (3270, 2900),
        'activity.ad01.d03': (3270, 4550),
    },
    'merges': {'activity.ad01.mend': (3395, 7450)},
    'notes': {'activity.ad01.note-idempotency': (650, 6205)},
    'final': {'activity.ad01.final': (3600, 8200)},
    'routes': {
        'relation.ad01.f01': {'points': [(3600, 588), (3600, 750)], 'label': (3600, 660)},
        'relation.ad01.f02': {'points': [(3600, 1060), (3600, 1250)], 'label': (3600, 1155)},
        'relation.ad01.f03': {'points': [(3600, 1560), (3600, 1750)], 'label': (3600, 1655)},
        'relation.ad01.f04': {'points': [(3930, 1970), (4800, 1985)], 'label': (4350, 1845)},
        'relation.ad01.f05': {'points': [(6600, 1985), (7350, 1985), (7350, 7586), (3804, 7586)], 'label': (7070, 4700)},
        'relation.ad01.f06': {'points': [(3600, 2190), (3600, 2400)], 'label': (4300, 2300)},
        'relation.ad01.f07': {'points': [(3600, 2710), (3600, 2900)], 'label': (3600, 2805)},
        'relation.ad01.f08': {'points': [(3930, 3120), (4800, 3155)], 'label': (4350, 3005)},
        'relation.ad01.f09': {'points': [(6600, 3155), (7150, 3155), (7150, 7500), (3804, 7586)], 'label': (6870, 5400)},
        'relation.ad01.f10': {'points': [(3600, 3340), (3600, 3550)], 'label': (4280, 3445)},
        'relation.ad01.f11': {'points': [(3600, 3860), (3600, 4050)], 'label': (3600, 3955)},
        'relation.ad01.f12': {'points': [(3600, 4360), (3600, 4550)], 'label': (3600, 4455)},
        'relation.ad01.f13': {'points': [(3930, 4770), (4800, 4805)], 'label': (4360, 4635)},
        'relation.ad01.f14': {'points': [(6600, 4805), (6850, 4805), (6850, 7420), (3804, 7586)], 'label': (6710, 6080)},
        'relation.ad01.f15': {'points': [(3600, 4990), (3600, 5200)], 'label': (4230, 5095)},
        'relation.ad01.f16': {'points': [(3600, 5510), (3600, 5700)], 'label': (3600, 5605)},
        'relation.ad01.f17': {'points': [(3600, 6010), (3600, 6200)], 'label': (3600, 6105)},
        'relation.ad01.f18': {'points': [(3600, 6510), (3600, 6700)], 'label': (3600, 6605)},
        'relation.ad01.f19': {'points': [(3600, 7010), (3600, 7450)], 'label': (3600, 7230)},
        'relation.ad01.f20': {'points': [(3600, 7723), (3600, 8146)], 'label': (3600, 7930)},
    },
}

AD02_LAYOUT = ActivityLayout(width=7800, height=8300, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD02 = {
    'initial': {'activity.ad02.initial': (3600, 550)},
    'actions': {
        'activity.ad02.a01': (2700, 800),
        'activity.ad02.a02': (2700, 1300),
        'activity.ad02.a03': (2700, 1800),
        'activity.ad02.a04': (4800, 2550),
        'activity.ad02.a05': (2700, 2900),
        'activity.ad02.a06': (2700, 3400),
        'activity.ad02.a07': (4800, 4150),
        'activity.ad02.a08': (2700, 4500),
        'activity.ad02.a09': (4800, 5250),
        'activity.ad02.a10': (2700, 5600),
        'activity.ad02.a11': (2700, 6100),
    },
    'decisions': {
        'activity.ad02.d01': (3270, 2350),
        'activity.ad02.d02': (3270, 3950),
        'activity.ad02.d03': (3270, 5050),
    },
    'merges': {'activity.ad02.mend': (3395, 6900)},
    'notes': {'activity.ad02.note-retry': (600, 6105)},
    'final': {'activity.ad02.final': (3600, 7750)},
    'routes': {
        'relation.ad02.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad02.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad02.f03': {'points': [(3600, 1610), (3600, 1800)], 'label': (3600, 1705)},
        'relation.ad02.f04': {'points': [(3600, 2110), (3600, 2350)], 'label': (3600, 2230)},
        'relation.ad02.f05': {'points': [(3930, 2570), (4800, 2705)], 'label': (4370, 2530)},
        'relation.ad02.f06': {'points': [(6600, 2705), (7350, 2705), (7350, 7036), (3804, 7036)], 'label': (7070, 4660)},
        'relation.ad02.f07': {'points': [(3600, 2790), (3600, 2900)], 'label': (4240, 2845)},
        'relation.ad02.f08': {'points': [(3600, 3210), (3600, 3400)], 'label': (3600, 3305)},
        'relation.ad02.f09': {'points': [(3600, 3710), (3600, 3950)], 'label': (3600, 3830)},
        'relation.ad02.f10': {'points': [(3930, 4170), (4800, 4305)], 'label': (4360, 4130)},
        'relation.ad02.f11': {'points': [(6600, 4305), (7150, 4305), (7150, 7036), (3804, 7036)], 'label': (6880, 5650)},
        'relation.ad02.f12': {'points': [(3600, 4390), (3600, 4500)], 'label': (4210, 4445)},
        'relation.ad02.f13': {'points': [(3600, 4810), (3600, 5050)], 'label': (3600, 4930)},
        'relation.ad02.f14': {'points': [(3930, 5270), (4800, 5405)], 'label': (4360, 5230)},
        'relation.ad02.f15': {'points': [(6600, 5405), (6950, 5405), (6950, 6900), (3804, 7036)], 'label': (6780, 6170)},
        'relation.ad02.f16': {'points': [(3600, 5490), (3600, 5600)], 'label': (4260, 5545)},
        'relation.ad02.f17': {'points': [(3600, 5910), (3600, 6100)], 'label': (3600, 6005)},
        'relation.ad02.f18': {'points': [(3600, 6410), (3600, 6900)], 'label': (3600, 6650)},
        'relation.ad02.f19': {'points': [(3600, 7173), (3600, 7696)], 'label': (3600, 7430)},
    },
}

AD03_LAYOUT = ActivityLayout(width=12000, height=9200, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD03 = {
    'initial': {'activity.ad03.initial': (3600, 550)},
    'actions': {
        'activity.ad03.a01': (2700, 800), 'activity.ad03.a00': (500, 1380),
        'activity.ad03.a02': (2700, 1900), 'activity.ad03.a03': (500, 2500),
        'activity.ad03.a04': (2700, 3000), 'activity.ad03.a05': (2700, 3500),
        'activity.ad03.a06': (2700, 4000), 'activity.ad03.a07': (500, 4600),
        'activity.ad03.a08': (1800, 5700), 'activity.ad03.a09': (1800, 6150),
        'activity.ad03.a10': (100, 6730), 'activity.ad03.a11': (1800, 7100),
        'activity.ad03.a12': (1800, 7550), 'activity.ad03.a13': (7200, 5700),
        'activity.ad03.a14': (9500, 6260), 'activity.ad03.a15': (7200, 6650),
        'activity.ad03.a16': (7200, 7100),
    },
    'decisions': {
        'activity.ad03.d00': (3270, 1300), 'activity.ad03.d01': (3270, 2400),
        'activity.ad03.d02': (3270, 4500), 'activity.ad03.d03': (3270, 5100),
        'activity.ad03.d04': (2370, 6600), 'activity.ad03.d05': (7770, 6150),
    },
    'merges': {'activity.ad03.mend': (5795, 8000)},
    'notes': {'activity.ad03.note-idempotency': (100, 7150)},
    'final': {'activity.ad03.final': (6000, 8750)},
    'routes': {
        'relation.ad03.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad03.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad03.f03': {'points': [(3270, 1520), (2300, 1535)], 'label': (2750, 1400)},
        'relation.ad03.f04': {'points': [(1400, 1690), (300, 1690), (300, 8136), (5795, 8136)], 'label': (300, 4900)},
        'relation.ad03.f05': {'points': [(3600, 1740), (3600, 1900)], 'label': (4240, 1820)},
        'relation.ad03.f06': {'points': [(3600, 2210), (3600, 2400)], 'label': (3600, 2305)},
        'relation.ad03.f07': {'points': [(3270, 2620), (2300, 2655)], 'label': (2750, 2505)},
        'relation.ad03.f08': {'points': [(1400, 2810), (500, 2810), (500, 8136), (5795, 8136)], 'label': (500, 5480)},
        'relation.ad03.f09': {'points': [(3600, 2840), (3600, 3000)], 'label': (4230, 2920)},
        'relation.ad03.f10': {'points': [(3600, 3310), (3600, 3500)], 'label': (3600, 3405)},
        'relation.ad03.f11': {'points': [(3600, 3810), (3600, 4000)], 'label': (3600, 3905)},
        'relation.ad03.f12': {'points': [(3600, 4310), (3600, 4500)], 'label': (3600, 4405)},
        'relation.ad03.f13': {'points': [(3270, 4720), (2300, 4755)], 'label': (2740, 4610)},
        'relation.ad03.f14': {'points': [(1400, 4910), (700, 4910), (700, 8136), (5795, 8136)], 'label': (700, 6250)},
        'relation.ad03.f15': {'points': [(3600, 4940), (3600, 5100)], 'label': (4250, 5020)},
        'relation.ad03.f16': {'points': [(3600, 5540), (2700, 5540), (2700, 5700)], 'label': (3040, 5480)},
        'relation.ad03.f17': {'points': [(2700, 6010), (2700, 6150)], 'label': (2700, 6080)},
        'relation.ad03.f18': {'points': [(2700, 6460), (2700, 6600)], 'label': (2700, 6530)},
        'relation.ad03.f19': {'points': [(2370, 6820), (1900, 6885)], 'label': (2130, 6720)},
        'relation.ad03.f20': {'points': [(1000, 7040), (400, 7040), (400, 8136), (5795, 8136)], 'label': (400, 7600)},
        'relation.ad03.f21': {'points': [(2700, 7040), (2700, 7100)], 'label': (3200, 7060)},
        'relation.ad03.f22': {'points': [(2700, 7410), (2700, 7550)], 'label': (2700, 7480)},
        'relation.ad03.f23': {'points': [(2700, 7860), (2700, 8136), (5795, 8136)], 'label': (4250, 8060)},
        'relation.ad03.f24': {'points': [(3930, 5320), (8100, 5320), (8100, 5700)], 'label': (6000, 5220)},
        'relation.ad03.f25': {'points': [(8100, 6010), (8100, 6150)], 'label': (8100, 6080)},
        'relation.ad03.f26': {'points': [(8430, 6370), (9500, 6415)], 'label': (8940, 6250)},
        'relation.ad03.f27': {'points': [(10400, 6570), (11000, 6570), (11000, 8136), (6204, 8136)], 'label': (11000, 7380)},
        'relation.ad03.f28': {'points': [(8100, 6590), (8100, 6650)], 'label': (8600, 6620)},
        'relation.ad03.f29': {'points': [(8100, 6960), (8100, 7100)], 'label': (8100, 7030)},
        'relation.ad03.f30': {'points': [(8100, 7410), (8100, 8136), (6204, 8136)], 'label': (7100, 8060)},
        'relation.ad03.f31': {'points': [(6000, 8273), (6000, 8696)], 'label': (6000, 8480)},
    },
}

AD04_LAYOUT = ActivityLayout(width=12000, height=9400, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD04 = {
    'initial': {'activity.ad04.initial': (3600, 550)},
    'actions': {
        'activity.ad04.a01': (2700, 800), 'activity.ad04.a02': (2700, 1300), 'activity.ad04.a03': (2700, 1800), 'activity.ad04.a04': (2700, 2300),
        'activity.ad04.a05': (5000, 3000), 'activity.ad04.a06': (500, 4000), 'activity.ad04.a07': (500, 4800),
        'activity.ad04.a08': (2700, 4000), 'activity.ad04.a09': (2700, 4500), 'activity.ad04.a10': (5000, 5600),
        'activity.ad04.a11': (5000, 6500), 'activity.ad04.a12': (7200, 7400), 'activity.ad04.a13': (9700, 7400),
        'activity.ad04.a14': (2700, 5600), 'activity.ad04.a15': (2700, 7000),
    },
    'decisions': {
        'activity.ad04.d01': (3270, 2850), 'activity.ad04.d02': (3270, 3450), 'activity.ad04.d03': (1070, 4400),
        'activity.ad04.d04': (3270, 5050), 'activity.ad04.d05': (5570, 6200), 'activity.ad04.d06': (7770, 6900),
    },
    'merges': {'activity.ad04.mend': (5795, 8200)},
    'notes': {'activity.ad04.note-idempotency': (500, 2200), 'activity.ad04.note-receipt': (8000, 3000)},
    'final': {'activity.ad04.final': (6000, 8950)},
    'routes': {
        'relation.ad04.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad04.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad04.f03': {'points': [(3600, 1610), (3600, 1800)], 'label': (3600, 1705)},
        'relation.ad04.f04': {'points': [(3600, 2110), (3600, 2300)], 'label': (3600, 2205)},
        'relation.ad04.f05': {'points': [(3600, 2610), (3600, 2850)], 'label': (3600, 2730)},
        'relation.ad04.f06': {'points': [(3930, 3070), (5000, 3155)], 'label': (4450, 3000)},
        'relation.ad04.f07': {'points': [(6800, 3155), (11300, 3155), (11300, 8336), (6204, 8336)], 'label': (11300, 5700)},
        'relation.ad04.f08': {'points': [(3600, 3290), (3600, 3450)], 'label': (4250, 3370)},
        'relation.ad04.f09': {'points': [(3270, 3670), (2300, 4155)], 'label': (2750, 3820)},
        'relation.ad04.f10': {'points': [(1400, 4310), (1400, 4400)], 'label': (1400, 4355)},
        'relation.ad04.f11': {'points': [(1400, 4840), (1400, 4800)], 'label': (2050, 4900)},
        'relation.ad04.f12': {'points': [(500, 4955), (250, 4955), (250, 1455), (2700, 1455)], 'label': (250, 3180)},
        'relation.ad04.f13': {'points': [(1730, 4620), (900, 4620), (900, 8336), (5795, 8336)], 'label': (900, 6500)},
        'relation.ad04.f14': {'points': [(3600, 3890), (3600, 4000)], 'label': (4250, 3945)},
        'relation.ad04.f15': {'points': [(3600, 4310), (3600, 4500)], 'label': (3600, 4405)},
        'relation.ad04.f16': {'points': [(3600, 4810), (3600, 5050)], 'label': (3600, 4930)},
        'relation.ad04.f17': {'points': [(3600, 5490), (3600, 5600)], 'label': (4250, 5545)},
        'relation.ad04.f18': {'points': [(3600, 5910), (3600, 7000)], 'label': (3600, 6450)},
        'relation.ad04.f19': {'points': [(3600, 7310), (3600, 8336), (5795, 8336)], 'label': (4700, 8200)},
        'relation.ad04.f20': {'points': [(3930, 5270), (5000, 5755)], 'label': (4450, 5400)},
        'relation.ad04.f21': {'points': [(5900, 5910), (5900, 6200)], 'label': (5900, 6055)},
        'relation.ad04.f22': {'points': [(5900, 6640), (5900, 6500)], 'label': (6550, 6700)},
        'relation.ad04.f23': {'points': [(5000, 6655), (4400, 6655), (4400, 7155), (4500, 7155)], 'label': (4450, 6900)},
        'relation.ad04.f24': {'points': [(6230, 6420), (8100, 6420), (8100, 6900)], 'label': (7100, 6320)},
        'relation.ad04.f25': {'points': [(8100, 7340), (8100, 7400)], 'label': (8650, 7370)},
        'relation.ad04.f26': {'points': [(8100, 7710), (8100, 8336), (6204, 8336)], 'label': (7200, 8200)},
        'relation.ad04.f27': {'points': [(8430, 7120), (9700, 7555)], 'label': (9000, 7000)},
        'relation.ad04.f28': {'points': [(10600, 7710), (11000, 7710), (11000, 8336), (6204, 8336)], 'label': (11000, 8000)},
        'relation.ad04.f29': {'points': [(6000, 8473), (6000, 8896)], 'label': (6000, 8680)},
    },
}

AD05_LAYOUT = ActivityLayout(width=11000, height=8800, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD05 = {
    'initial': {'activity.ad05.initial': (3600, 550)},
    'actions': {
        'activity.ad05.a01': (2700, 800), 'activity.ad05.a02': (2700, 1300), 'activity.ad05.a03': (5000, 2000),
        'activity.ad05.a04': (2700, 2400), 'activity.ad05.a05': (2700, 2900), 'activity.ad05.a06': (2700, 3400),
        'activity.ad05.a07': (500, 6600), 'activity.ad05.a08': (5000, 4200), 'activity.ad05.a09': (2700, 4500),
        'activity.ad05.a10': (2700, 5000), 'activity.ad05.a11': (2700, 5500), 'activity.ad05.a12': (5000, 6600),
    },
    'decisions': {'activity.ad05.d01': (3270, 1850), 'activity.ad05.d02': (3270, 3950), 'activity.ad05.d03': (3270, 6050)},
    'merges': {'activity.ad05.mend': (4895, 7600)},
    'final': {'activity.ad05.final': (5100, 8350)},
    'routes': {
        'relation.ad05.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad05.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad05.f03': {'points': [(3600, 1610), (3600, 1850)], 'label': (3600, 1730)},
        'relation.ad05.f04': {'points': [(3930, 2070), (5000, 2155)], 'label': (4450, 2000)},
        'relation.ad05.f05': {'points': [(6800, 2155), (9800, 2155), (9800, 7736), (5304, 7736)], 'label': (9800, 5000)},
        'relation.ad05.f06': {'points': [(3600, 2290), (3600, 2400)], 'label': (4250, 2345)},
        'relation.ad05.f07': {'points': [(3600, 2710), (3600, 2900)], 'label': (3600, 2805)},
        'relation.ad05.f08': {'points': [(3600, 3210), (3600, 3400)], 'label': (3600, 3305)},
        'relation.ad05.f09': {'points': [(3600, 3710), (3600, 3950)], 'label': (3600, 3830)},
        'relation.ad05.f10': {'points': [(3930, 4170), (5000, 4355)], 'label': (4450, 4130)},
        'relation.ad05.f11': {'points': [(6800, 4355), (9000, 4355), (9000, 7736), (5304, 7736)], 'label': (9000, 6000)},
        'relation.ad05.f12': {'points': [(3600, 4390), (3600, 4500)], 'label': (4250, 4445)},
        'relation.ad05.f13': {'points': [(3600, 4810), (3600, 5000)], 'label': (3600, 4905)},
        'relation.ad05.f14': {'points': [(3600, 5310), (3600, 5500)], 'label': (3600, 5405)},
        'relation.ad05.f15': {'points': [(3600, 5810), (3600, 6050)], 'label': (3600, 5930)},
        'relation.ad05.f16': {'points': [(3270, 6270), (2300, 6755)], 'label': (2750, 6400)},
        'relation.ad05.f17': {'points': [(2300, 6755), (1200, 6755), (1200, 7736), (4895, 7736)], 'label': (1200, 7300)},
        'relation.ad05.f18': {'points': [(3930, 6270), (5000, 6755)], 'label': (4450, 6400)},
        'relation.ad05.f19': {'points': [(6800, 6755), (10000, 6755), (10000, 3555), (4500, 3555)], 'label': (10000, 5200)},
        'relation.ad05.f20': {'points': [(6800, 6755), (10300, 6755), (10300, 3555), (4500, 3555)], 'label': (10300, 5200)},
        'relation.ad05.f21': {'points': [(5100, 7873), (5100, 8296)], 'label': (5100, 8080)},
    },
}

AD06_LAYOUT = ActivityLayout(width=11000, height=9500, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD06 = {
    'initial': {'activity.ad06.initial': (3600, 550)},
    'actions': {
        'activity.ad06.a01': (2700, 800), 'activity.ad06.a00': (500, 1480), 'activity.ad06.a02': (2700, 1900), 'activity.ad06.a03': (2700, 2400),
        'activity.ad06.a04': (500, 3100), 'activity.ad06.a05': (2700, 3500), 'activity.ad06.a06': (2700, 4000), 'activity.ad06.a07': (2700, 4500),
        'activity.ad06.a08': (2700, 5000), 'activity.ad06.a09': (500, 6000), 'activity.ad06.a10': (500, 6600), 'activity.ad06.a11': (2700, 6600),
        'activity.ad06.a12': (5000, 7350), 'activity.ad06.a13': (2700, 7700), 'activity.ad06.a14': (2700, 8100),
    },
    'decisions': {'activity.ad06.d00': (3270, 1300), 'activity.ad06.d01': (3270, 2900), 'activity.ad06.d02': (3270, 5500), 'activity.ad06.d03': (3270, 6100), 'activity.ad06.d04': (3270, 7150)},
    'merges': {'activity.ad06.mend': (3395, 8600)},
    'final': {'activity.ad06.final': (3600, 9250)},
    'routes': {
        'relation.ad06.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad06.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad06.f03': {'points': [(3270, 1520), (2300, 1635)], 'label': (2750, 1420)},
        'relation.ad06.f04': {'points': [(1400, 1790), (250, 1790), (250, 8736), (3395, 8736)], 'label': (250, 5200)},
        'relation.ad06.f05': {'points': [(3600, 1740), (3600, 1900)], 'label': (4250, 1820)},
        'relation.ad06.f06': {'points': [(3600, 2210), (3600, 2400)], 'label': (3600, 2305)},
        'relation.ad06.f07': {'points': [(3600, 2710), (3600, 2900)], 'label': (3600, 2805)},
        'relation.ad06.f08': {'points': [(3270, 3120), (2300, 3255)], 'label': (2750, 3020)},
        'relation.ad06.f09': {'points': [(1400, 3410), (400, 3410), (400, 8736), (3395, 8736)], 'label': (400, 6000)},
        'relation.ad06.f10': {'points': [(3600, 3340), (3600, 3500)], 'label': (4250, 3420)},
        'relation.ad06.f11': {'points': [(3600, 3810), (3600, 4000)], 'label': (3600, 3905)},
        'relation.ad06.f12': {'points': [(3600, 4310), (3600, 4500)], 'label': (3600, 4405)},
        'relation.ad06.f13': {'points': [(3600, 4810), (3600, 5000)], 'label': (3600, 4905)},
        'relation.ad06.f14': {'points': [(3600, 5310), (3600, 5500)], 'label': (3600, 5405)},
        'relation.ad06.f15': {'points': [(3270, 5720), (2300, 6155)], 'label': (2750, 5820)},
        'relation.ad06.f16': {'points': [(1400, 6310), (1400, 8100), (2700, 8255)], 'label': (1400, 7200)},
        'relation.ad06.f17': {'points': [(3600, 5940), (3600, 6100)], 'label': (4250, 6020)},
        'relation.ad06.f18': {'points': [(3270, 6320), (2300, 6755)], 'label': (2750, 6420)},
        'relation.ad06.f19': {'points': [(1400, 6910), (1400, 8100), (2700, 8255)], 'label': (1400, 7500)},
        'relation.ad06.f20': {'points': [(3600, 6540), (3600, 6600)], 'label': (4250, 6570)},
        'relation.ad06.f21': {'points': [(3600, 6910), (3600, 7150)], 'label': (3600, 7030)},
        'relation.ad06.f22': {'points': [(3930, 7370), (5000, 7505)], 'label': (4450, 7270)},
        'relation.ad06.f23': {'points': [(6800, 7505), (7600, 7505), (7600, 8255), (4500, 8255)], 'label': (7600, 7900)},
        'relation.ad06.f24': {'points': [(3600, 7590), (3600, 7700)], 'label': (4250, 7645)},
        'relation.ad06.f25': {'points': [(3600, 8010), (3600, 8100)], 'label': (3600, 8055)},
        'relation.ad06.f26': {'points': [(3600, 8410), (3600, 8600)], 'label': (3600, 8505)},
        'relation.ad06.f27': {'points': [(3600, 8773), (3600, 9196)], 'label': (3600, 8980)},
    },
}

AD07_LAYOUT = ActivityLayout(width=7800, height=8500, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD07 = {
    'initial': {'activity.ad07.initial': (3600, 550)},
    'actions': {
        'activity.ad07.a01': (2700, 800), 'activity.ad07.a02': (2700, 1300), 'activity.ad07.a03': (4800, 1950),
        'activity.ad07.a04': (2700, 2450), 'activity.ad07.a05': (4800, 3250), 'activity.ad07.a06': (2700, 3650),
        'activity.ad07.a07': (2700, 4150), 'activity.ad07.a08': (2700, 4650), 'activity.ad07.a09': (2700, 5150), 'activity.ad07.a10': (2700, 5650),
    },
    'decisions': {'activity.ad07.d01': (3270, 1850), 'activity.ad07.d02': (3270, 3050)},
    'merges': {'activity.ad07.mend': (3395, 6650)},
    'final': {'activity.ad07.final': (3600, 7450)},
    'routes': {
        'relation.ad07.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad07.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad07.f03': {'points': [(3600, 1610), (3600, 1850)], 'label': (3600, 1730)},
        'relation.ad07.f04': {'points': [(3930, 2070), (4800, 2105)], 'label': (4350, 2020)},
        'relation.ad07.f05': {'points': [(6600, 2105), (7350, 2105), (7350, 6786), (3804, 6786)], 'label': (7100, 4450)},
        'relation.ad07.f06': {'points': [(3600, 2290), (3600, 2450)], 'label': (4250, 2370)},
        'relation.ad07.f07': {'points': [(3600, 2760), (3600, 3050)], 'label': (3600, 2905)},
        'relation.ad07.f08': {'points': [(3930, 3270), (4800, 3405)], 'label': (4350, 3230)},
        'relation.ad07.f09': {'points': [(6600, 3405), (7150, 3405), (7150, 6786), (3804, 6786)], 'label': (6900, 5000)},
        'relation.ad07.f10': {'points': [(3600, 3490), (3600, 3650)], 'label': (4250, 3570)},
        'relation.ad07.f11': {'points': [(3600, 3960), (3600, 4150)], 'label': (3600, 4055)},
        'relation.ad07.f12': {'points': [(3600, 4460), (3600, 4650)], 'label': (3600, 4555)},
        'relation.ad07.f13': {'points': [(3600, 4960), (3600, 5150)], 'label': (3600, 5055)},
        'relation.ad07.f14': {'points': [(3600, 5460), (3600, 5650)], 'label': (3600, 5555)},
        'relation.ad07.f15': {'points': [(3600, 5960), (3600, 6650)], 'label': (3600, 6305)},
        'relation.ad07.f16': {'points': [(3600, 6823), (3600, 7396)], 'label': (3600, 7100)},
    },
}

AD08_LAYOUT = ActivityLayout(width=7800, height=8400, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD08 = {
    'initial': {'activity.ad08.initial': (3600, 550)},
    'actions': {
        'activity.ad08.a01': (2700, 800), 'activity.ad08.a02': (2700, 1300), 'activity.ad08.a03': (2700, 1800),
        'activity.ad08.a00': (4800, 2450), 'activity.ad08.a04': (2700, 2850), 'activity.ad08.a05': (4800, 3650),
        'activity.ad08.a06': (2700, 4050), 'activity.ad08.a07': (2700, 4550), 'activity.ad08.a08': (2700, 5050), 'activity.ad08.a09': (2700, 5550),
    },
    'decisions': {'activity.ad08.d00': (3270, 2350), 'activity.ad08.d01': (3270, 3450)},
    'merges': {'activity.ad08.mend': (3395, 6550)},
    'final': {'activity.ad08.final': (3600, 7350)},
    'routes': {
        'relation.ad08.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad08.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad08.f03': {'points': [(3600, 1610), (3600, 1800)], 'label': (3600, 1705)},
        'relation.ad08.f04': {'points': [(3600, 2110), (3600, 2350)], 'label': (3600, 2230)},
        'relation.ad08.f05': {'points': [(3930, 2570), (4800, 2605)], 'label': (4350, 2520)},
        'relation.ad08.f06': {'points': [(6600, 2605), (7350, 2605), (7350, 6686), (3804, 6686)], 'label': (7100, 4700)},
        'relation.ad08.f07': {'points': [(3600, 2790), (3600, 2850)], 'label': (4250, 2820)},
        'relation.ad08.f08': {'points': [(3600, 3160), (3600, 3450)], 'label': (3600, 3305)},
        'relation.ad08.f09': {'points': [(3930, 3670), (4800, 3805)], 'label': (4350, 3630)},
        'relation.ad08.f10': {'points': [(6600, 3805), (7150, 3805), (7150, 6686), (3804, 6686)], 'label': (6900, 5200)},
        'relation.ad08.f11': {'points': [(3600, 3890), (3600, 4050)], 'label': (4250, 3970)},
        'relation.ad08.f12': {'points': [(3600, 4360), (3600, 4550)], 'label': (3600, 4455)},
        'relation.ad08.f13': {'points': [(3600, 4860), (3600, 5050)], 'label': (3600, 4955)},
        'relation.ad08.f14': {'points': [(3600, 5360), (3600, 5550)], 'label': (3600, 5455)},
        'relation.ad08.f15': {'points': [(3600, 5860), (3600, 6550)], 'label': (3600, 6205)},
        'relation.ad08.f16': {'points': [(3600, 6723), (3600, 7296)], 'label': (3600, 7000)},
    },
}

AD09_LAYOUT = ActivityLayout(width=7800, height=8700, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD09 = {
    'initial': {'activity.ad09.initial': (3600, 550)},
    'actions': {
        'activity.ad09.a01': (2700, 800), 'activity.ad09.a02': (2700, 1300), 'activity.ad09.a03': (2700, 1800), 'activity.ad09.a04': (2700, 2300),
        'activity.ad09.a05': (4800, 3150), 'activity.ad09.a06': (2700, 3450), 'activity.ad09.a07': (2700, 3950), 'activity.ad09.a08': (4800, 4750),
        'activity.ad09.a09': (2700, 5150), 'activity.ad09.a10': (2700, 5650), 'activity.ad09.a11': (2700, 6150), 'activity.ad09.a12': (2700, 6650),
    },
    'decisions': {'activity.ad09.d01': (3270, 2850), 'activity.ad09.d02': (3270, 4550)},
    'merges': {'activity.ad09.mend': (3395, 7550)},
    'final': {'activity.ad09.final': (3600, 8300)},
    'routes': {
        'relation.ad09.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad09.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad09.f03': {'points': [(3600, 1610), (3600, 1800)], 'label': (3600, 1705)},
        'relation.ad09.f04': {'points': [(3600, 2110), (3600, 2300)], 'label': (3600, 2205)},
        'relation.ad09.f05': {'points': [(3600, 2610), (3600, 2850)], 'label': (3600, 2730)},
        'relation.ad09.f06': {'points': [(3930, 3070), (4800, 3305)], 'label': (4350, 3000)},
        'relation.ad09.f07': {'points': [(6600, 3305), (7350, 3305), (7350, 7686), (3804, 7686)], 'label': (7100, 5500)},
        'relation.ad09.f08': {'points': [(3600, 3290), (3600, 3450)], 'label': (4250, 3370)},
        'relation.ad09.f09': {'points': [(3600, 3760), (3600, 3950)], 'label': (3600, 3855)},
        'relation.ad09.f10': {'points': [(3600, 4260), (3600, 4550)], 'label': (3600, 4405)},
        'relation.ad09.f11': {'points': [(3930, 4770), (4800, 4905)], 'label': (4350, 4730)},
        'relation.ad09.f12': {'points': [(6600, 4905), (7150, 4905), (7150, 7686), (3804, 7686)], 'label': (6900, 6200)},
        'relation.ad09.f13': {'points': [(3600, 4990), (3600, 5150)], 'label': (4250, 5070)},
        'relation.ad09.f14': {'points': [(3600, 5460), (3600, 5650)], 'label': (3600, 5555)},
        'relation.ad09.f15': {'points': [(3600, 5960), (3600, 6150)], 'label': (3600, 6055)},
        'relation.ad09.f16': {'points': [(3600, 6460), (3600, 6650)], 'label': (3600, 6555)},
        'relation.ad09.f17': {'points': [(3600, 6960), (3600, 7550)], 'label': (3600, 7255)},
        'relation.ad09.f18': {'points': [(3600, 7723), (3600, 8246)], 'label': (3600, 7980)},
    },
}

AD10_LAYOUT = ActivityLayout(width=9000, height=8700, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1900, note_height=300)

AD10 = {
    'initial': {'activity.ad10.initial': (3600, 550)},
    'actions': {
        'activity.ad10.a01': (2700, 800), 'activity.ad10.a02': (2700, 1300), 'activity.ad10.a03': (5000, 1950), 'activity.ad10.a04': (5000, 2850),
        'activity.ad10.a05': (5000, 3750), 'activity.ad10.a06': (2700, 3900), 'activity.ad10.a07': (2700, 4400), 'activity.ad10.a08': (2700, 4900),
        'activity.ad10.a09': (2700, 5400), 'activity.ad10.a10': (2700, 5900), 'activity.ad10.a11': (2700, 6400),
    },
    'decisions': {'activity.ad10.d01': (3270, 1850), 'activity.ad10.d02': (3270, 2400), 'activity.ad10.d03': (3270, 3300)},
    'merges': {'activity.ad10.mend': (3395, 7350)},
    'notes': {'activity.ad10.note-correction': (600, 5700)},
    'final': {'activity.ad10.final': (3600, 8100)},
    'routes': {
        'relation.ad10.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad10.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad10.f03': {'points': [(3600, 1610), (3600, 1850)], 'label': (3600, 1730)},
        'relation.ad10.f04': {'points': [(3930, 2070), (5000, 2105)], 'label': (4450, 2020)},
        'relation.ad10.f05': {'points': [(6800, 2105), (8500, 2105), (8500, 7486), (3804, 7486)], 'label': (8500, 4800)},
        'relation.ad10.f06': {'points': [(3600, 2290), (3600, 2400)], 'label': (4250, 2345)},
        'relation.ad10.f07': {'points': [(3930, 2620), (5000, 3005)], 'label': (4450, 2580)},
        'relation.ad10.f08': {'points': [(6800, 3005), (8300, 3005), (8300, 7486), (3804, 7486)], 'label': (8300, 5200)},
        'relation.ad10.f09': {'points': [(3600, 2840), (3600, 3300)], 'label': (4250, 3070)},
        'relation.ad10.f10': {'points': [(3930, 3520), (5000, 3905)], 'label': (4450, 3480)},
        'relation.ad10.f11': {'points': [(6800, 3905), (8100, 3905), (8100, 7486), (3804, 7486)], 'label': (8100, 5700)},
        'relation.ad10.f12': {'points': [(3600, 3740), (3600, 3900)], 'label': (4250, 3820)},
        'relation.ad10.f13': {'points': [(3600, 4210), (3600, 4400)], 'label': (3600, 4305)},
        'relation.ad10.f14': {'points': [(3600, 4710), (3600, 4900)], 'label': (3600, 4805)},
        'relation.ad10.f15': {'points': [(3600, 5210), (3600, 5400)], 'label': (3600, 5305)},
        'relation.ad10.f16': {'points': [(3600, 5710), (3600, 5900)], 'label': (3600, 5805)},
        'relation.ad10.f17': {'points': [(3600, 6210), (3600, 6400)], 'label': (3600, 6305)},
        'relation.ad10.f18': {'points': [(3600, 6710), (3600, 7350)], 'label': (3600, 7030)},
        'relation.ad10.f19': {'points': [(3600, 7523), (3600, 8046)], 'label': (3600, 7780)},
    },
}

AD11_LAYOUT = ActivityLayout(width=10500, height=9500, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD11 = {
    'initial': {'activity.ad11.initial': (3600, 550)},
    'actions': {
        'activity.ad11.a01': (2700, 800), 'activity.ad11.a02': (2700, 1300), 'activity.ad11.a03': (500, 2000), 'activity.ad11.a04': (500, 2600), 'activity.ad11.a05': (500, 3200),
        'activity.ad11.a06': (2700, 3650), 'activity.ad11.a07': (2700, 4150), 'activity.ad11.a08': (2700, 4650), 'activity.ad11.a09': (500, 5650),
        'activity.ad11.a10': (500, 6250), 'activity.ad11.a11': (5000, 6250), 'activity.ad11.a12': (2700, 7150),
    },
    'decisions': {'activity.ad11.d01': (3270, 1850), 'activity.ad11.d02': (3270, 2450), 'activity.ad11.d03': (3270, 3050), 'activity.ad11.d04': (3270, 5150), 'activity.ad11.d05': (3270, 5750)},
    'merges': {'activity.ad11.mend': (3395, 8050)},
    'final': {'activity.ad11.final': (3600, 8850)},
    'routes': {
        'relation.ad11.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad11.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad11.f03': {'points': [(3600, 1610), (3600, 1850)], 'label': (3600, 1730)},
        'relation.ad11.f04': {'points': [(3270, 2070), (2300, 2155)], 'label': (2750, 2000)},
        'relation.ad11.f05': {'points': [(1400, 2310), (200, 2310), (200, 8186), (3395, 8186)], 'label': (200, 5200)},
        'relation.ad11.f06': {'points': [(3600, 2290), (3600, 2450)], 'label': (4250, 2370)},
        'relation.ad11.f07': {'points': [(3270, 2670), (2300, 2755)], 'label': (2750, 2600)},
        'relation.ad11.f08': {'points': [(1400, 2910), (400, 2910), (400, 8186), (3395, 8186)], 'label': (400, 5500)},
        'relation.ad11.f09': {'points': [(3600, 2890), (3600, 3050)], 'label': (4250, 2970)},
        'relation.ad11.f10': {'points': [(3270, 3270), (2300, 3355)], 'label': (2750, 3200)},
        'relation.ad11.f11': {'points': [(1400, 3510), (600, 3510), (600, 8186), (3395, 8186)], 'label': (600, 5800)},
        'relation.ad11.f12': {'points': [(3600, 3490), (3600, 3650)], 'label': (4250, 3570)},
        'relation.ad11.f13': {'points': [(3600, 3960), (3600, 4150)], 'label': (3600, 4055)},
        'relation.ad11.f14': {'points': [(3600, 4460), (3600, 4650)], 'label': (3600, 4555)},
        'relation.ad11.f15': {'points': [(3600, 4960), (3600, 5150)], 'label': (3600, 5055)},
        'relation.ad11.f16': {'points': [(3270, 5370), (2300, 5805)], 'label': (2750, 5470)},
        'relation.ad11.f17': {'points': [(1400, 5960), (1400, 7150), (2700, 7305)], 'label': (1400, 6550)},
        'relation.ad11.f18': {'points': [(3600, 5590), (3600, 5750)], 'label': (4250, 5670)},
        'relation.ad11.f19': {'points': [(3270, 5970), (2300, 6405)], 'label': (2750, 6070)},
        'relation.ad11.f20': {'points': [(1400, 6560), (1400, 7150), (2700, 7305)], 'label': (1400, 6850)},
        'relation.ad11.f21': {'points': [(3930, 5970), (5000, 6405)], 'label': (4450, 6070)},
        'relation.ad11.f22': {'points': [(5900, 6560), (5900, 7305), (4500, 7305)], 'label': (5900, 6900)},
        'relation.ad11.f23': {'points': [(3600, 7460), (3600, 8050)], 'label': (3600, 7755)},
        'relation.ad11.f24': {'points': [(3600, 8223), (3600, 8796)], 'label': (3600, 8500)},
    },
}

AD12_LAYOUT = ActivityLayout(width=10000, height=8000, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD12 = {
    'initial': {'activity.ad12.initial': (3600, 550)},
    'actions': {
        'activity.ad12.a01': (2700, 800), 'activity.ad12.a02': (5000, 1500), 'activity.ad12.a03': (2700, 2000),
        'activity.ad12.a04': (500, 3200), 'activity.ad12.a05': (500, 3700), 'activity.ad12.a06': (500, 4200), 'activity.ad12.a07': (500, 4700), 'activity.ad12.a08': (500, 5200),
        'activity.ad12.a09': (2700, 3200), 'activity.ad12.a10': (5000, 3200), 'activity.ad12.a11': (7300, 3200),
    },
    'decisions': {'activity.ad12.d01': (3270, 1400), 'activity.ad12.d02': (3270, 2600)},
    'merges': {'activity.ad12.mend': (4895, 6500)},
    'final': {'activity.ad12.final': (5100, 7350)},
    'routes': {
        'relation.ad12.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad12.f02': {'points': [(3600, 1110), (3600, 1400)], 'label': (3600, 1255)},
        'relation.ad12.f03': {'points': [(3930, 1620), (5000, 1655)], 'label': (4450, 1570)},
        'relation.ad12.f04': {'points': [(6800, 1655), (9000, 1655), (9000, 6636), (5304, 6636)], 'label': (9000, 4100)},
        'relation.ad12.f05': {'points': [(3600, 1840), (3600, 2000)], 'label': (4250, 1920)},
        'relation.ad12.f06': {'points': [(3600, 2310), (3600, 2600)], 'label': (3600, 2455)},
        'relation.ad12.f07': {'points': [(3270, 2820), (2300, 3355)], 'label': (2750, 2920)},
        'relation.ad12.f08': {'points': [(1400, 3510), (1400, 3700)], 'label': (1400, 3605)},
        'relation.ad12.f09': {'points': [(1400, 4010), (1400, 4200)], 'label': (1400, 4105)},
        'relation.ad12.f10': {'points': [(1400, 4510), (1400, 4700)], 'label': (1400, 4605)},
        'relation.ad12.f11': {'points': [(1400, 5010), (1400, 5200)], 'label': (1400, 5105)},
        'relation.ad12.f12': {'points': [(1400, 5510), (1400, 6636), (4895, 6636)], 'label': (1400, 6070)},
        'relation.ad12.f13': {'points': [(3600, 2820), (3600, 3200)], 'label': (4250, 3000)},
        'relation.ad12.f14': {'points': [(3600, 3510), (3600, 6636), (4895, 6636)], 'label': (3600, 5000)},
        'relation.ad12.f15': {'points': [(3930, 2820), (5000, 3355)], 'label': (4450, 2920)},
        'relation.ad12.f16': {'points': [(5900, 3510), (5900, 6636), (5304, 6636)], 'label': (5900, 5000)},
        'relation.ad12.f17': {'points': [(3930, 2820), (7300, 3355)], 'label': (5800, 2920)},
        'relation.ad12.f18': {'points': [(8200, 3510), (8200, 6636), (5304, 6636)], 'label': (8200, 5000)},
        'relation.ad12.f19': {'points': [(5100, 6773), (5100, 7296)], 'label': (5100, 7040)},
    },
}

AD13_LAYOUT = ActivityLayout(width=13000, height=11200, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD13 = {
    'initial': {'activity.ad13.initial': (3600, 550)},
    'actions': {
        'activity.ad13.a01': (2700, 800), 'activity.ad13.a02': (2700, 1300), 'activity.ad13.a03': (2700, 2300), 'activity.ad13.a04': (2700, 2800),
        'activity.ad13.a05': (2700, 3300), 'activity.ad13.a06': (2700, 3800), 'activity.ad13.a07': (500, 4850), 'activity.ad13.a08': (2700, 4850),
        'activity.ad13.a09': (500, 5900), 'activity.ad13.a10': (2700, 5900), 'activity.ad13.a11': (5000, 4850), 'activity.ad13.a12': (2700, 6500),
        'activity.ad13.a17': (5000, 5450), 'activity.ad13.a13': (2700, 7600), 'activity.ad13.a14': (2700, 8100), 'activity.ad13.a15': (5200, 8750), 'activity.ad13.a16': (2700, 9250),
    },
    'decisions': {'activity.ad13.d01': (3270, 1800), 'activity.ad13.d02': (3270, 4300), 'activity.ad13.d03': (3270, 5400), 'activity.ad13.d04': (3270, 7100), 'activity.ad13.d05': (3270, 8650)},
    'merges': {'activity.ad13.mend': (3395, 10100)},
    'final': {'activity.ad13.final': (3600, 10850)},
    'routes': {
        'relation.ad13.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad13.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad13.f03': {'points': [(3600, 1610), (3600, 1800)], 'label': (3600, 1705)},
        'relation.ad13.f04': {'points': [(3600, 2020), (3600, 2300)], 'label': (4250, 2150)},
        'relation.ad13.f05': {'points': [(3600, 2610), (3600, 2800)], 'label': (3600, 2705)},
        'relation.ad13.f06': {'points': [(3930, 2020), (4500, 2020), (4500, 2955), (4500, 2955)], 'label': (4300, 1900)},
        'relation.ad13.f07': {'points': [(3600, 3110), (3600, 3300)], 'label': (3600, 3205)},
        'relation.ad13.f08': {'points': [(3600, 3610), (3600, 3800)], 'label': (3600, 3705)},
        'relation.ad13.f09': {'points': [(3600, 4110), (3600, 4300)], 'label': (3600, 4205)},
        'relation.ad13.f10': {'points': [(3270, 4520), (2300, 5005)], 'label': (2750, 4620)},
        'relation.ad13.f11': {'points': [(1400, 5160), (1400, 6500), (2700, 6655)], 'label': (1400, 5800)},
        'relation.ad13.f12': {'points': [(3600, 4520), (3600, 4850)], 'label': (4250, 4680)},
        'relation.ad13.f13': {'points': [(3600, 5160), (3600, 5400)], 'label': (3600, 5280)},
        'relation.ad13.f14': {'points': [(3270, 5620), (2300, 6055)], 'label': (2750, 5720)},
        'relation.ad13.f15': {'points': [(1400, 6210), (1400, 6655), (2700, 6655)], 'label': (1400, 6420)},
        'relation.ad13.f16': {'points': [(3930, 5620), (4500, 5620), (4500, 6055), (4500, 6655)], 'label': (4300, 5720)},
        'relation.ad13.f17': {'points': [(3270, 4520), (5000, 5005)], 'label': (4200, 4620)},
        'relation.ad13.f18': {'points': [(6800, 5005), (6800, 5450)], 'label': (6800, 5220)},
        'relation.ad13.f19': {'points': [(6800, 5760), (10000, 5760), (10000, 10236), (3804, 10236)], 'label': (10000, 7850)},
        'relation.ad13.f20': {'points': [(3600, 6810), (3600, 7100)], 'label': (3600, 6955)},
        'relation.ad13.f21': {'points': [(3270, 7320), (1500, 7320), (1500, 3955), (2700, 3955)], 'label': (1500, 5650)},
        'relation.ad13.f22': {'points': [(3600, 7320), (3600, 7600)], 'label': (4250, 7450)},
        'relation.ad13.f23': {'points': [(3600, 7910), (3600, 8100)], 'label': (3600, 8005)},
        'relation.ad13.f24': {'points': [(3600, 8410), (3600, 8650)], 'label': (3600, 8530)},
        'relation.ad13.f25': {'points': [(3930, 8870), (5200, 8905)], 'label': (4500, 8820)},
        'relation.ad13.f26': {'points': [(7000, 8905), (11400, 8905), (11400, 3955), (4500, 3955)], 'label': (11400, 6500)},
        'relation.ad13.f27': {'points': [(3600, 9090), (3600, 9250)], 'label': (4250, 9170)},
        'relation.ad13.f28': {'points': [(3600, 9560), (3600, 10100)], 'label': (3600, 9830)},
        'relation.ad13.f29': {'points': [(3600, 9720), (3600, 10100)], 'label': (3600, 9870)},
        'relation.ad13.f30': {'points': [(3600, 10273), (3600, 10796)], 'label': (3600, 10530)},
    },
}

AD14_LAYOUT = ActivityLayout(width=9000, height=8200, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD14 = {
    'initial': {'activity.ad14.initial': (3600, 550)},
    'actions': {
        'activity.ad14.a01': (2700, 800), 'activity.ad14.a02': (2700, 1300), 'activity.ad14.a03': (5000, 1950),
        'activity.ad14.a04': (2700, 2450), 'activity.ad14.a05': (2700, 2950), 'activity.ad14.a06': (2700, 3450), 'activity.ad14.a07': (5000, 4050),
        'activity.ad14.a08': (2700, 4550), 'activity.ad14.a09': (2700, 5050), 'activity.ad14.a10': (2700, 5550), 'activity.ad14.a11': (2700, 6050),
    },
    'decisions': {'activity.ad14.d01': (3270, 1850), 'activity.ad14.d02': (3270, 3950)},
    'merges': {'activity.ad14.mend': (3395, 6950)},
    'final': {'activity.ad14.final': (3600, 7750)},
    'routes': {
        'relation.ad14.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad14.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad14.f03': {'points': [(3600, 1610), (3600, 1850)], 'label': (3600, 1730)},
        'relation.ad14.f04': {'points': [(3930, 2070), (5000, 2105)], 'label': (4450, 2020)},
        'relation.ad14.f05': {'points': [(6800, 2105), (8000, 2105), (8000, 7036), (3804, 7036)], 'label': (8000, 4600)},
        'relation.ad14.f06': {'points': [(3600, 2290), (3600, 2450)], 'label': (4250, 2370)},
        'relation.ad14.f07': {'points': [(3600, 2760), (3600, 2950)], 'label': (3600, 2855)},
        'relation.ad14.f08': {'points': [(3600, 3260), (3600, 3450)], 'label': (3600, 3355)},
        'relation.ad14.f09': {'points': [(3600, 3760), (3600, 3950)], 'label': (3600, 3855)},
        'relation.ad14.f10': {'points': [(3930, 4170), (5000, 4205)], 'label': (4450, 4130)},
        'relation.ad14.f11': {'points': [(6800, 4205), (8500, 4205), (8500, 955), (4500, 955)], 'label': (8500, 2750)},
        'relation.ad14.f12': {'points': [(3600, 4390), (3600, 4550)], 'label': (4250, 4470)},
        'relation.ad14.f13': {'points': [(3600, 4860), (3600, 5050)], 'label': (3600, 4955)},
        'relation.ad14.f14': {'points': [(3600, 5360), (3600, 5550)], 'label': (3600, 5455)},
        'relation.ad14.f15': {'points': [(3600, 5860), (3600, 6050)], 'label': (3600, 5955)},
        'relation.ad14.f16': {'points': [(3600, 6360), (3600, 6950)], 'label': (3600, 6655)},
        'relation.ad14.f17': {'points': [(3600, 7123), (3600, 7696)], 'label': (3600, 7400)},
    },
}

AD15_LAYOUT = ActivityLayout(width=9000, height=6800, title_y=190, action_width=1800, action_height=310, decision_width=660, decision_height=440, note_width=1700, note_height=300)

AD15 = {
    'initial': {'activity.ad15.initial': (3600, 550)},
    'actions': {
        'activity.ad15.a01': (2700, 800), 'activity.ad15.a02': (2700, 1300), 'activity.ad15.a03': (2700, 1800),
        'activity.ad15.a04': (5200, 2450), 'activity.ad15.a05': (5200, 3000), 'activity.ad15.a06': (2700, 2900),
        'activity.ad15.a07': (1000, 3950), 'activity.ad15.a08': (5200, 3950), 'activity.ad15.a09': (2700, 4650),
    },
    'decisions': {'activity.ad15.d01': (3270, 2350), 'activity.ad15.d02': (3270, 3500)},
    'merges': {'activity.ad15.mend': (3395, 5500)},
    'final': {'activity.ad15.final': (3600, 6300)},
    'routes': {
        'relation.ad15.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad15.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad15.f03': {'points': [(3600, 1610), (3600, 1800)], 'label': (3600, 1705)},
        'relation.ad15.f04': {'points': [(3600, 2110), (3600, 2350)], 'label': (3600, 2230)},
        'relation.ad15.f05': {'points': [(3930, 2570), (5200, 2605)], 'label': (4500, 2520)},
        'relation.ad15.f06': {'points': [(6100, 2760), (6100, 3000)], 'label': (6100, 2880)},
        'relation.ad15.f07': {'points': [(6100, 3310), (7000, 3310), (7000, 5720), (3804, 5720)], 'label': (7000, 4450)},
        'relation.ad15.f08': {'points': [(3600, 2790), (3600, 2900)], 'label': (4250, 2840)},
        'relation.ad15.f09': {'points': [(3600, 3210), (3600, 3500)], 'label': (3600, 3355)},
        'relation.ad15.f10': {'points': [(3270, 3720), (2800, 3720), (2800, 4105)], 'label': (2200, 3670)},
        'relation.ad15.f11': {'points': [(1900, 4260), (1900, 4805), (2700, 4805)], 'label': (1900, 4530)},
        'relation.ad15.f12': {'points': [(3930, 3720), (5200, 3720), (5200, 4105)], 'label': (4500, 3670)},
        'relation.ad15.f13': {'points': [(6100, 4260), (6100, 4805), (4500, 4805)], 'label': (6100, 4530)},
        'relation.ad15.f14': {'points': [(3600, 4960), (3600, 5500)], 'label': (3600, 5230)},
        'relation.ad15.f15': {'points': [(3600, 5673), (3600, 6246)], 'label': (3600, 5960)},
    },
}

AD16_LAYOUT = ActivityLayout(width=9500, height=9700, title_y=190, action_width=1800, action_height=310, decision_width=900, decision_height=600, note_width=1700, note_height=300)

AD16 = {
    'initial': {'activity.ad16.initial': (3600, 550)},
    'actions': {
        'activity.ad16.a01': (2700, 800), 'activity.ad16.a02': (2700, 1300), 'activity.ad16.a03': (5000, 1950),
        'activity.ad16.a04': (2700, 2500), 'activity.ad16.a05': (2700, 3000), 'activity.ad16.a06': (2700, 3500),
        'activity.ad16.a07': (500, 4700), 'activity.ad16.a08': (2700, 5200), 'activity.ad16.a09': (500, 6500),
        'activity.ad16.a10': (2700, 7200), 'activity.ad16.a11': (2700, 7700),
    },
    'decisions': {'activity.ad16.d01': (3150, 1800), 'activity.ad16.d02': (3150, 4000), 'activity.ad16.d03': (3150, 5700)},
    'merges': {'activity.ad16.mend': (3321, 8400)},
    'final': {'activity.ad16.final': (3600, 9300)},
    'routes': {
        'relation.ad16.f01': {'points': [(3600, 588), (3600, 800)], 'label': (3600, 690)},
        'relation.ad16.f02': {'points': [(3600, 1110), (3600, 1300)], 'label': (3600, 1205)},
        'relation.ad16.f03': {'points': [(3600, 1610), (3600, 1800)], 'label': (3600, 1705)},
        'relation.ad16.f04': {'points': [(4050, 2100), (5000, 2105)], 'label': (4500, 2020)},
        'relation.ad16.f05': {'points': [(6800, 2105), (8500, 2105), (8500, 8586), (3879, 8586)], 'label': (8500, 5200)},
        'relation.ad16.f06': {'points': [(3600, 2400), (3600, 2500)], 'label': (4300, 2450)},
        'relation.ad16.f07': {'points': [(3600, 2810), (3600, 3000)], 'label': (3600, 2905)},
        'relation.ad16.f08': {'points': [(3600, 3310), (3600, 3500)], 'label': (3600, 3405)},
        'relation.ad16.f09': {'points': [(3600, 3810), (3600, 4000)], 'label': (3600, 3905)},
        'relation.ad16.f10': {'points': [(3150, 4300), (1400, 4300), (1400, 4700)], 'label': (2300, 4250)},
        'relation.ad16.f11': {'points': [(1400, 5010), (1400, 5355), (2700, 5355)], 'label': (1400, 5190)},
        'relation.ad16.f12': {'points': [(3600, 4600), (3600, 5200)], 'label': (4250, 4900)},
        'relation.ad16.f13': {'points': [(3600, 5510), (3600, 5700)], 'label': (3600, 5605)},
        'relation.ad16.f14': {'points': [(3150, 6000), (2300, 6000), (2300, 6655)], 'label': (2700, 5950)},
        'relation.ad16.f15': {'points': [(1400, 6810), (1400, 7355), (2700, 7355)], 'label': (1400, 7080)},
        'relation.ad16.f16': {'points': [(4050, 6000), (5300, 6000), (5300, 7355), (4500, 7355)], 'label': (4800, 5950)},
        'relation.ad16.f17': {'points': [(3600, 7510), (3600, 7700)], 'label': (3600, 7605)},
        'relation.ad16.f18': {'points': [(3600, 8010), (3600, 8400)], 'label': (3600, 8205)},
        'relation.ad16.f19': {'points': [(3600, 8772), (3600, 9246)], 'label': (3600, 9000)},
    },
}

LAYOUTS: dict[str, tuple[ActivityLayout, dict]] = {
    'aafiatak-ad01-register-patient': (AD01_LAYOUT, AD01),
    'aafiatak-ad02-log-in': (AD02_LAYOUT, AD02),
    'aafiatak-ad03-book-appointment': (AD03_LAYOUT, AD03),
    'aafiatak-ad04-process-full-payment': (AD04_LAYOUT, AD04),
    'aafiatak-ad05-subscribe-to-availability-alert': (AD05_LAYOUT, AD05),
    'aafiatak-ad06-cancel-appointment': (AD06_LAYOUT, AD06),
    'aafiatak-ad07-publish-availability': (AD07_LAYOUT, AD07),
    'aafiatak-ad08-withdraw-remaining-capacity': (AD08_LAYOUT, AD08),
    'aafiatak-ad09-reschedule-appointment': (AD09_LAYOUT, AD09),
    'aafiatak-ad10-register-patient-check-in': (AD10_LAYOUT, AD10),
    'aafiatak-ad11-record-no-show': (AD11_LAYOUT, AD11),
    'aafiatak-ad12-handle-late-arrival': (AD12_LAYOUT, AD12),
    'aafiatak-ad13-manage-operational-exceptions': (AD13_LAYOUT, AD13),
    'aafiatak-ad14-call-next-patient': (AD14_LAYOUT, AD14),
    'aafiatak-ad15-review-facility-onboarding-request': (AD15_LAYOUT, AD15),
    'aafiatak-ad16-suspend-facility': (AD16_LAYOUT, AD16),
}


def layout_for(view_id: str) -> tuple[ActivityLayout, dict]:
    try:
        return LAYOUTS[view_id]
    except KeyError as exc:
        raise ValueError(f'No curated activity layout registered for {view_id}') from exc
