import swisseph as swe

NAKSHATRA_SIZE = 360.0 / 27.0

NAK_LORDS = [
    "Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury",
    "Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury",
    "Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"
]

DASHA_YEARS = {
    "Ketu":7,"Venus":20,"Sun":6,"Moon":10,
    "Mars":7,"Rahu":18,"Jupiter":16,"Saturn":19,"Mercury":17
}


def get_moon_sidereal_longitude(jd):
    # uses global sid_mode set in app.py
    return swe.calc_ut(jd, swe.MOON)[0][0] % 360


def get_moon_dasha_input(jd):

    moon_lon = get_moon_sidereal_longitude(jd)

    nak_index = int(moon_lon / NAKSHATRA_SIZE)
    if nak_index >= 27:
        nak_index = 26

    lord = NAK_LORDS[nak_index]

    start_deg = nak_index * NAKSHATRA_SIZE
    elapsed = (moon_lon - start_deg) / NAKSHATRA_SIZE

    balance_years = DASHA_YEARS[lord] * (1 - elapsed)

    return {
        "moon_longitude": moon_lon,
        "start_lord": lord,
        "balance_years": balance_years
    }