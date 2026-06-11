# =========================
# CAREER SUCCESS RULES
# =========================

CAREER_SUCCESS_RULES = {

    frozenset([2,6,10,11]): {
        "score":150,
        "event":"COMPLETE_CAREER_SUCCESS"
    },

    frozenset([6,10,11]): {
        "score":150,
        "event":"CAREER_RISE"
    },

    frozenset([10,11]): {
        "score":150,
        "event":"STATUS_AND_RECOGNITION"
    },

    frozenset([6,11]): {
        "score":150,
        "event":"GAIN_FROM_OPPOSITION"
    },

    frozenset([2,11]): {
        "score":100,
        "event":"INCOME_GAIN"
    },

    frozenset([11]): {
        "score":90,
        "event":"GAIN"
    },

    frozenset([8,11]): {
        "score":90,
        "event":"UNEARNED_GAIN"
    },

    frozenset([2,6,10]): {
        "score":75,
        "event":"PROFESSIONAL_PROGRESS"
    },

    frozenset([6,10]): {
        "score":70,
        "event":"EMPLOYMENT_SUCCESS"
    },

    frozenset([6]): {
        "score":60,
        "event":"EMPLOYMENT"
    },

    frozenset([10]): {
        "score":55,
        "event":"PROFESSION"
    },

    frozenset([2]): {
        "score":50,
        "event":"EARNINGS"
    }
}


# =========================
# CAREER FAILURE RULES
# =========================

CAREER_FAILURE_RULES = {

    frozenset([6,8]): {
        "score": -100,
        "event": "ADVERSE_WORK_ENVIRONMENT"
    },

    frozenset([6,12]): {
        "score": -120,
        "event": "STRESSED_SERVICE"
    },

    frozenset([8,12]): {
        "score": -150,
        "event": "VALUE_DESTRUCTION"
    },

    frozenset([6,8,12]): {
        "score": -150,
        "event": "RESIGNATION"
    },

    frozenset([5,8,12]): {
        "score": -180,
        "event": "TERMINATION"
    }
}

# =========================
# SPECIAL EVENT DESCRIPTIONS
# =========================

SPECIAL_EVENTS = {

    # Positive Events

    "GAIN_FROM_OPPOSITION":
        "Extraordinary gain through competition, opposition, litigation, interview, examination or selection process.",

    "UNEARNED_GAIN":
        "Unexpected financial gain, settlement, inheritance, insurance, gratuity, PF, compensation or windfall.",

    "STATUS_AND_RECOGNITION":
        "Promotion, authority, recognition, visibility and professional status improvement.",

    "COMPLETE_CAREER_SUCCESS":
        "Income, position, achievement and professional success indicated.",

    "CAREER_RISE":
        "Professional advancement, career growth and progress indicated.",

    "INCOME_GAIN":
        "Income increase, financial growth and monetary benefits indicated.",

    "GAIN":
        "Fulfilment of desires and realization of expectations.",

    "EMPLOYMENT_SUCCESS":
        "Success in employment, service matters and professional efforts.",

    "EMPLOYMENT":
        "Employment opportunities and service-related developments indicated.",

    "PROFESSION":
        "Professional activities and career matters activated.",

    "EARNINGS":
        "Income generation and financial activity indicated.",

    "PROFESSIONAL_PROGRESS":
        "Steady professional development and career improvement.",
            # Negative Events

    "ADVERSE_WORK_ENVIRONMENT":
        "Native may work under difficult, stressful or hostile professional circumstances.",

    "STRESSED_SERVICE":
        "Pressure, dissatisfaction, sacrifice and stress in service environment indicated.",

    "VALUE_DESTRUCTION":
        "Loss, depreciation or destruction of value indicated. In business this may manifest through inventory loss, product depreciation, asset impairment or financial erosion.",

    "RESIGNATION":
        "Resignation, voluntary exit or separation from service indicated.",

    "TERMINATION":
        "Suspension, termination, dismissal or removal from position indicated."
}


 