from engine.career_rules import (
    CAREER_SUCCESS_RULES,
    CAREER_FAILURE_RULES,
    SPECIAL_EVENTS
)

PLANET_WEIGHT = 1
STAR_WEIGHT = 2
SUB_WEIGHT = 3


def parse_houses(value):

    if not value:
        return []

    return [
        int(x.strip())
        for x in str(value).split(",")
        if x.strip().isdigit()
    ]


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

    planet_houses = parse_houses(row.get("planet_houses", ""))
    star_houses = parse_houses(row.get("star_houses", ""))
    sub_houses = parse_houses(row.get("sub_houses", ""))

    p_set = set(planet_houses)
    s_set = set(star_houses)
    sub_set = set(sub_houses)

    combined = p_set | s_set | sub_set

    star_score, _ = evaluate_houses(s_set)
    sub_score_eval, _ = evaluate_houses(sub_set)

    conflict = (
        (star_score > 0 and sub_score_eval < 0)
        or
        (star_score < 0 and sub_score_eval > 0)
    )

    score, event = evaluate_houses(combined)

    if conflict:
        score -= 40

    return {
        "planet": row.get("planet", ""),
        "score": score,
        "event": event,
        "conflict": conflict,
        "strength": (
            len(p_set) * PLANET_WEIGHT
            + len(s_set) * STAR_WEIGHT
            + len(sub_set) * (2 if conflict else SUB_WEIGHT)
        )
    }

def get_planet_score(
    kp_grid,
    planet_name
):

    for row in kp_grid:

        if row["planet"] != planet_name:
            continue

        houses = set()

        houses.update(
            parse_houses(
                row.get(
                    "planet_houses",
                    ""
                )
            )
        )

        houses.update(
            parse_houses(
                row.get(
                    "star_houses",
                    ""
                )
            )
        )

        houses.update(
            parse_houses(
                row.get(
                    "sub_houses",
                    ""
                )
            )
        )

        positive = 0
        negative = 0

        if {2,6,10,11}.issubset(houses):
            positive += 100

        if {6,10,11}.issubset(houses):
            positive += 100

        if {10,11}.issubset(houses):
            positive += 100

        if {6,11}.issubset(houses):
            positive += 100

        if (
            len(
                houses.intersection(
                    {5,8,12}
                )
            ) >= 2
        ):
            negative += 100

        if (
            len(
                houses.intersection(
                    {6,8,12}
                )
            ) >= 2
        ):
            negative += 100

        return positive - negative

    return 0
    
def predict_career_horary(kp_grid):

    total = 0
    events = []

    for row in kp_grid:

        result = score_row(row)

        total += result["score"]

        if result["event"]:
            events.append(result["event"])
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

  return {

    "career_score": total,

    "severity": severity,

    "career_mode": career_mode,

    "positive_hits": positive_hits,

    "negative_hits": negative_hits,

    "events": list(set(events)),

    "event_descriptions":
        get_event_descriptions(
            list(set(events))
        )
}
   
   

def get_event_descriptions(events):

    descriptions = []

    for event in events:

        if event in SPECIAL_EVENTS:
            descriptions.append(SPECIAL_EVENTS[event])

    return list(set(descriptions))
