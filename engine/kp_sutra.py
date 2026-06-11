# engine/kp_sutra.py

NAK_SIZE = 13.3333333333

NAK_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury"
]

DASHA_ORDER = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]

DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17
}


# -----------------------------
# Nakshatra
# -----------------------------
def get_nakshatra(deg):
    idx = int(deg // NAK_SIZE)
    lord = NAK_LORDS[idx % 9]
    return lord


# -----------------------------
# Sub Lord
# -----------------------------
def get_sub_lord(deg):
    nak_idx = int(deg // NAK_SIZE)
    nak_start = nak_idx * NAK_SIZE
    offset = deg - nak_start

    total = 120
    span = NAK_SIZE

    start_lord = NAK_LORDS[nak_idx % 9]
    start_index = DASHA_ORDER.index(start_lord)

    acc = 0

    for i in range(9):
        lord = DASHA_ORDER[(start_index + i) % 9]
        portion = span * (DASHA_YEARS[lord] / total)

        if acc <= offset < acc + portion:
            return lord

        acc += portion

    return DASHA_ORDER[-1]


# -----------------------------
# Sign Lord Mapping
# -----------------------------
SIGN_LORD = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter"
}


# -----------------------------
# Sutra Grid
# -----------------------------
def generate_sutra_grid(planets, planet_houses):

    grid = {}

    for planet, info in planets.items():

        deg = info["degree"]
        sign = info["sign"]

        nak_lord = get_nakshatra(deg)
        sub_lord = get_sub_lord(deg)
        sign_lord = SIGN_LORD[sign]

        # Houses
        h1 = planet_houses.get(planet)        # own
        h2 = planet_houses.get(nak_lord)      # star lord
        h3 = planet_houses.get(sign_lord)     # sign lord

        houses = sorted(set([h1, h2, h3]))

        grid[planet] = {
            "nakshatra_lord": nak_lord,
            "sub_lord": sub_lord,
            "significator_houses": houses
        }

    return grid