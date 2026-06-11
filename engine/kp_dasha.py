# KP Nakshatra + Sub-lord + Vimshottari Dasha

NAK_SIZE = 13.333333333333334  # 13°20'

# KP sequence (repeats every 9 nakshatras)
NAK_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury"
]

# Vimshottari years
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

DASHA_ORDER = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]


def normalize_deg(d):
    return d % 360.0


def get_nakshatra(deg):
    d = normalize_deg(deg)
    nak_index = int(d // NAK_SIZE)  # 0..26
    start = nak_index * NAK_SIZE
    end = start + NAK_SIZE
    lord = NAK_LORDS[nak_index % 9]
    return {
        "index": nak_index + 1,   # 1..27
        "start": start,
        "end": end,
        "lord": lord
    }


def get_sub_lord(deg):
    """
    KP Sub-lord:
    Divide the current Nakshatra into 9 unequal parts
    in Vimshottari proportion, starting from the Nakshatra lord.
    """
    d = normalize_deg(deg)
    nak = get_nakshatra(d)

    span = nak["end"] - nak["start"]
    offset = d - nak["start"]

    # order starting from nak lord
    start_idx = DASHA_ORDER.index(nak["lord"])
    seq = DASHA_ORDER[start_idx:] + DASHA_ORDER[:start_idx]

    total_years = sum(DASHA_YEARS.values())  # 120
    acc = 0.0

    for lord in seq:
        part = span * (DASHA_YEARS[lord] / total_years)
        if acc <= offset < acc + part:
            return lord
        acc += part

    # fallback (edge)
    return seq[-1]


def compute_balance_years(moon_deg):
    """
    Balance of running Mahadasha at birth.
    """
    d = normalize_deg(moon_deg)
    nak = get_nakshatra(d)

    span = nak["end"] - nak["start"]
    remaining = nak["end"] - d
    frac = remaining / span

    lord = nak["lord"]
    years_total = DASHA_YEARS[lord]
    balance = years_total * frac

    return {
        "lord": lord,
        "balance_years": round(balance, 3)
    }


def build_dasha_sequence(start_lord, balance_years, years_ahead=120):
    """
    Simple forward Mahadasha sequence from birth.
    """
    seq = []
    order = DASHA_ORDER

    idx = order.index(start_lord)
    t = 0.0

    # first (balance)
    seq.append({
        "lord": start_lord,
        "years": round(balance_years, 3)
    })
    t += balance_years

    i = 1
    while t < years_ahead:
        lord = order[(idx + i) % 9]
        yrs = DASHA_YEARS[lord]
        seq.append({
            "lord": lord,
            "years": yrs
        })
        t += yrs
        i += 1

    return seq


def analyze_kp_layers(planet_positions):
    """
    Returns:
    - nakshatra (star lord)
    - sub-lord
    - Moon-based dasha
    """
    kp_planets = {}

    for p, info in planet_positions.items():
        deg = info["degree"]

        nak = get_nakshatra(deg)
        sub = get_sub_lord(deg)

        kp_planets[p] = {
            "degree": round(deg, 6),
            "nakshatra_lord": nak["lord"],
            "sub_lord": sub
        }

    # Moon-based dasha
    moon_deg = planet_positions["Moon"]["degree"]
    balance = compute_balance_years(moon_deg)

    dasha_seq = build_dasha_sequence(
        balance["lord"],
        balance["balance_years"]
    )

    return {
        "planet_kp": kp_planets,
        "dasha": {
            "starting_lord": balance["lord"],
            "balance_years": balance["balance_years"],
            "sequence": dasha_seq
        }
    }