import swisseph as swe
from datetime import datetime, timedelta

# -----------------------------
# CONFIG
# -----------------------------
swe.set_ephe_path('.')

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.TRUE_NODE
}

SIGNS = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]

SIGN_LORDS = {
    "Aries":"Mars","Taurus":"Venus","Gemini":"Mercury",
    "Cancer":"Moon","Leo":"Sun","Virgo":"Mercury",
    "Libra":"Venus","Scorpio":"Mars","Sagittarius":"Jupiter",
    "Capricorn":"Saturn","Aquarius":"Saturn","Pisces":"Jupiter"
}

NAKSHATRA_LORDS = [
    "Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"
]*3

# -----------------------------
# HELPERS
# -----------------------------
def get_sign_index(deg):
    deg = deg % 360
    return int(deg // 30)

def get_sign(deg):
    return SIGNS[get_sign_index(deg)]

def get_nakshatra_index(deg):
    return int(deg // (360 / 27))

def get_nakshatra_lord(deg):
    return NAKSHATRA_LORDS[get_nakshatra_index(deg)]

def get_sub_lord(deg):
    # Simple subdivision (stable for now)
    nak_size = 360 / 27
    sub_size = nak_size / 9

    nak_offset = deg % nak_size
    sub_index = int(nak_offset // sub_size)

    return NAKSHATRA_LORDS[sub_index]

def get_house(deg, cusps):
    deg = deg % 360

    for i in range(12):
        start = cusps[i] % 360
        end = cusps[(i + 1) % 12] % 360

        if start < end:
            if start <= deg < end:
                return i + 1
        else:
            if deg >= start or deg < end:
                return i + 1

    return 12

# -----------------------------
# MAIN ENGINE
# -----------------------------
def calculate_all(dob, time, lat, lon):

    print("\n🔹 [REQUEST RECEIVED]")
    print("DOB:", dob, "TIME:", time, "LAT:", lat, "LON:", lon)

    # IST → UTC
    dt = datetime.strptime(f"{dob} {time}", "%Y-%m-%d %H:%M")
    dt_utc = dt - timedelta(hours=5, minutes=30)

    # Julian Day
    jd = swe.julday(
        dt_utc.year,
        dt_utc.month,
        dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0
    )

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SIDEREAL | swe.FLG_SWIEPH

    # Houses
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
    asc_deg = ascmc[0]

    print("\n🔹 Ascendant Degree:", round(asc_deg, 4))

    planets = {}
    planet_houses = {}

    # -----------------------------
    # PLANETS
    # -----------------------------
    for name, p_id in PLANETS.items():

        try:
            pos, _ = swe.calc_ut(jd, p_id, flags)

            deg = pos[0] % 360

            sign = get_sign(deg)
            sign_lord = SIGN_LORDS[sign]
            star_lord = get_nakshatra_lord(deg)
            sub_lord = get_sub_lord(deg)

            house = get_house(deg, cusps)

            planets[name] = {
                "degree": deg,
                "sign": sign,
                "sign_lord": sign_lord,
                "star_lord": star_lord,
                "sub_lord": sub_lord
            }

            planet_houses[name] = house

            # 🔥 DEBUG EACH PLANET
            print(f"{name:8} | Deg: {round(deg,2):6} | Sign: {sign:10} | House: {house} | Star: {star_lord} | Sub: {sub_lord}")

        except Exception as e:
            print(f"❌ Error calculating {name}: {e}")

    # -----------------------------
    # KETU
    # -----------------------------
    if "Rahu" in planets:
        rahu_deg = planets["Rahu"]["degree"]
        ketu_deg = (rahu_deg + 180) % 360

        ketu_sign = get_sign(ketu_deg)
        ketu_star = get_nakshatra_lord(ketu_deg)
        ketu_sub = get_sub_lord(ketu_deg)

        planets["Ketu"] = {
            "degree": ketu_deg,
            "sign": ketu_sign,
            "sign_lord": SIGN_LORDS[ketu_sign],
            "star_lord": ketu_star,
            "sub_lord": ketu_sub
        }

        planet_houses["Ketu"] = get_house(ketu_deg, cusps)

        print(f"Ketu     | Deg: {round(ketu_deg,2)} | Sign: {ketu_sign}")

    # -----------------------------
    # 🔥 FINAL DEBUG BLOCK
    # -----------------------------
    print("\n🔹 VERIFICATION CHECK (Virgo Test)")
    for p in ["Mars", "Venus"]:
        if p in planets:
            deg = planets[p]["degree"]
            sign = planets[p]["sign"]
            print(f"{p} → {round(deg,2)}° → {sign}")

    print("\n==============================\n")

    return {
        "ascendant": asc_deg,
        "cusps": list(cusps),
        "planets": planets,
        "planet_houses": planet_houses
    }