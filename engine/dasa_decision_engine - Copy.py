def classify(score):

    if score >= 80:
        return "GOOD"

    return "BAD"


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
            "income":"INCREASE"
        }

    if md=="BAD" and bd=="GOOD" and ad=="GOOD":

        return {
            "status":"STAGNANT",
            "income":"CONTINUES"
        }

    if md=="GOOD" and bd=="BAD" and ad=="BAD":

        return {
            "status":"PROTECTED",
            "income":"PRESSURE"
        }

    if md=="BAD" and bd=="BAD" and ad=="GOOD":

        return {
            "status":"NO_IMPROVEMENT",
            "income":"TEMP_SUPPORT"
        }

    if md=="GOOD" and bd=="GOOD" and ad=="BAD":

        return {
            "status":"DELAY",
            "income":"PROTECTED"
        }

    return {
        "status":"MIXED",
        "income":"MIXED"
    }