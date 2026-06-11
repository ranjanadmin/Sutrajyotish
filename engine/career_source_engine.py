def get_career_source(maha, bhukti, antara):

    source = []
    position = []

    dba = [
        str(maha).lower(),
        str(bhukti).lower(),
        str(antara).lower()
    ]

    if "sun" in dba:
        source.append("Government")

    if "moon" in dba:
        source.append("Public")

    if "jupiter" in dba:
        position.append("Leadership")

    if "venus" in dba:
        position.append("Respectable Position")

    return {
        "source": source,
        "position": position
    }