from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CollaborationLayout:
    """Shared paper and typography system; scenario topology belongs below."""

    width: int = 16000
    height: int = 10400
    participant_width: int = 2200
    participant_height: int = 720
    participant_font_size: int = 64
    message_font_size: int = 62
    message_line_height: int = 78


# This is intentionally not a list of free-floating message coordinates.  Each
# link declares only an allowed placement side/order, desired maximum line width,
# and local gap.  The geometry planner places complete message runs next to the
# real structural link while avoiding participants, other links, loops, labels,
# the heading, and page edges.
LAYOUTS: dict[str, tuple[CollaborationLayout, dict]] = {
    "aafiatak-cd01-patient-registration-otp": (
        CollaborationLayout(),
        {
            "participants": {
                "participant.cd01.aafiatak-backend": (7850, 5000),
                "participant.cd01.patient-application": (2750, 5000),
                "participant.cd01.aafiatak-data-store": (7850, 1800),
                "participant.cd01.whatsapp-authentication-provider": (13150, 7250),
                "participant.cd01.visitor": (5000, 8550),
            },
            "links": {
                "L01": {"side": ("right", "left"), "maxLabelWidth": 2800, "labelGap": 210},
                "L02": {"side": ("above", "below"), "maxLabelWidth": 3000, "labelGap": 190},
                "L03": {"side": ("above", "below", "right"), "maxLabelWidth": 2750, "labelGap": 190},
                "L04": {"side": ("left", "right"), "maxLabelWidth": 2600, "labelGap": 190},
                "L05": {"side": ("above", "below"), "maxLabelWidth": 2600, "labelGap": 190},
            },
            "selfMessages": {
                "participant.cd01.aafiatak-backend": {"sides": ("right", "left", "below", "above")},
            },
        },
    ),
    "aafiatak-cd02-book-appointment-full-payment": (
        CollaborationLayout(),
        {
            "participants": {
                "participant.cd02.aafiatak-backend": (7850, 5050),
                "participant.cd02.aafiatak-data-store": (7850, 1700),
                "participant.cd02.patient-application": (2500, 4750),
                "participant.cd02.patient": (2600, 8600),
                "participant.cd02.payment-gateway": (13200, 7550),
                "participant.cd02.notification-service": (13200, 2550),
            },
            "links": {
                "L01": {"side": ("right", "left"), "maxLabelWidth": 3000, "labelGap": 240},
                "L02": {"side": ("above", "below", "right"), "maxLabelWidth": 2600, "labelGap": 190},
                "L03": {"side": ("above", "below"), "maxLabelWidth": 2850, "labelGap": 190},
                "L04": {"side": ("above", "below", "right"), "maxLabelWidth": 2750, "labelGap": 190},
                "L05": {"side": ("right", "left"), "maxLabelWidth": 2500, "labelGap": 190},
                "L06": {"side": ("above", "below"), "maxLabelWidth": 2500, "labelGap": 190},
                "L07": {"side": ("below", "above"), "maxLabelWidth": 2500, "labelGap": 190},
            },
            "selfMessages": {},
        },
    ),
    "aafiatak-cd03-cancel-appointment-full-refund": (
        CollaborationLayout(),
        {
            "participants": {
                "participant.cd03.aafiatak-backend": (7850, 5050),
                "participant.cd03.aafiatak-data-store": (7850, 1750),
                "participant.cd03.patient-application": (2550, 4750),
                "participant.cd03.patient": (2600, 8500),
                "participant.cd03.payment-gateway": (13200, 7200),
                "participant.cd03.notification-service": (13200, 2550),
            },
            "links": {
                "L01": {"side": ("right", "left"), "maxLabelWidth": 2900, "labelGap": 220},
                "L02": {"side": ("above", "below", "right"), "maxLabelWidth": 2500, "labelGap": 190},
                "L03": {"side": ("above", "below"), "maxLabelWidth": 2800, "labelGap": 190},
                "L04": {"side": ("above", "below", "right"), "maxLabelWidth": 2650, "labelGap": 190},
                "L05": {"side": ("right", "left"), "maxLabelWidth": 2400, "labelGap": 190},
            },
            "selfMessages": {
                "participant.cd03.aafiatak-backend": {"sides": ("left", "right", "below", "above")},
            },
        },
    ),
    "aafiatak-cd04-reschedule-appointment": (
        CollaborationLayout(),
        {
            "participants": {
                "participant.cd04.aafiatak-backend": (7850, 5050),
                "participant.cd04.aafiatak-data-store": (7850, 1750),
                "participant.cd04.facility-web-dashboard": (2500, 4700),
                "participant.cd04.booking-and-reception-staff": (2550, 8500),
                "participant.cd04.notification-service": (13200, 2650),
                "participant.cd04.patient": (13200, 8200),
            },
            "links": {
                "L01": {"side": ("right", "left"), "maxLabelWidth": 2900, "labelGap": 220},
                "L02": {"side": ("above", "below"), "maxLabelWidth": 2800, "labelGap": 190},
                "L03": {"side": ("below", "above", "right"), "maxLabelWidth": 2500, "labelGap": 190},
                "L04": {"side": ("right", "left"), "maxLabelWidth": 2500, "labelGap": 190},
                "L05": {"side": ("left", "right"), "maxLabelWidth": 2400, "labelGap": 190},
            },
            "selfMessages": {},
        },
    ),
    "aafiatak-cd05-checkin-queue-call-next": (
        CollaborationLayout(participant_width=2150),
        {
            "participants": {
                "participant.cd05.aafiatak-backend": (7850, 5000),
                "participant.cd05.aafiatak-data-store": (7850, 1650),
                "participant.cd05.facility-web-dashboard": (2200, 4400),
                "participant.cd05.booking-and-reception-staff": (2200, 7800),
                "participant.cd05.doctor-interface": (13200, 4400),
                "participant.cd05.doctor": (13200, 7500),
                "participant.cd05.notification-service": (11600, 8700),
                "participant.cd05.patient": (4500, 9000),
            },
            "links": {
                "L01": {"side": ("right", "left"), "maxLabelWidth": 3000, "labelGap": 240},
                "L02": {"side": ("above", "below", "right"), "maxLabelWidth": 2600, "labelGap": 190},
                "L03": {"side": ("above", "below"), "maxLabelWidth": 2800, "labelGap": 190},
                "L04": {"side": ("above", "below", "right"), "maxLabelWidth": 2550, "labelGap": 190},
                "L05": {"side": ("right", "left"), "maxLabelWidth": 2500, "labelGap": 190},
                "L06": {"side": ("left", "right"), "maxLabelWidth": 2300, "labelGap": 190},
                "L07": {"side": ("left", "right"), "maxLabelWidth": 2300, "labelGap": 190},
                "L08": {"side": ("above", "below"), "maxLabelWidth": 2500, "labelGap": 190},
            },
            "selfMessages": {
                "participant.cd05.aafiatak-backend": {"sides": ("below", "left", "right", "above"), "labelSide": "left"},
            },
        },
    ),
    "aafiatak-cd06-operational-exception": (
        CollaborationLayout(),
        {
            "participants": {
                "participant.cd06.aafiatak-backend": (7850, 5000),
                "participant.cd06.aafiatak-data-store": (7850, 1700),
                "participant.cd06.facility-web-dashboard": (2500, 4400),
                "participant.cd06.booking-and-reception-staff": (2500, 8550),
                "participant.cd06.payment-gateway": (13250, 5000),
                "participant.cd06.notification-service": (12250, 7900),
                "participant.cd06.patient": (13200, 9250),
            },
            "links": {
                "L01": {"side": ("right", "left"), "maxLabelWidth": 3000, "labelGap": 240},
                "L02": {"side": ("above", "below"), "maxLabelWidth": 2700, "labelGap": 190},
                "L03": {"side": ("above", "below", "right"), "maxLabelWidth": 2550, "labelGap": 190},
                "L04": {"side": ("above", "below", "right"), "maxLabelWidth": 2500, "labelGap": 190},
                "L05": {"side": ("left", "right"), "maxLabelWidth": 2400, "labelGap": 190},
                "L06": {"side": ("above", "below"), "maxLabelWidth": 2300, "labelGap": 190},
            },
            "selfMessages": {},
        },
    ),
}


def layout_for(view_id: str) -> tuple[CollaborationLayout, dict]:
    return LAYOUTS[view_id]
