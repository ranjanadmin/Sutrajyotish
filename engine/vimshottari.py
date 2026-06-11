# engine/vimshottari.py

from datetime import datetime, timedelta

# Vimshottari order
DASHA_ORDER = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]

# Years
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

NAK_SIZE = 13.3333333333


# -----------------------------
# Helper
# -----------------------------
def get_nakshatra_index(deg):
    return int(deg // NAK_SIZE)


def get_dasha_start(moon_deg):
    nak_index = get_nakshatra_index(moon_deg)
    lord = DASHA_ORDER[nak_index % 9]

    nak_start = nak_index * NAK_SIZE
    balance = (nak_start + NAK_SIZE - moon_deg) / NAK_SIZE

    return lord, balance


# -----------------------------
# Build Mahadasha
# -----------------------------
def build_mahadasha(moon_deg, birth_dt):

    start_lord, balance_frac = get_dasha_start(moon_deg)

    order = DASHA_ORDER
    idx = order.index(start_lord)

    timeline = []

    current_date = birth_dt

    # First (balance)
    years = DASHA_YEARS[start_lord] * balance_frac
    end_date = current_date + timedelta(days=years * 365.25)

    timeline.append({
        "lord": start_lord,
        "start": current_date,
        "end": end_date
    })

    current_date = end_date

    # Remaining full cycles
    for i in range(1, 9):
        lord = order[(idx + i) % 9]
        years = DASHA_YEARS[lord]

        end_date = current_date + timedelta(days=years * 365.25)

        timeline.append({
            "lord": lord,
            "start": current_date,
            "end": end_date
        })

        current_date = end_date

    return timeline


# -----------------------------
# Antar Dasha
# -----------------------------
def build_antar(maha_lord, start, end):

    total_days = (end - start).days

    antar = []
    current = start

    for lord in DASHA_ORDER:
        frac = DASHA_YEARS[lord] / 120
        days = total_days * frac

        next_date = current + timedelta(days=days)

        antar.append({
            "lord": lord,
            "start": current,
            "end": next_date
        })

        current = next_date

    return antar


# -----------------------------
# Main API
# -----------------------------
def generate_vimshottari(moon_deg, birth_dt):

    maha = build_mahadasha(moon_deg, birth_dt)

    # attach antar
    for m in maha:
        m["antar"] = build_antar(m["lord"], m["start"], m["end"])

    return maha