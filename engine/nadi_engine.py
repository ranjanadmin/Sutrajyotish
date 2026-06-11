def apply_nadi_layer(kp, sutra, dasha):

    result = []

    # KP condition
    if "2" in kp["Sun"]["houses"]:
        result.append("Income opportunity active")

    # Risk override
    if "risk" in kp:
        result.append("⚠ Job instability / defamation yoga")

    # Sutra strength
    if sutra["final_strength"] == "HIGH":
        result.append("Strong repetition indicates event materialization")

    # Dasha trigger
    if dasha["mahadasha"] == "Saturn":
        result.append("Karmic phase active")

    return " | ".join(result)