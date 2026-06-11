import swisseph as swe

# ================= SIGNS =================
SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# ================= PLANET MAP =================
PLANET_MAP = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE
}


# ================= SIGN INDEX =================
def get_sign_index(lon):
    lon = lon % 360
    return int(lon // 30) + 1


# ================= MAIN FUNCTION =================
def compute_planets(jd):

    if jd is None:
        return {}

    # ✅ KP AYANAMSA
    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)

    planets = {}

    for name, pid in PLANET_MAP.items():
        try:
            # ✅ SIDEREAL CALCULATION (CRITICAL FIX)
            result = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL)

            lon = result[0][0] % 360

            sign_index = get_sign_index(lon)

            print(f"DEBUG {name}: {lon:.2f}° → {SIGNS[sign_index-1]}")  # debug

            planets[name] = {
                "longitude": lon,
                "sign": sign_index,
                "sign_name": SIGNS[sign_index - 1]
            }

        except Exception as e:
            print(f"⚠️ Planet calc error {name}: {e}")
            continue

    # ✅ KETU
    if "Rahu" in planets:
        try:
            ketu_lon = (planets["Rahu"]["longitude"] + 180) % 360
            ketu_sign = get_sign_index(ketu_lon)

            planets["Ketu"] = {
                "longitude": ketu_lon,
                "sign": ketu_sign,
                "sign_name": SIGNS[ketu_sign - 1]
            }
        except Exception as e:
            print("⚠️ Ketu calc error:", e)

    return planets