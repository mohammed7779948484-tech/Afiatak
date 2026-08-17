from __future__ import annotations

# Compact A3-landscape equivalent grid. The reduced logical canvas increases
# report-scale typography while retaining clear horizontal paths for messages.
CANVAS = (6000, 4243)
TITLE_Y = 150
HEADER_Y = 290
LIFELINE_TOP = 585
LIFELINE_BOTTOM = 3950

PARTICIPANT_X = {
    'actor.sd01.visitor': 600,
    'object.sd01.patient-application': 1800,
    'object.sd01.backend': 3000,
    'object.sd01.data-store': 4200,
    'object.sd01.whatsapp-provider': 5400,
}

PARTICIPANT_WIDTH = {
    'actor.sd01.visitor': 650,
    'object.sd01.patient-application': 900,
    'object.sd01.backend': 900,
    'object.sd01.data-store': 900,
    'object.sd01.whatsapp-provider': 1050,
}

MESSAGE_Y = {
    'message.sd01.m01': 800,
    'message.sd01.m02': 960,
    'message.sd01.m03': 1120,
    'message.sd01.m04': 1280,
    'message.sd01.m05': 1440,
    'message.sd01.m06': 1600,
    'message.sd01.m07': 1760,
    'message.sd01.m08': 1920,
    'message.sd01.m09': 2080,
    'message.sd01.m10': 2240,
    'message.sd01.m11': 2400,
    'message.sd01.m12': 2560,
    'message.sd01.m13': 2720,
    'message.sd01.m14': 2880,
    'message.sd01.m15': 3040,
    'message.sd01.m16': 3200,
    'message.sd01.m17': 3360,
    'message.sd01.m18': 3520,
    'message.sd01.m19': 3680,
}

ACTIVATIONS = (
    ('object.sd01.patient-application', 770, 1015, 16),
    ('object.sd01.backend', 930, 1950, 0),
    ('object.sd01.backend', 1100, 1190, 24),
    ('object.sd01.data-store', 1250, 1470, 0),
    ('object.sd01.whatsapp-provider', 1570, 1790, 0),
    ('object.sd01.patient-application', 1890, 2430, 0),
    ('object.sd01.backend', 2370, 2760, 0),
    ('object.sd01.backend', 2540, 2630, 24),
    ('object.sd01.patient-application', 2690, 3070, 16),
    ('object.sd01.backend', 3010, 3550, 0),
    ('object.sd01.data-store', 3170, 3390, 0),
    ('object.sd01.patient-application', 3490, 3710, 0),
)
