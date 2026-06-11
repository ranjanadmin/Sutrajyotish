
from engine.career_rules import (
    CAREER_SUCCESS_RULES,
    CAREER_FAILURE_RULES,
    SPECIAL_EVENTS
)


PLANET_WEIGHT = 1
STAR_WEIGHT = 2
SUB_WEIGHT = 3


def evaluate_houses(houses):

    houses = set(houses)

    best_score = 0
    best_event = ""

    for combo,data in CAREER_SUCCESS_RULES.items():

        if combo.issubset(houses):

            if data["score"] > best_score:

                best_score = data["score"]
                best_event = data["event"]

    for combo,data in CAREER_FAILURE_RULES.items():

        if combo.issubset(houses):

            if abs(data["score"]) > abs(best_score):

                best_score = data["score"]
                best_event = data["event"]

    return best_score,best_event


def score_row(row):

    planet_houses = row["planet_houses"]
    star_houses = row["star_houses"]
    sub_houses = row["sub_houses"]

    p_score,p_event = evaluate_houses(planet_houses)
    s_score,s_event = evaluate_houses(star_houses)
    sub_score,sub_event = evaluate_houses(sub_houses)

    total = (
        p_score*PLANET_WEIGHT
        +
        s_score*STAR_WEIGHT
        +
        sub_score*SUB_WEIGHT
    )

    return {
        "planet":row["planet"],
        "score":total,
        "planet_event":p_event,
        "star_event":s_event,
        "sub_event":sub_event
    }


def predict_career_horary(kp_grid):

    total = 0
    events = []

    for row in kp_grid:

        result = score_row(row)

        total += result["score"]

        if result["sub_event"]:
            events.append(result["sub_event"])

    return {

        "career_score": total,

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

            descriptions.append(
                SPECIAL_EVENTS[event]
            )

    return list(set(descriptions))


    