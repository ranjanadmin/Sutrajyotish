from collections import defaultdict

from datetime import (
    datetime,
    timedelta
)

import swisseph as swe
from datetime import datetime
import pytz
from engine.kp_engine import build_cusp_table


# --------------------------------
# KP AYANAMSA MODE
# --------------------------------

swe.set_sid_mode(
    swe.SIDM_KRISHNAMURTI
)
# -------------------------------
# CONFIG
# -------------------------------
SUTRA_OFFSET = {
    "Sun": 0.0,
    "Moon": 0.0,
    "Mars": 0.0,
    "Mercury": 0.0,
    "Jupiter": 0.0,
    "Venus": 0.0,
    "Saturn": 0.0,
    "Rahu": 0.0,
    "Ketu": 0.0,
    "Uranus": 0.0,
    "Neptune": 0.0,
    "Pluto": 0.0
}

SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces"
]

NAK_LORDS = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury"
]

DASA_YEARS = {
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

SIGN_LORDS = {
    1: "Mars",
    2: "Venus",
    3: "Mercury",
    4: "Moon",
    5: "Sun",
    6: "Mercury",
    7: "Venus",
    8: "Mars",
    9: "Jupiter",
    10: "Saturn",
    11: "Saturn",
    12: "Jupiter"
}


MODERN_RULERS = {
    "Uranus": "Capricorn",
    "Neptune": "Pisces",
    "Pluto": "Scorpio"
}


# -------------------------------
# HELPERS
# -------------------------------

def get_jd(dt):

    return swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour +
        dt.minute / 60.0 +
        dt.second / 3600.0
    )


def get_sign_num(longitude):

    return int((longitude % 360) / 30) + 1


def get_sign_name(longitude):

    return SIGNS[
        int((longitude % 360) / 30)
    ]


def decimal_to_dms(deg):

    deg = deg % 30

    d = int(deg)

    minutes = (
        (deg - d) * 60
    )

    m = int(minutes)

    seconds = (
        (minutes - m) * 60
    )

    s = round(seconds)

    if s == 60:

        s = 0
        m += 1

    if m == 60:

        m = 0
        d += 1

    return (
        f"{d:02d}°"
        f"{m:02d}'"
        f'{s:02d}"'
    )

def get_nakshatra_lord(deg):

    nak_index = int(
        (deg % 360) / (13 + 1/3)
    )

    return NAK_LORDS[nak_index % 9]

# =========================
# NAKSHATRA + KP SUB LORD
# =========================

VIMSOTTARI = {
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

ORDER = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury"
]


def get_nakshatra(lon):
    nakshatras = [
        ("Ashwini", "Ketu"),
        ("Bharani", "Venus"),
        ("Krittika", "Sun"),
        ("Rohini", "Moon"),
        ("Mrigashira", "Mars"),
        ("Ardra", "Rahu"),
        ("Punarvasu", "Jupiter"),
        ("Pushya", "Saturn"),
        ("Ashlesha", "Mercury"),

        ("Magha", "Ketu"),
        ("Purva Phalguni", "Venus"),
        ("Uttara Phalguni", "Sun"),
        ("Hasta", "Moon"),
        ("Chitra", "Mars"),
        ("Swati", "Rahu"),
        ("Vishakha", "Jupiter"),
        ("Anuradha", "Saturn"),
        ("Jyeshtha", "Mercury"),

        ("Mula", "Ketu"),
        ("Purva Ashadha", "Venus"),
        ("Uttara Ashadha", "Sun"),
        ("Shravana", "Moon"),
        ("Dhanishta", "Mars"),
        ("Shatabhisha", "Rahu"),
        ("Purva Bhadrapada", "Jupiter"),
        ("Uttara Bhadrapada", "Saturn"),
        ("Revati", "Mercury"),
    ]

    nak_length = 13 + 20 / 60

    index = int(lon / nak_length)

    return nakshatras[index]


def get_sub_lord(longitude, nak_lord):

    nak_length = 13 + 20 / 60.0

    # exact nakshatra start
    nak_index = int(longitude / nak_length)

    nak_start = nak_index * nak_length

    # precise offset within nakshatra
    offset = longitude - nak_start

    # convert to arc minutes
    offset_arcmin = offset * 60.0

    start_index = ORDER.index(nak_lord)

    sequence = (
        ORDER[start_index:] +
        ORDER[:start_index]
    )

    cumulative = 0.0

    for lord in sequence:

        span = (
            800.0 *
            VIMSOTTARI[lord]
        ) / 120.0

        cumulative += span

        if offset_arcmin <= cumulative:
            return lord

    return sequence[-1]
    
    
# -------------------------------
# ASCENDANT
# -------------------------------

# -------------------------------
# ASCENDANT
# -------------------------------

def compute_ascendant(dt_utc, lat, lon):

    jd = get_jd(dt_utc)

    houses, ascmc = swe.houses_ex(

        jd,
        lat,
        lon,

        b'P',

        swe.FLG_SIDEREAL
    )

    asc_deg = (
        ascmc[0] % 360
    )
   
    asc_deg = (
        asc_deg + 0.97
    ) % 360
    asc_sign = get_sign_num(
        asc_deg
    )

    return asc_sign, asc_deg

# -------------------------------
# CUSPS
# -------------------------------

# -------------------------------
# CUSPS
# -------------------------------

def compute_cusps(dt_utc, lat, lon):

    jd = get_jd(dt_utc)

    houses, _ = swe.houses_ex(

        jd,
        lat,
        lon,

        b'P',

        swe.FLG_SIDEREAL
    )

    return [
       (x + 0.97) % 360
       for x in houses
    ]


# -------------------------------
# PLANETS
# -------------------------------

def compute_planets(dt_utc):

    jd = swe.julday(
        dt_utc.year,
        dt_utc.month,
        dt_utc.day,
        dt_utc.hour +
        dt_utc.minute / 60.0
    )

    planets = {}

    planet_list = {

        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.TRUE_NODE,
        "Uranus": swe.URANUS,
        "Neptune": swe.NEPTUNE,
        "Pluto": swe.PLUTO
    }

    signs = [

        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces"
    ]

    ketu_lon = 0

    for name, pid in planet_list.items():

        result = swe.calc_ut(

            jd,
            pid,

            swe.FLG_SWIEPH |
            swe.FLG_SIDEREAL
        )

        # --------------------------------
        # LONGITUDE
        # --------------------------------

        lon = result[0][0] % 360

        # --------------------------------
        # SPEED / RETROGRADE
        # --------------------------------

        speed = result[0][3]

        retrograde = speed < 0

        # --------------------------------
        # HORASOFT CALIBRATION
        # --------------------------------

        lon = (
            lon + 0.97
        ) % 360

        lon = (

            lon +
            SUTRA_OFFSET.get(name, 0.0)

        ) % 360

        # --------------------------------
        # KETU FROM RAHU
        # --------------------------------

        if name == "Rahu":

            ketu_lon = (
                lon + 180
            ) % 360

        sign_index = int(
            lon / 30
        )

        sign_name = signs[
            sign_index
        ]

        sign_degree = (
            lon % 30
        )

        nak_name, nak_lord = (
            get_nakshatra(lon)
        )

        sub_lord = get_sub_lord(
            lon,
            nak_lord
        )

        house = sign_index + 1

        planets[name] = {

            "longitude": round(
                lon,
                6
            ),

            "long": round(
                lon,
                6
            ),

            "sign": sign_name,

            "sign_name": sign_name,

            "sign_num": (
                sign_index + 1
            ),

            "degree": round(
                lon,
                2
            ),

            "deg": sign_degree,

            "sign_degree": sign_degree,

            "nakshatra": nak_name,

            "nak": nak_name,

            "star_lord": nak_lord,

            "star": nak_lord,

            "sub_lord": sub_lord,

            "sub": sub_lord,

            "house": house,

            # --------------------------------
            # TRANSIT SUPPORT
            # --------------------------------

            "is_retrograde": retrograde,

            "speed": round(
                speed,
                6
            )
        }

    # =========================
    # KETU
    # =========================

    ketu_sign_index = int(
        ketu_lon / 30
    )

    ketu_sign = signs[
        ketu_sign_index
    ]

    ketu_degree = (
        ketu_lon % 30
    )

    ketu_nak, ketu_star = get_nakshatra(
        ketu_lon
    )

    ketu_sub = get_sub_lord(
        ketu_lon,
        ketu_star
    )

    planets["Ketu"] = {

        "longitude": round(
            ketu_lon,
            6
        ),

        "long": round(
            ketu_lon,
            6
        ),

        "sign": ketu_sign,

        "sign_name": ketu_sign,

        "sign_num":
            ketu_sign_index + 1,

        "degree": round(
            ketu_lon,
            2
        ),

        "sign_degree": round(
            ketu_degree,
            2
        ),

        "deg": round(
            ketu_degree,
            2
        ),

        "nakshatra": ketu_nak,

        "nak": ketu_nak,

        "star_lord": ketu_star,

        "star": ketu_star,

        "sub_lord": ketu_sub,

        "sub": ketu_sub,

        "house":
            ketu_sign_index + 1,

        "is_retrograde": True,

        "speed": 0
    }

    return planets
# -------------------------------
# HOUSE HELPERS
# -------------------------------

def get_house_from_sign(sign, asc):

    return ((sign - asc) % 12) + 1


def get_house_from_cusps(lon, cusps):

    lon = lon % 360

    for i in range(12):

        start = cusps[i] % 360

        end = cusps[(i + 1) % 12] % 360

        if start < end:

            if start <= lon < end:
                return i + 1

        else:

            if lon >= start or lon < end:
                return i + 1

    return 1




# -------------------------------
# OUTER PLANET SIGNIFICATIONS
# -------------------------------

def get_outer_planet_significations(
    planet,
    asc_sign,
    cusp_house
):

    houses = set()

    # --------------------------------
    # 1. Occupation from Bhava Chalit
    # --------------------------------
    if planet in cusp_house:
        houses.add(cusp_house[planet])

    # --------------------------------
    # 2. Lordship from Lagna Chart
    # --------------------------------

    for house_num in range(1, 13):

        house_sign_num = (
            (asc_sign + house_num - 2) % 12
        ) + 1

        house_sign = SIGNS[
            house_sign_num - 1
        ]

        # Uranus -> Capricorn
        if (
            planet == "Uranus"
            and house_sign == "Capricorn"
        ):
            houses.add(house_num)

        # Neptune -> Pisces
        elif (
            planet == "Neptune"
            and house_sign == "Pisces"
        ):
            houses.add(house_num)

        # Pluto -> Scorpio
        elif (
            planet == "Pluto"
            and house_sign == "Scorpio"
        ):
            houses.add(house_num)

    return sorted(list(houses))

# -------------------------------
# HOUSE OWNERS
# -------------------------------

def build_house_owners(asc_sign):

    owners = {}

    for house in range(1, 13):

        sign = (
            (asc_sign + house - 2)
            % 12
        ) + 1

        lord = SIGN_LORDS[sign]

        if lord not in owners:
            owners[lord] = []

        owners[lord].append(house)

    return owners


# -------------------------------
# BASIC SIGNIFICATIONS
# -------------------------------

def basic_significations(
    planet,
    cusp_house,
    house_owners
):

    houses = set()

    if planet in cusp_house:
        houses.add(
            cusp_house[planet]
        )

    if planet in house_owners:

        for h in house_owners[planet]:
            houses.add(h)

    return sorted(list(houses))


# -------------------------------
# NODE SIGNIFICATIONS
# -------------------------------

def node_significations(
    node,
    planets,
    sign_house,
    cusp_house,
    house_owners
):

    houses = set()

    node_long = planets[node]["long"]

    node_sign = planets[node]["sign_num"]

    if node in cusp_house:

        houses.add(
            cusp_house[node]
        )

    sign_lord = SIGN_LORDS.get(
        node_sign
    )

    if sign_lord:

        for h in basic_significations(
            sign_lord,
            cusp_house,
            house_owners
        ):
            houses.add(h)

    # conjunctions
    for p, pdata in planets.items():

        if p == node:
            continue

        diff = abs(
            pdata["long"] - node_long
        )

        if diff > 180:
            diff = 360 - diff

        if diff <= 8:

            for h in basic_significations(
                p,
                cusp_house,
                house_owners
            ):
                houses.add(h)

    # Vedic aspects
    for p, pdata in planets.items():

        if p == node:
            continue

        if p in ["Rahu", "Ketu"]:
            continue

        p_house = sign_house[p]

        node_house = sign_house[node]

        diff_house = (
            node_house - p_house
        ) % 12

        aspect = False

        if diff_house == 6:
            aspect = True

        if p == "Mars":

            if diff_house in [3, 7]:
                aspect = True

        elif p == "Jupiter":

            if diff_house in [4, 8]:
                aspect = True

        elif p == "Saturn":

            if diff_house in [2, 9]:
                aspect = True

        if aspect:

            for h in basic_significations(
                p,
                cusp_house,
                house_owners
            ):
                houses.add(h)

    return sorted(
        list(houses)
    )


# -------------------------------
# MASTER SIGNIFICATIONS
# -------------------------------

def get_significations(
    planet,
    planets,
    sign_house,
    cusp_house,
    house_owners,
    asc_sign
):

    if planet in ["Rahu", "Ketu"]:

        return node_significations(
            planet,
            planets,
            sign_house,
            cusp_house,
            house_owners
        )

    if planet in ["Uranus", "Neptune", "Pluto"]:

        return get_outer_planet_significations(
            planet,
            asc_sign,
            cusp_house
        )

    return basic_significations(
        planet,
        cusp_house,
        house_owners
    )


# -------------------------------
# KP GRID
# -------------------------------

def build_kp_grid(
    planets,
    sign_house,
    cusp_house,
    house_owners,
    asc_sign
):
    grid = []

    for p, data in planets.items():

        planet_houses = get_significations(
                    p,
                planets,
                sign_house,
                cusp_house,
                house_owners,
                asc_sign
             )

        star_lord = data["star"]

        sub_lord = data["sub"]

        star_houses = get_significations(
           star_lord,
           planets,
           sign_house,
           cusp_house,
           house_owners,
           asc_sign
        )
        sub_houses = get_significations(
             sub_lord,
             planets,
             sign_house,
             cusp_house,
             house_owners,
             asc_sign
      )

        grid.append({

            "planet": p,

            "planet_houses":
                ",".join(
                    map(str, planet_houses)
                ),

            "star_lord": star_lord,

            "star_houses":
                ",".join(
                    map(str, star_houses)
                ),

            "sub_lord": sub_lord,

            "sub_houses":
                ",".join(
                    map(str, sub_houses)
                )
        })

    return grid

# --------------------------------
# KP 249 SUB LORD TABLE
# --------------------------------

def build_kp_249_table():

    KP_ORDER = [

        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn",
        "Mercury"
    ]

    YEARS = {

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

    table = []

    serial = 1

    nak_length = 13 + 20 / 60.0

    current = 0.0

    for nak_index in range(27):

        nak_lord = KP_ORDER[
            nak_index % 9
        ]

        rotated = (
            KP_ORDER[
                KP_ORDER.index(nak_lord):
            ]
            +
            KP_ORDER[
                :KP_ORDER.index(nak_lord)
            ]
        )

        for sub_lord in rotated:

            sub_span = (

                nak_length *
                YEARS[sub_lord]

            ) / 120.0

            sub_start = current

            sub_end = (
                current + sub_span
            )

            sign_lord = SIGN_LORDS[
                get_sign_num(
                    sub_start
                )
            ]

            table.append({

                "serial": serial,

                "sign_lord": sign_lord,

                "nak_lord": nak_lord,

                "sub_lord": sub_lord,

                "start_dms": decimal_to_dms(
                    sub_start % 30
                ),

                "end_dms": decimal_to_dms(
                    sub_end % 30
                ),

                "start": round(
                    sub_start,
                    6
                ),

                "end": round(
                    sub_end,
                    6
                )
            })

            serial += 1

            current = sub_end

    return table
# -------------------------------
# HORARY DEGREE
# -------------------------------
def get_horary_degree(number):

    table = build_kp_249_table()

    if number < 1 or number > 249:

        raise ValueError(
            "Horary number must be 1-249"
        )

    row = table[
        (number - 1)
        % len(table)
    ]

    degree = (
        row["start"] +
        row["end"]
    ) / 2.0

    return {

        "degree": degree,

        "nak_lord":
            row["nak_lord"],

        "sub_lord":
            row["sub_lord"]
    }
# -------------------------------
# BUILD HORARY CHART
# -------------------------------
def build_horary_chart(
    number,
    dt_utc,
    lat,
    lon
):

    horary = get_horary_degree(
        number
    )

    asc_deg = horary["degree"]

    asc_sign = get_sign_num(
        asc_deg
    )

    planets = compute_planets(
        dt_utc
    )
    # =====================================
    # CUSPS
    # =====================================

    cusps = compute_cusps(
        dt_utc,
        lat,
        lon
    )

    cusp_table = build_cusp_table(
        cusps
    )

    house_owners = build_house_owners(
        asc_sign
    )

    # Override Lagna
    cusps[0] = asc_deg

    lagna = defaultdict(list)

    bhav = defaultdict(list)

    sign_house = {}

    cusp_house = {}

    house_owners = (
        build_house_owners(
            asc_sign
        )
    )

    for p, d in planets.items():

        sign_num = d["sign_num"]

        longitude = d["long"]

        sign_house_num = (
            get_house_from_sign(
                sign_num,
                asc_sign
            )
        )

        cusp_house_num = (
            get_house_from_cusps(
                longitude,
                cusps
            )
        )

        lagna[
            sign_house_num
        ].append(p)

        bhav[
            cusp_house_num
        ].append(p)

        sign_house[p] = (
            sign_house_num
        )

        cusp_house[p] = (
            cusp_house_num
        )

    kp_grid = build_kp_grid(
        planets,
        sign_house,
        cusp_house,
        house_owners,
        asc_sign
      )
        # --------------------------------
    # VIMSHOTTARI DASA
    # --------------------------------

    dasa_tree = build_vimshottari_tree(

        planets,

        dt_utc
    )

    dasa_rows = []

    current_dasa = None

    now = dt_utc

    for maha in dasa_tree:

        for bhukti in maha["bhukti"]:

            for antar in bhukti["antar"]:

                row = {

                    "maha": maha["lord"],

                    "antar": bhukti["lord"],

                    "pratyantar": antar["lord"],

                    "start": antar["start"],

                    "end": antar["end"]
                }

                dasa_rows.append(row)

                if (

                    antar["start"] <= now <= antar["end"]

                ):

                    current_dasa = row
    dasa_tree = build_vimshottari_tree(
        planets,
        dt_utc
    )

    dasa_rows = []

    for maha in dasa_tree:

        maha_lord = maha["lord"]

        for antar in maha["bhukti"]:

            antar_lord = antar["lord"]

            for praty in antar["antar"]:

                praty_lord = praty["lord"]

                dasa_rows.append({

                    "maha": maha_lord,

                    "antar": antar_lord,

                    "pratyantar": praty_lord,

                    "start":
                        praty["start"].strftime(
                            "%d-%m-%Y %H:%M"
                        ),

                    "end":
                        praty["end"].strftime(
                            "%d-%m-%Y %H:%M"
                        )
                })

    return {
        "kp_249": build_kp_249_table(),
        "dasa_tree": dasa_tree,

        "vimshottari_rows": dasa_rows,

        "current_dasa": current_dasa, 
        "lagna_chart":
            build_lagna_chart(
                planets,
                asc_sign
            ),

        "lagna_chart_workspace":
            build_lagna_chart_workspace(
                planets,
                asc_sign
            ),

        "bhav_chart":
            dict(bhav),

        "kp_grid":
            kp_grid,

 "planets": [

    {
        "planet": p,

        "sign":
            planets[p]["sign_name"],

        "degree":
            round(
                planets[p]["long"],
                2
            ),

        "sign_degree":
            decimal_to_dms(
                planets[p]["sign_degree"]
            ),

        "lord":
            SIGN_LORDS.get(
                planets[p]["sign_num"],
                ""
            ),

        "nak":
            planets[p]["nakshatra"],

        "stl":
            planets[p]["star_lord"],

        "sl":
            planets[p]["sub_lord"],

        "ssl": "",

        # Transit compatibility
        "star":
            planets[p]["star_lord"],

        "sub":
            planets[p]["sub_lord"],

        "star_lord":
            planets[p]["star_lord"],

        "sub_lord":
            planets[p]["sub_lord"]
    }

    for p in planets
],

        "cusps": cusp_table,
        

        "asc_sign":
            asc_sign,

        "asc_degree":
            round(
                asc_deg,
                2
            ),

        "moon_sign_lord":
            SIGN_LORDS.get(
                planets["Moon"]["sign_num"],
                ""
            )
    }
#-------------------------------
# VIMSHOTTARI DASA TREE
# -------------------------------

def build_vimshottari_tree(planets, birth_dt):

    order = [
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn",
        "Mercury"
    ]

    years = {
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

    moon_long = planets["Moon"]["longitude"]

    nak_length = 13 + 20 / 60.0

    nak_index = int(
        moon_long / nak_length
    )

    nak_start = (
        nak_index * nak_length
    )

    elapsed_deg = (
        moon_long - nak_start
    )

    remaining_deg = (
        nak_length - elapsed_deg
    )

    moon_star_lord = planets["Moon"]["star_lord"]

    full_years = years[
        moon_star_lord
    ]

    start_index = order.index(
        moon_star_lord
    )

    balance_years = (
        remaining_deg *
        full_years
    ) / nak_length

    # --------------------------------
    # ELAPSED MAHADASA
    # --------------------------------

    elapsed_years = (
        full_years -
        balance_years
    )

    elapsed_days = (
        elapsed_years *
        365.25636
    )

    # --------------------------------
    # TRUE MAHADASA START
    # --------------------------------

    current_start = (
        birth_dt -
        timedelta(days=elapsed_days)
    )

    tree = []

    for i in range(9):

        maha_lord = order[
            (start_index + i) % 9
        ]

        maha_years = years[
            maha_lord
        ]

        if i == 0:

           maha_days = (
               maha_years *
               365.25636
          )
        else:

            maha_days = (
                maha_years *
                365.25636
            )

        maha_start = current_start

        maha_end = (
            maha_start +
            timedelta(days=maha_days)
        )

        bhuktis = []

        maha_index = order.index(
            maha_lord
        )

        for j in range(9):

            bhukti_lord = order[
                (maha_index + j) % 9
            ]

            bhukti_days = (
                maha_days *
                years[bhukti_lord]
            ) / 120.0

            if j == 0:

                bhukti_start = maha_start

            else:

                bhukti_start = (
                    bhuktis[-1]["end"]
                )

            bhukti_end = (
                bhukti_start +
                timedelta(days=bhukti_days)
            )

            antar_list = []

            bhukti_index = order.index(
                bhukti_lord
            )

            for k in range(9):

                antar_lord = order[
                    (bhukti_index + k) % 9
                ]

                antar_days = (
                    bhukti_days *
                    years[antar_lord]
                ) / 120.0

                if k == 0:

                    antar_start = bhukti_start

                else:

                    antar_start = (
                        antar_list[-1]["end"]
                    )

                antar_end = (
                    antar_start +
                    timedelta(days=antar_days)
                )

                antar_list.append({

                    "lord": antar_lord,

                    "start": antar_start,

                    "end": antar_end
                })

            if i == 0:

                filtered_antar = []

                for a in antar_list:

                    if a["end"] >= birth_dt:

                        filtered_antar.append(a)

                antar_list = filtered_antar

            bhuktis.append({

                "lord": bhukti_lord,

                "start": bhukti_start,

                "end": bhukti_end,

                "antar": antar_list
            })

        if i == 0:

            filtered_bhukti = []

            for b in bhuktis:

                if b["end"] >= birth_dt:

                    filtered_bhukti.append(b)

            bhuktis = filtered_bhukti

        tree.append({

            "lord": maha_lord,

            "start": maha_start,

            "end": maha_end,

            "bhukti": bhuktis
        })

        current_start = maha_end

    return tree

# -------------------------------
# BUILD LAGNA CHART GRID
# -------------------------------

def build_lagna_chart(planets, asc_sign):

    layout = [
        [12, 1, 2, 3],
        [11, 0, 0, 4],
        [10, 0, 0, 5],
        [9, 8, 7, 6]
    ]

    sign_boxes = {}

    for sign in range(1, 13):

        sign_boxes[sign] = []

    short_names = {
        "Sun": "Sun",
        "Moon": "Moon",
        "Mars": "Mars",
        "Mercury": "Merc",
        "Jupiter": "Jup",
        "Venus": "Ven",
        "Saturn": "Sat",
        "Rahu": "Rahu",
        "Ketu": "Ketu",
        "Uranus": "Ur",
        "Neptune": "Ne",
        "Pluto": "Pl"
    }

    for pname, pdata in planets.items():

        sign_num = pdata["sign_num"]

        sign_boxes[sign_num].append(
            short_names.get(
                pname,
                pname
            )
        )

    final_grid = []

    for row in layout:

        row_data = []

        for sign in row:

            if sign == 0:

                row_data.append("")
                continue

            text = str(sign)

            if sign_boxes[sign]:

                text += "\n" + "\n".join(
                    sign_boxes[sign]
                )

            row_data.append(text)

        final_grid.append(row_data)

    return final_grid




# -------------------------------
# BUILD WORKSPACE LAGNA CHART
# -------------------------------

def build_lagna_chart_workspace(planets, asc_sign):

    short_names = {
        "Sun": "Sun",
        "Moon": "Moon",
        "Mars": "Mars",
        "Mercury": "Merc",
        "Jupiter": "Jup",
        "Venus": "Ven",
        "Saturn": "Sat",
        "Rahu": "Rahu",
        "Ketu": "Ketu",
        "Uranus": "Ur",
        "Neptune": "Ne",
        "Pluto": "Pl"
    }

    sign_boxes = {}

    for sign in range(1, 13):
        sign_boxes[sign] = []

    for pname, pdata in planets.items():

        sign_num = pdata["sign_num"]

        sign_boxes[sign_num].append(
            short_names.get(pname, pname)
        )

    return sign_boxes


# -------------------------------
# MAIN ENGINE
# -------------------------------
def generate_charts(
     dob,
     tob,
     lat,
     lon,
     timezone
 ):

    dt_local = datetime.strptime(
        f"{dob} {tob}",
          "%d-%m-%Y %H:%M"
    )

    LOCAL_TZ = pytz.timezone(
        timezone
    )

    dt_localized = LOCAL_TZ.localize(
        dt_local
    )

    dt_utc = dt_localized.astimezone(
        pytz.utc
    )

    dt_utc = dt_utc.replace(
        tzinfo=None
    )
    # =====================================
    # PLANETS
    # =====================================

    planets = compute_planets(
        dt_utc
    )

    # =====================================
    # DASA TREE
    # =====================================

    dasa_tree = build_vimshottari_tree(
        planets,
        dt_utc
    )

    # =====================================
    # ASCENDANT
    # =====================================

    asc_sign, asc_deg = compute_ascendant(
        dt_utc,
        lat,
        lon
    )

   
    # =====================================
    # CUSPS
    # =====================================

    cusps = compute_cusps(
        dt_utc,
        lat,
        lon
    )

    cusp_table = build_cusp_table(
        cusps
    )

    house_owners = build_house_owners(
        asc_sign
    )

    lagna = defaultdict(list)

    bhav = defaultdict(list)

    sign_house = {}

    cusp_house = {}

    # =====================================
    # HOUSE MAPPING
    # =====================================

    for p, d in planets.items():

        sign_num = d["sign_num"]

        longitude = d["long"]

        sign_house_num = get_house_from_sign(
            sign_num,
            asc_sign
        )

        cusp_house_num = get_house_from_cusps(
            longitude,
            cusps
        )

        lagna[sign_house_num].append(p)

        bhav[cusp_house_num].append(p)

        sign_house[p] = sign_house_num

        cusp_house[p] = cusp_house_num

    # =====================================
    # KP GRID
    # =====================================

    kp_grid = build_kp_grid(
          planets,
          sign_house,
          cusp_house,
          house_owners,
          asc_sign
    )
    # =====================================
    # DASA ROWS
    # =====================================

    dasa_rows = []

    for maha in dasa_tree:

        maha_lord = maha["lord"]

        for antar in maha["bhukti"]:

            antar_lord = antar["lord"]

            for praty in antar["antar"]:

                praty_lord = praty["lord"]

                dasa_rows.append({

                    "maha": maha_lord,

                    "antar": antar_lord,

                    "pratyantar": praty_lord,

                    "start":
                        praty["start"].strftime(
                            "%d-%m-%Y %H:%M"
                        ),

                    "end":
                        praty["end"].strftime(
                            "%d-%m-%Y %H:%M"
                        )
                })

    # =====================================
    # CURRENT DASA
    # =====================================

    current_dasa = None

    now = datetime.utcnow()

    for maha in dasa_tree:

        for antar in maha["bhukti"]:

            for praty in antar["antar"]:

                if (
                    praty["start"] <= now <= praty["end"]
                ):

                    current_dasa = {

                        "maha": maha["lord"],

                        "antar": antar["lord"],

                        "pratyantar": praty["lord"],

                        "start":
                            praty["start"].strftime(
                                "%d-%m-%Y %H:%M"
                            ),

                        "end":
                            praty["end"].strftime(
                                "%d-%m-%Y %H:%M"
                            )
                    }

    # =====================================
    # FINAL RETURN
    # =====================================

    return {

    "kp_249": build_kp_249_table(),

    "dasa_tree": dasa_tree,

    "vimshottari_rows": dasa_rows,

    "current_dasa": current_dasa or {},

    "lagna_chart":
        build_lagna_chart(
            planets,
            asc_sign
        ),

    "lagna_chart_workspace":
        build_lagna_chart_workspace(
            planets,
            asc_sign
        ),

    "bhav_chart":
        dict(bhav),

    "kp_grid":
        kp_grid,

"planets": [

    {
        "planet": p,

        "sign":
            planets[p]["sign_name"],

        "degree":
            round(
                planets[p]["long"],
                2
            ),

        "sign_degree":
            decimal_to_dms(
                planets[p]["sign_degree"]
            ),

        "lord":
            SIGN_LORDS.get(
                planets[p]["sign_num"],
                ""
            ),

        "nak":
            planets[p]["nakshatra"],

        "stl":
            planets[p]["star_lord"],

        "sl":
            planets[p]["sub_lord"],

        "ssl": "",

        # Transit compatibility
        "star":
            planets[p]["star_lord"],

        "sub":
            planets[p]["sub_lord"],

        "star_lord":
            planets[p]["star_lord"],

        "sub_lord":
            planets[p]["sub_lord"]
    }

    for p in planets
],
    "cusps": cusp_table,

    "asc_sign":
        asc_sign,

    "asc_degree":
        round(
            asc_deg,
            2
        ),

    "asc_ruling":
        SIGN_LORDS.get(
            asc_sign,
            ""
        ),

   "moon_sign_lord":
    SIGN_LORDS.get(
        planets["Moon"]["sign_num"],
        ""
    ),
   
    "moon_ruling":
        planets["Moon"]["star_lord"],

    "day_lord":
        dt_local.strftime("%A")
}