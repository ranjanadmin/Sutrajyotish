def generate_sutra_grid(charts, kp):

    sutra = {}

    for p, data in kp.items():
        if p == "risk":
            continue

        sutra[p] = {
            "houses": data["houses"],
            "strength": len(data["houses"])
        }

    return sutra