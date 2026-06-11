from datetime import datetime, timedelta

from engine.dasa_decision_engine import (
    evaluate_event_dba,
    evaluate_job_change_dba
)

from engine.prediction_engine import (
    get_planet_events,
    get_planet_score
)


def build_24_month_timeline(
    kp_grid,
    vimshottari_rows,
    score_function=None,
    question_type="PROMOTION"
):

    now = datetime.utcnow()
    future_limit = now + timedelta(days=730)

    timeline = []

    if vimshottari_rows:
        print(
            "VIMSHOTTARI SAMPLE:",
            vimshottari_rows[0]
        )

    for row in vimshottari_rows:

        try:

            start = datetime.strptime(
                row["start"],
                "%d-%m-%Y %H:%M"
            )

            end = datetime.strptime(
                row["end"],
                "%d-%m-%Y %H:%M"
            )

        except Exception:
            continue

        if end < now:
            continue

        if start > future_limit:
            continue

        maha = row.get("maha", "")
        bhukti = row.get("antar", "")
        antara = row.get("pratyantar", "")

        maha_events = get_planet_events(
            kp_grid,
            maha
        )

        bhukti_events = get_planet_events(
            kp_grid,
            bhukti
        )

        antara_events = get_planet_events(
            kp_grid,
            antara
        )

        if question_type == "JOB_CHANGE":

            dba = evaluate_job_change_dba(
                maha,
                bhukti,
                antara,
                kp_grid
            )

        else:

            dba = evaluate_event_dba(
                maha_events,
                bhukti_events,
                antara_events
            )

# ---------------------------------
# Phase-1 DBA Strength Filter
# ---------------------------------

maha_score = get_planet_score(
    kp_grid,
    maha
)["score"]

bhukti_score = get_planet_score(
    kp_grid,
    bhukti
)["score"]

antara_score = get_planet_score(
    kp_grid,
    antara
)["score"]

# Promotion requires positive DBA

dba_total = (
    maha_score +
    bhukti_score +
    antara_score
)

        if (
            dba["confidence"] in ("HIGH", "MEDIUM")
            and
            dba_total > 0
        ):

            timeline.append({

                "start": row["start"],
                "end": row["end"],

                "maha": maha,
                "bhukti": bhukti,
                "antara": antara,

                "event": dba["event"],
                "confidence": dba["confidence"],

                "dba_score": dba_total

            })

    # ----------------------------------
    # AFTER FOR LOOP ENDS
    # ----------------------------------

    if not timeline:

        return {
            "best_window": "No supportive period found in next 24 months",
            "risk_window": "",
            "event": "NO_MANIFESTATION",
            "confidence": "LOW",
            "dba": "",
            "matches": []
        }

    high = [
        x for x in timeline
        if x["confidence"] == "HIGH"
    ]

    first = high[0] if high else timeline[0]

    return {

        "best_window":
            f"{first['start']} to {first['end']}",

        "event":
            first["event"],

        "confidence":
            first["confidence"],

        "dba":
            f"{first['maha']}/{first['bhukti']}/{first['antara']}",

        "matches":
            timeline

    }