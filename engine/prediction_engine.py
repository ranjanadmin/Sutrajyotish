from engine.career_rules import (
    CAREER_SUCCESS_RULES,
    CAREER_FAILURE_RULES,
    SPECIAL_EVENTS
)

PLANET_WEIGHT = 1
STAR_WEIGHT = 2
SUB_WEIGHT = 3
VERY_POSITIVE = "VERY_POSITIVE"
POSITIVE = "POSITIVE"
POSITIVE_WITH_STRUGGLE = "POSITIVE_WITH_STRUGGLE"
NEUTRAL = "NEUTRAL"
NEGATIVE = "NEGATIVE"
VERY_NEGATIVE = "VERY_NEGATIVE"

def evaluate_houses(houses):

    houses = set(houses)

    best_score = 0
    best_event = ""

    for combo, data in CAREER_SUCCESS_RULES.items():

        if combo.issubset(houses):

            if data["score"] > best_score:

                best_score = data["score"]
                best_event = data["event"]

    for combo, data in CAREER_FAILURE_RULES.items():

        if combo.issubset(houses):

            if abs(data["score"]) > abs(best_score):

                best_score = data["score"]
                best_event = data["event"]

    return best_score, best_event


def score_row(row):

    planet_houses = parse_houses(
        row.get(
            "planet_houses",
            ""
        )
    )

    star_houses = parse_houses(
        row.get(
            "star_houses",
            ""
        )
    )

    sub_houses = parse_houses(
        row.get(
            "sub_houses",
            ""
        )
    )
    planet_set = set(planet_houses)
    star_set = set(star_houses)
    sub_set = set(sub_houses)

    houses = set()
    houses.update(planet_houses)
    houses.update(star_houses)
    houses.update(sub_houses)

    positive = 0
    negative = 0
    p_score, p_event = evaluate_houses(
        planet_houses
    )

    s_score, s_event = evaluate_houses(
        star_houses
    )

    sub_score, sub_event = evaluate_houses(
        sub_houses
    )

    planet_weight = 1
    star_weight = 2
    sub_weight = 3

    # Nakshatra and Sub-Lord oppose each other

    if (
        (s_score > 0 and sub_score < 0)
        or
        (s_score < 0 and sub_score > 0)
    ):
        star_weight = 2
        sub_weight = 2

    total = (
        p_score * planet_weight
        + s_score * star_weight
        + sub_score * sub_weight
    )

    # ----------------------------------
    # Vertical Adverse Override
    # ----------------------------------

    if (
        12 in planet_set and
        8 in star_set and
        6 in sub_set
    ):
        total -= 300

    if (
        8 in planet_set and
        12 in star_set and
        6 in sub_set
    ):
        total -= 300

    if (
        6 in planet_set and
        8 in star_set and
        12 in sub_set
    ):
        total -= 300

    print(
        row["planet"],
        planet_houses,
        star_houses,
        sub_houses,
        total
    )
    events = []

    if p_event:
        events.append(p_event)

    if s_event:
        events.append(s_event)

    if sub_event:
        events.append(sub_event)

    return {
        "planet": row["planet"],
        "score": total,
        "events": list(set(events)),
        "event": sub_event,
        "planet_event": p_event,
        "star_event": s_event,
        "sub_event": sub_event
    }

def parse_houses(value):

    if not value:
        return []

    return [

        int(x.strip())

        for x in str(value).split(",")

        if x.strip().isdigit()
    ]
def classify_planet_strength(
    positive_score,
    negative_score
):

    net = positive_score - negative_score

    if net >= 200:
        return VERY_POSITIVE

    if net >= 100:
        return POSITIVE

    if net > 0:
        return POSITIVE_WITH_STRUGGLE

    if net == 0:
        return NEUTRAL

    if net > -100:
        return NEGATIVE

    return VERY_NEGATIVE

def get_planet_score(
    kp_grid,
    planet_name
):

    for row in kp_grid:

        if row.get("planet") != planet_name:
            continue

        planet_houses = parse_houses(
            row.get("planet_houses", "")
        )

        star_houses = parse_houses(
            row.get("star_houses", "")
        )

        sub_houses = parse_houses(
            row.get("sub_houses", "")
        )

        planet_set = set(planet_houses)
        star_set = set(star_houses)
        sub_set = set(sub_houses)

        houses = set()
        houses.update(planet_houses)
        houses.update(star_houses)
        houses.update(sub_houses)

        positive = 0
        negative = 0

        # Soft Launch Rules

        if {8, 11}.issubset(houses):
            positive += 80

        if {2, 8, 11}.issubset(houses):
            positive += 100

        if (
            12 in planet_set and
            10 in star_set and
            6 in sub_set
        ):
            positive += 80

        if (
            12 in planet_set and
            10 in star_set and
            11 in sub_set
        ):
            positive += 100

        if (
            8 in planet_set and
            10 in star_set and
            11 in sub_set
        ):
            positive += 120

        if (
            8 in planet_set and
            11 in star_set and
            10 in sub_set
        ):
            positive += 120

        # Promotion Rules

        if {2, 6, 10, 11}.issubset(houses):
            positive += 150

        if {6, 10, 11}.issubset(houses):
            positive += 150

        if {10, 11}.issubset(houses):
            positive += 150

        if {6, 11}.issubset(houses):
            positive += 150

        # Negative Rules

        if 8 in houses and 12 in houses:
            negative += 150

        if 6 in houses and 12 in houses:
            negative += 120

        if 6 in houses and 8 in houses:
            negative += 100

        if (
            5 in houses and
            8 in houses and
            12 in houses
        ):
            negative += 180

        if (
            6 in houses and
            8 in houses and
            12 in houses
        ):
            negative += 150

        return {
            "score": positive - negative,
            "positive": positive,
            "negative": negative,
            "strength": classify_planet_strength(
                positive,
                negative
            )
        }

    return {
        "score": 0,
        "positive": 0,
        "negative": 0,
        "strength": NEUTRAL
    }      

def predict_career_horary(kp_grid):

    total = 0
    events = []

    for row in kp_grid:

        result = score_row(row)

        total += result["score"]

        for event in result["events"]:
            events.append(event)

    severity = "NEUTRAL"

    if total >= 300:
        severity = "EXTREME_POSITIVE"

    elif total >= 200:
        severity = "MAJOR_POSITIVE"

    elif total >= 100:
        severity = "POSITIVE"

    elif total <= -300:
        severity = "EXTREME_NEGATIVE"

    elif total <= -200:
        severity = "MAJOR_NEGATIVE"

    elif total <= -100:
        severity = "NEGATIVE"

    career_mode = "SERVICE"

    POSITIVE_EVENTS = {
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

    NEGATIVE_EVENTS = {
        "ADVERSE_WORK_ENVIRONMENT",
        "STRESSED_SERVICE",
        "VALUE_DESTRUCTION",
        "RESIGNATION",
        "TERMINATION"
    }

    positive_hits = 0
    negative_hits = 0

    for event in set(events):

        if event in POSITIVE_EVENTS:
            positive_hits += 1

        if event in NEGATIVE_EVENTS:
            negative_hits += 1

    prediction_summary = []

    if total > 0:

        prediction_summary.append(
            "Career promise exists."
        )

    if "EMPLOYMENT" in events:

        prediction_summary.append(
            "Employment and service-related matters are strongly activated."
        )

    if (
        "INCOME_GAIN" in events
        or "GAIN" in events
        or "EARNINGS" in events
    ):

        prediction_summary.append(
            "Income generation and financial improvement are indicated."
        )

    if (
        "STATUS_AND_RECOGNITION" in events
        or "CAREER_RISE" in events
    ):

        prediction_summary.append(
            "The native is likely to receive support for professional growth, employment opportunities, or career advancement."
        )

    prediction_summary.append(
        "This analysis is a probabilistic astrological assessment and should not be treated as financial, legal, medical, employment, or investment advice."
    )

    return {

        "career_score": total,

        "severity": severity,

        "career_mode": career_mode,

        "prediction_summary": prediction_summary,

        "positive_hits": positive_hits,

        "negative_hits": negative_hits,

        "events": list(set(events)),

        "event_descriptions": get_event_descriptions(
            list(set(events))
        )

    }
def get_event_descriptions(events):

    descriptions = []

    for event in events:

        if event in SPECIAL_EVENTS:

            descriptions.append(
                SPECIAL_EVENTS[event]
            )

    return list(set(descriptions))
    
def get_planet_events(
    kp_grid,
    planet_name
):

    for row in kp_grid:

        if row.get("planet") != planet_name:
            continue

        events = []

        planet_houses = parse_houses(
            row.get("planet_houses", "")
        )

        star_houses = parse_houses(
            row.get("star_houses", "")
        )

        sub_houses = parse_houses(
            row.get("sub_houses", "")
        )

        _, p_event = evaluate_houses(
            planet_houses
        )

        _, s_event = evaluate_houses(
            star_houses
        )

        _, sub_event = evaluate_houses(
            sub_houses
        )

        if p_event:
            events.append(p_event)

        if s_event:
            events.append(s_event)

        if sub_event:
            events.append(sub_event)

        return list(set(events))

    return []   
   
 
