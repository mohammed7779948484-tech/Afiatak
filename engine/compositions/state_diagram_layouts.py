from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StateLayout:
    width: int = 7500
    height: int = 5303
    title_y: int = 185
    state_width: int = 1250
    state_height: int = 360


STD01 = {
    "states": {
        "state.std01.draft": (1000, 1700),
        "state.std01.published": (3000, 1700),
        "state.std01.frozen": (3000, 3150),
        "state.std01.closed": (5100, 1450),
        "state.std01.cancelled": (5100, 3300),
    },
    "initial": {"state.std01.initial": (560, 1880)},
    "final": {"state.std01.final-closed": (6800, 1630), "state.std01.final-cancelled": (6800, 3480)},
    "routes": {
        "relation.std01.t01": {"points": [(615, 1880), (1000, 1880)], "label": (805, 1745)},
        "relation.std01.t02": {"points": [(2250, 1880), (3000, 1880)], "label": (2625, 1660)},
        "relation.std01.t03": {"points": [(3625, 2060), (3625, 3150)], "label": (3920, 2320)},
        "relation.std01.t04": {"points": [(2960, 3330), (2650, 3330), (2650, 1640), (3000, 1640)], "label": (2380, 2470)},
        "relation.std01.t05": {"points": [(4250, 1820), (5100, 1630)], "label": (4650, 1515)},
        "relation.std01.t06": {"points": [(4250, 3330), (4600, 3330), (4600, 1630), (5100, 1630)], "label": (4770, 2400)},
        "relation.std01.t07": {"points": [(3625, 2060), (3625, 2700), (4700, 2700), (4700, 3480), (5100, 3480)], "label": (4160, 2835)},
        "relation.std01.t08": {"points": [(4250, 3330), (5100, 3480)], "label": (4680, 3590)},
        "relation.std01.t09": {"points": [(6350, 1630), (6748, 1630)], "label": (6550, 1515)},
        "relation.std01.t10": {"points": [(6350, 3480), (6748, 3480)], "label": (6550, 3365)},
    },
}


STD02 = {
    "states": {
        "state.std02.open": (1750, 1800),
        "state.std02.frozen": (3600, 3100),
        "state.std02.closed": (5500, 1800),
    },
    "initial": {"state.std02.initial": (900, 1980)},
    "final": {"state.std02.final": (7050, 1980)},
    "routes": {
        "relation.std02.t01": {"points": [(955, 1980), (1750, 1980)], "label": (1320, 1860)},
        "relation.std02.t02": {"points": [(2375, 2160), (2375, 2650), (4225, 2650), (4225, 3100)], "label": (3310, 2540)},
        "relation.std02.t03": {"points": [(3600, 3280), (3000, 3280), (3000, 1620), (2375, 1620), (2375, 1800)], "label": (2770, 2460)},
        "relation.std02.t04": {"points": [(3000, 1980), (5500, 1980)], "label": (4250, 1870)},
        "relation.std02.t05": {"points": [(4850, 3280), (5100, 3280), (5100, 1980), (5500, 1980)], "label": (5260, 2650)},
        "relation.std02.t06": {"points": [(6750, 1980), (6998, 1980)], "label": (6870, 1870)},
    },
}


STD03 = {
    "states": {
        "state.std03.active": (1500, 2300),
        "state.std03.consumed": (5100, 1050),
        "state.std03.expired": (5100, 2300),
        "state.std03.released": (5100, 3550),
    },
    "initial": {"state.std03.initial": (720, 2480)},
    "final": {
        "state.std03.final-consumed": (6950, 1230),
        "state.std03.final-expired": (6950, 2480),
        "state.std03.final-released": (6950, 3730),
    },
    "routes": {
        "relation.std03.t01": {"points": [(775, 2480), (1500, 2480)], "label": (1130, 2180)},
        "relation.std03.t02": {"points": [(2750, 2400), (3300, 2400), (3300, 1230), (5100, 1230)], "label": (4050, 1120)},
        "relation.std03.t03": {"points": [(2750, 2530), (3550, 2530), (3550, 1450), (4700, 1450), (4700, 1230), (5100, 1230)], "label": (4140, 1660)},
        "relation.std03.t04": {"points": [(2750, 2480), (5100, 2480)], "label": (3940, 2370)},
        "relation.std03.t05": {"points": [(2750, 2600), (3350, 2600), (3350, 3730), (5100, 3730)], "label": (3750, 3250)},
        "relation.std03.t06": {"points": [(2225, 2660), (2225, 4300), (4650, 4300), (4650, 3730), (5100, 3730)], "label": (3500, 4210)},
        "relation.std03.t07": {"points": [(6350, 1230), (6898, 1230)], "label": (6620, 1120)},
        "relation.std03.t08": {"points": [(6350, 2480), (6898, 2480)], "label": (6620, 2370)},
        "relation.std03.t09": {"points": [(6350, 3730), (6898, 3730)], "label": (6620, 3620)},
    },
}


STD04 = {
    "states": {
        "state.std04.confirmed": (1600, 2300),
        "state.std04.cancelled-patient": (5000, 1250),
        "state.std04.cancelled-facility": (5000, 3400),
    },
    "initial": {"state.std04.initial": (760, 2480)},
    "final": {"state.std04.final-patient": (6950, 1430), "state.std04.final-facility": (6950, 3580)},
    "routes": {
        "relation.std04.t01": {"points": [(815, 2480), (1600, 2480)], "label": (1180, 2120)},
        "relation.std04.t02": {"points": [(2850, 2410), (3300, 2410), (3300, 1430), (5000, 1430)], "label": (4100, 1120)},
        "relation.std04.t03": {"points": [(2850, 2550), (3300, 2550), (3300, 3580), (5000, 3580)], "label": (4100, 3290)},
        "relation.std04.t04": {"points": [(6250, 1430), (6898, 1430)], "label": (6575, 1320)},
        "relation.std04.t05": {"points": [(6250, 3580), (6898, 3580)], "label": (6575, 3470)},
    },
}


STD05 = {
    "states": {
        "state.std05.created": (1000, 2400),
        "state.std05.processing": (2600, 2400),
        "state.std05.succeeded": (4300, 1100),
        "state.std05.failed": (4300, 2350),
        "state.std05.expired": (4300, 3550),
        "state.std05.under-review": (6100, 1100),
        "state.std05.refund-pending": (4300, 4400),
        "state.std05.refunded": (6100, 4400),
    },
    "initial": {"state.std05.initial": (500, 2580)},
    "final": {
        "state.std05.final-failed": (6300, 2530),
        "state.std05.final-expired": (6300, 3730),
        "state.std05.final-refunded": (6725, 4970),
    },
    "routes": {
        "relation.std05.t01": {"points": [(555, 2580), (1000, 2580)], "label": (770, 2390)},
        "relation.std05.t02": {"points": [(2250, 2580), (2600, 2580)], "label": (2425, 2470)},
        "relation.std05.t03": {"points": [(1625, 2760), (1625, 3730), (4300, 3730)], "label": (2880, 3620)},
        "relation.std05.t04": {"points": [(3225, 2400), (3225, 1720), (4300, 1280)], "label": (3740, 1540)},
        "relation.std05.t05": {"points": [(3850, 2530), (4300, 2530)], "label": (4070, 2420)},
        "relation.std05.t06": {"points": [(3225, 2760), (3225, 3730), (4300, 3730)], "label": (3760, 3830)},
        "relation.std05.t07": {"points": [(3225, 2400), (3225, 700), (6100, 700), (6100, 1280)], "label": (4680, 570)},
        "relation.std05.t08": {"points": [(5550, 1280), (6100, 1280)], "label": (5820, 1000)},
        "relation.std05.t09": {"points": [(4925, 1460), (5700, 1460), (5700, 4300), (4925, 4300), (4925, 4400)], "label": (5870, 3010)},
        "relation.std05.t10": {"points": [(5550, 4580), (6100, 4580)], "label": (5825, 4470)},
        "relation.std05.t11": {"points": [(5550, 2530), (6248, 2530)], "label": (5900, 2420)},
        "relation.std05.t12": {"points": [(5550, 3730), (6248, 3730)], "label": (5900, 3620)},
        "relation.std05.t13": {"points": [(6725, 4760), (6725, 4918)], "label": (6910, 4845)},
    },
}


STD06 = {
    "states": {
        "state.std06.created": (1100, 2400),
        "state.std06.checked-in": (2800, 2400),
        "state.std06.in-service": (4500, 2400),
        "state.std06.completed": (5700, 1100),
        "state.std06.not-completed": (5700, 3400),
        "state.std06.no-show": (3100, 4000),
    },
    "initial": {"state.std06.initial": (500, 2580)},
    "final": {
        "state.std06.final-completed": (7000, 1280),
        "state.std06.final-not-completed": (7000, 3580),
        "state.std06.final-no-show": (5200, 4180),
    },
    "routes": {
        "relation.std06.t01": {"points": [(555, 2580), (1100, 2580)], "label": (810, 2390)},
        "relation.std06.t02": {"points": [(2350, 2580), (2800, 2580)], "label": (2575, 2920)},
        "relation.std06.t03": {"points": [(1725, 2400), (1725, 1700), (3425, 1700), (3425, 2400)], "label": (2575, 1560)},
        "relation.std06.t04": {"points": [(1725, 2760), (1725, 4180), (3100, 4180)], "label": (2375, 3880)},
        "relation.std06.t05": {"points": [(4050, 2580), (4500, 2580)], "label": (4275, 2920)},
        "relation.std06.t06": {"points": [(3425, 2760), (3425, 3580), (5700, 3580)], "label": (4560, 3470)},
        "relation.std06.t07": {"points": [(5125, 2400), (5125, 1280), (5700, 1280)], "label": (5420, 1110)},
        "relation.std06.t08": {"points": [(5125, 2760), (5125, 3950), (6325, 3950), (6325, 3760)], "label": (5725, 4050)},
        "relation.std06.t09": {"points": [(3425, 2400), (3425, 2050), (2450, 2050), (2450, 2220), (2350, 2220), (2350, 2400)], "label": (2920, 2190)},
        "relation.std06.t10": {"points": [(6950, 1280), (6948, 1280)], "label": (6830, 1170)},
        "relation.std06.t11": {"points": [(6950, 3580), (6948, 3580)], "label": (6830, 3470)},
        "relation.std06.t12": {"points": [(4350, 4180), (5148, 4180)], "label": (4750, 4070)},
    },
}


STD07 = {
    "states": {
        "state.std07.waiting": (1500, 2400),
        "state.std07.called": (3400, 2400),
        "state.std07.done": (5400, 1500),
        "state.std07.removed": (5400, 3400),
    },
    "initial": {"state.std07.initial": (800, 2580)},
    "final": {"state.std07.final-done": (7050, 1680), "state.std07.final-removed": (7050, 3580)},
    "routes": {
        "relation.std07.t01": {"points": [(855, 2580), (1500, 2580)], "label": (1160, 2390)},
        "relation.std07.t02": {"points": [(2750, 2580), (3400, 2580)], "label": (3075, 2470)},
        "relation.std07.t03": {"points": [(4650, 2400), (4650, 1680), (5400, 1680)], "label": (5030, 1535)},
        "relation.std07.t04": {"points": [(2125, 2760), (2125, 3100), (5000, 3100), (5000, 3580), (5400, 3580)], "label": (3560, 2990)},
        "relation.std07.t05": {"points": [(4025, 2760), (4025, 4250), (6025, 4250), (6025, 3760)], "label": (5025, 4370)},
        "relation.std07.t06": {"points": [(6650, 1680), (6998, 1680)], "label": (6825, 1570)},
        "relation.std07.t07": {"points": [(6650, 3580), (6998, 3580)], "label": (6825, 3470)},
    },
}


LAYOUTS = {"aafiatak-std01-availability-release": STD01, "aafiatak-std02-arrival-group": STD02, "aafiatak-std03-reservation-hold": STD03, "aafiatak-std04-appointment": STD04, "aafiatak-std05-payment-intent": STD05, "aafiatak-std06-visit-instance": STD06, "aafiatak-std07-queue-entry": STD07}


def layout_for(view_id: str) -> tuple[StateLayout, dict]:
    if view_id not in LAYOUTS:
        raise ValueError(f"No curated state layout registered for {view_id}")
    return StateLayout(), LAYOUTS[view_id]
