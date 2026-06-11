def normalize_degree(deg):
    """Ensure degree is within 0–360"""
    if deg is None:
        return None
    return deg % 360


def get_house_from_lon(lon, cusps):
    """
    Find house based on cusp boundaries (KP / Placidus safe)
    """

    # ---------------- SAFETY ----------------
    if lon is None or not cusps or len(cusps) < 12:
        return None

    lon = normalize_degree(lon)
    cusps = [normalize_degree(c) for c in cusps]

    # ---------------- CORE LOGIC ----------------
    for i in range(12):
        start = cusps[i]
        end = cusps[(i + 1) % 12]

        # Normal case
        if start <= end:
            if start <= lon < end:
                return i + 1

        # Wrap case (e.g., 350 → 10)
        else:
            if lon >= start or lon < end:
                return i + 1

    # ---------------- FALLBACK ----------------
    return 1