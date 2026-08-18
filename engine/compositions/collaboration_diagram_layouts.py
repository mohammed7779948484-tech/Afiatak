from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CollaborationLayout:
    width: int = 16000
    height: int = 10400
    title_y: int = 250
    participant_width: int = 2350
    participant_height: int = 760
    message_font_size: int = 62
    participant_font_size: int = 64


# Each composition is a graph-derived spatial arrangement.  Participants use
# centre coordinates. Link blocks define dedicated clear-space rectangles where
# reusable-link messages are stacked; no timeline, lifeline, or activation data
# exists in this model.
LAYOUTS: dict[str, tuple[CollaborationLayout, dict]] = {
    "aafiatak-cd01-patient-registration-otp": (
        CollaborationLayout(),
        {
            "participants": {
                "participant.cd01.aafiatak-backend": (8000, 5000),
                "participant.cd01.patient-application": (2200, 5000),
                "participant.cd01.aafiatak-data-store": (8000, 1650),
                "participant.cd01.whatsapp-authentication-provider": (13300, 7350),
                "participant.cd01.visitor": (5100, 8650),
            },
            "links": {
                "L01": {"labelBox": (9000, 1950, 3950), "side": "right"},
                "L02": {"labelBox": (3900, 3250, 3700), "side": "above"},
                "L03": {"labelBox": (9900, 4700, 3900), "side": "above"},
                "L04": {"labelBox": (400, 6500, 2300), "side": "left"},
                "L05": {"labelBox": (8200, 8350, 4200), "side": "above"},
            },
            "selfMessages": {
                "message.cd01.03": {"box": (8850, 5200, 3500), "side": "right"},
                "message.cd01.12": {"box": (8850, 6050, 3500), "side": "right"},
            },
        },
    ),
    "aafiatak-cd02-book-appointment-full-payment": (
        CollaborationLayout(),
        {
            "participants": {
                "participant.cd02.aafiatak-backend": (8000, 5000),
                "participant.cd02.aafiatak-data-store": (8000, 1450),
                "participant.cd02.patient-application": (2350, 4650),
                "participant.cd02.patient": (2500, 8450),
                "participant.cd02.payment-gateway": (13200, 7600),
                "participant.cd02.notification-service": (13200, 2550),
            },
            "links": {
                "L01": {"labelBox": (9250, 1150, 4300), "side": "right"},
                "L02": {"labelBox": (10300, 3150, 3900), "side": "below"},
                "L03": {"labelBox": (3400, 2450, 3900), "side": "above"},
                "L04": {"labelBox": (10100, 4700, 4200), "side": "right"},
                "L05": {"labelBox": (3500, 6100, 3000), "side": "right"},
                "L06": {"labelBox": (5900, 8350, 3900), "side": "above"},
                "L07": {"labelBox": (5550, 6500, 4100), "side": "below"},
            },
            "selfMessages": {},
        },
    ),
    "aafiatak-cd03-cancel-appointment-full-refund": (
        CollaborationLayout(),
        {
            "participants": {
                "participant.cd03.aafiatak-backend": (8000, 5000),
                "participant.cd03.aafiatak-data-store": (8000, 1600),
                "participant.cd03.patient-application": (2300, 4700),
                "participant.cd03.patient": (2450, 8350),
                "participant.cd03.payment-gateway": (13200, 7200),
                "participant.cd03.notification-service": (13200, 2600),
            },
            "links": {
                "L01": {"labelBox": (9150, 1750, 4200), "side": "right"},
                "L02": {"labelBox": (10350, 3200, 3700), "side": "below"},
                "L03": {"labelBox": (3450, 2700, 3900), "side": "above"},
                "L04": {"labelBox": (10100, 5050, 4000), "side": "right"},
                "L05": {"labelBox": (3550, 6100, 3000), "side": "right"},
            },
            "selfMessages": {
                "message.cd03.05": {"box": (8700, 6950, 3700), "side": "right"},
            },
        },
    ),
    "aafiatak-cd04-reschedule-appointment": (
        CollaborationLayout(),
        {
            "participants": {
                "participant.cd04.aafiatak-backend": (8000, 5000),
                "participant.cd04.aafiatak-data-store": (8000, 1600),
                "participant.cd04.facility-web-dashboard": (2300, 4700),
                "participant.cd04.booking-and-reception-staff": (2400, 8350),
                "participant.cd04.notification-service": (13200, 2700),
                "participant.cd04.patient": (13200, 8200),
            },
            "links": {
                "L01": {"labelBox": (9150, 1750, 4200), "side": "right"},
                "L02": {"labelBox": (3450, 2600, 3900), "side": "above"},
                "L03": {"labelBox": (10350, 3450, 3700), "side": "below"},
                "L04": {"labelBox": (3500, 6200, 3200), "side": "right"},
                "L05": {"labelBox": (9500, 7200, 2800), "side": "left"},
            },
            "selfMessages": {},
        },
    ),
    "aafiatak-cd05-checkin-queue-call-next": (
        CollaborationLayout(),
        {
            "participants": {
                "participant.cd05.aafiatak-backend": (8000, 5000),
                "participant.cd05.aafiatak-data-store": (8000, 1300),
                "participant.cd05.facility-web-dashboard": (2200, 4400),
                "participant.cd05.booking-and-reception-staff": (2200, 7900),
                "participant.cd05.doctor-interface": (13200, 4400),
                "participant.cd05.doctor": (13200, 7500),
                "participant.cd05.notification-service": (11900, 8600),
                "participant.cd05.patient": (4200, 8800),
            },
            "links": {
                "L01": {"labelBox": (9250, 950, 4300), "side": "right"},
                "L02": {"labelBox": (10100, 2450, 3900), "side": "right"},
                "L03": {"labelBox": (3350, 2200, 4000), "side": "above"},
                "L04": {"labelBox": (9200, 6500, 3700), "side": "above"},
                "L05": {"labelBox": (3300, 5850, 3000), "side": "right"},
                "L06": {"labelBox": (360, 7000, 3000), "side": "left"},
                "L07": {"labelBox": (10100, 5750, 3000), "side": "left"},
                "L08": {"labelBox": (6700, 8650, 3600), "side": "above"},
            },
            "selfMessages": {"message.cd05.06": {"box": (8700, 5750, 4000), "side": "right"}},
        },
    ),
    "aafiatak-cd06-operational-exception": (
        CollaborationLayout(),
        {
            "participants": {
                "participant.cd06.aafiatak-backend": (8000, 5000),
                "participant.cd06.aafiatak-data-store": (8000, 1350),
                "participant.cd06.facility-web-dashboard": (2300, 4400),
                "participant.cd06.booking-and-reception-staff": (2300, 8600),
                "participant.cd06.payment-gateway": (13300, 5000),
                "participant.cd06.notification-service": (12500, 8000),
                "participant.cd06.patient": (13200, 9300),
            },
            "links": {
                "L01": {"labelBox": (9100, 900, 4300), "side": "right"},
                "L02": {"labelBox": (3250, 2350, 4000), "side": "above"},
                "L03": {"labelBox": (9000, 6250, 3900), "side": "above"},
                "L04": {"labelBox": (10200, 4050, 3900), "side": "above"},
                "L05": {"labelBox": (400, 5500, 3300), "side": "left"},
                "L06": {"labelBox": (9000, 8650, 2900), "side": "above"},
            },
            "selfMessages": {},
        },
    ),
}


def layout_for(view_id: str) -> tuple[CollaborationLayout, dict]:
    return LAYOUTS[view_id]
