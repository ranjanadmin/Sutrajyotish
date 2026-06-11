def classify(score):

    if score >= 120:
       return "GOOD"

    if score <= -120:
        return "BAD"

    return "MIXED"

def evaluate_dba(
    maha_score,
    bhukti_score,
    antara_score
):

    md = classify(maha_score)
    bd = classify(bhukti_score)
    ad = classify(antara_score)

    if md=="GOOD" and bd=="GOOD" and ad=="GOOD":

        return {
            "status":"MAJOR_RISE",
            "income":"INCREASE",
            "timeline":
            "Strong period for promotion, status and income growth."
        }

    if md=="BAD" and bd=="GOOD" and ad=="GOOD":

        return {
            "status":"NO_STATUS_RISE",
            "income":"GOOD",
            "timeline":
            "Income continues but status may not improve."
        }

    if md=="GOOD" and bd=="BAD" and ad=="BAD":

        return {
            "status":"STATUS_RETAINED",
            "income":"MAJOR_LOSS",
            "timeline":
            "Status remains protected but financial pressure is likely."
        }

    if md=="BAD" and bd=="BAD" and ad=="GOOD":

        return {
            "status":"NO_IMPROVEMENT",
            "income":"TEMP_SUPPORT",
            "timeline":
            "Temporary support exists but major progress is unlikely."
        }

    if md=="GOOD" and bd=="BAD" and ad=="GOOD":

        return {
            "status":"STAGNANT",
            "income":"AVERAGE",
            "timeline":
            "Some relief exists but no major progress."
        }

    if md=="BAD" and bd=="BAD" and ad=="GOOD":

        return {
            "status":"NO_IMPROVEMENT",
            "income":"TEMP_SUPPORT",
            "timeline":
            "Temporary support exists but major progress is unlikely."
        }

    if md=="GOOD" and bd=="BAD" and ad=="GOOD":

        return {
            "status":"STAGNANT",
            "income":"AVERAGE",
            "timeline":
            "Some relief exists but no major progress."
        }

    if md=="GOOD" and bd=="GOOD" and ad=="BAD":

        return {
            "status":"INVESTMENT_PHASE",
            "income":"EXPENSE",
            "timeline":
            "Investment, expansion or asset acquisition likely. Wait for next Antara."
        }

    return {
        "status":"MIXED",
        "income":"MIXED",
        "timeline":"Mixed results."
    }

SUCCESS_EVENTS = {
    "COMPLETE_CAREER_SUCCESS",
    "CAREER_RISE",
    "STATUS_AND_RECOGNITION",
    "GAIN_FROM_OPPOSITION",
    "INCOME_GAIN",
    "GAIN",
    "PROFESSIONAL_PROGRESS",
    "EMPLOYMENT_SUCCESS",
    "EMPLOYMENT",
    "PROFESSION",
    "EARNINGS"
}

FAILURE_EVENTS = {
    "ADVERSE_WORK_ENVIRONMENT",
    "STRESSED_SERVICE",
    "VALUE_DESTRUCTION",
    "RESIGNATION",
    "TERMINATION"
}

def evaluate_event_dba(
    maha_events,
    bhukti_events,
    antara_events
):

    maha_success = any(
        e in SUCCESS_EVENTS
        for e in maha_events
    )

    bhukti_success = any(
        e in SUCCESS_EVENTS
        for e in bhukti_events
    )

    antara_success = any(
        e in SUCCESS_EVENTS
        for e in antara_events
    )

    if (
        maha_success and
        bhukti_success and
        antara_success
    ):
        return {
            "event": "CAREER_SUCCESS",
            "confidence": "HIGH"
        }

    maha_failure = any(
        e in FAILURE_EVENTS
        for e in maha_events
    )

    bhukti_failure = any(
        e in FAILURE_EVENTS
        for e in bhukti_events
    )

    antara_failure = any(
        e in FAILURE_EVENTS
        for e in antara_events
    )

    if (
        maha_failure and
        bhukti_failure and
        antara_failure
    ):
        return {
            "event": "CAREER_FAILURE",
            "confidence": "HIGH"
        }

    if (
        maha_success and
        bhukti_success
    ):
        return {
            "event": "PROMISED",
            "confidence": "MEDIUM"
        }

    return {
        "event": "NONE",
        "confidence": "LOW"
    }

def evaluate_promotion_dba(
    maha_info,
    bhukti_info,
    antara_info
):

    promotion_strength = (
        maha_info.get("positive", 0)
        + bhukti_info.get("positive", 0)
        + antara_info.get("positive", 0)
    )

    adverse_strength = (
        maha_info.get("negative", 0)
        + bhukti_info.get("negative", 0)
        + antara_info.get("negative", 0)
    )

    if promotion_strength > adverse_strength:

        return {
            "event": "PROMOTION",
            "confidence": "HIGH"
        }

    return {
        "event": "NO_PROMOTION",
        "confidence": "LOW"
    }


def evaluate_job_change_dba(
    maha_planet,
    bhukti_planet,
    antara_planet,
    kp_grid
):

    from engine.prediction_engine import parse_houses

    dba_planets = {
        maha_planet,
        bhukti_planet,
        antara_planet
    }

    house5_count = 0
    house9_count = 0

    separative_present = False

    SEPARATIVE_PLANETS = {
        "Sun",
        "Saturn",
        "Rahu",
        "Ketu"
    }

    for row in kp_grid:

        planet = row.get("planet")

        if planet not in dba_planets:
            continue

        houses = set()

        houses.update(
            parse_houses(
                row.get("planet_houses", "")
            )
        )

        houses.update(
            parse_houses(
                row.get("star_houses", "")
            )
        )

        houses.update(
            parse_houses(
                row.get("sub_houses", "")
            )
        )

        if 5 in houses:
            house5_count += 1

        if 9 in houses:
            house9_count += 1

        if planet in SEPARATIVE_PLANETS:
            separative_present = True

    if (
        house5_count >= 2
        and house9_count >= 2
        and separative_present
    ):

        return {
            "event": "JOB_CHANGE",
            "confidence": "HIGH"
        }

    return {
        "event": "NO_JOB_CHANGE",
        "confidence": "LOW"
    }
  