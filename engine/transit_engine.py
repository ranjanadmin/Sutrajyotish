from datetime import datetime
import pytz

from engine.charts import (
    compute_planets,
    compute_cusps,
    compute_ascendant,
    decimal_to_dms,
    get_sign_name,
    get_nakshatra_lord,
    get_sub_lord,
    get_nakshatra
)

# --------------------------------
# TRANSIT ENGINE
# --------------------------------

def generate_transit_data(
    dt_utc,
    lat,
    lon,
    natal_planets
):

    print("GENERATING TRANSIT...")

    # --------------------------------
    # TRANSIT DATA
    # --------------------------------

    planets = compute_planets(
        dt_utc
    )

    cusps = compute_cusps(
        dt_utc,
        lat,
        lon
    )

    asc_data = compute_ascendant(
        dt_utc,
        lat,
        lon
    )

    asc_sign = asc_data[0]
    asc_degree = asc_data[1]

    # --------------------------------
    # TRANSIT TABLE
    # --------------------------------

    transit_planets = []

    transit_table = []

    for p, data in planets.items():

        row = {

            "planet":
                p,

            "sign":
                data.get(
                    "sign_name",
                    ""
                ),

            "degree":
                round(
                    data.get(
                        "long",
                        0
                    ),
                    2
                ),

            "sign_degree":
                decimal_to_dms(
                    data.get(
                        "sign_degree",
                        0
                    )
                ),

            "nak":
                data.get(
                    "star",
                    ""
                ),

            "sub":
                data.get(
                    "sub",
                    ""
                ),

            "lord":
                data.get(
                    "sign_lord",
                    ""
                ),

            "stl":
                data.get(
                    "star_lord",
                    ""
                ),

            "sl":
                data.get(
                    "sub_lord",
                    ""
                ),

            "ssl":
                data.get(
                    "sub_sub_lord",
                    ""
                ),

            "retrograde":
                data.get(
                    "is_retrograde",
                    False
                )
        }

        transit_planets.append(row)

        transit_table.append(row)

    # --------------------------------
    # SIGN MAP
    # --------------------------------

    sign_map = {

        "Aries": 1,
        "Taurus": 2,
        "Gemini": 3,
        "Cancer": 4,
        "Leo": 5,
        "Virgo": 6,
        "Libra": 7,
        "Scorpio": 8,
        "Sagittarius": 9,
        "Capricorn": 10,
        "Aquarius": 11,
        "Pisces": 12
    }

    # --------------------------------
    # NATAL TABLE
    # --------------------------------

    natal_table = []

    natal_chart = {}

    for item in natal_planets:

        p = item["planet"]

        sign_name = item["sign"]

        sign_num = sign_map.get(
            sign_name,
            1
        )

        natal_table.append({

            "planet":
                item["planet"],

            "sign":
                item["sign"],

            "degree":
                item["degree"],

            "sign_degree":
                item["sign_degree"],

            "star":
                item.get(
                  "star",
               item.get(
                 "star_lord",
                  ""
             )
           ),

            "sub":
                item.get(
                  "sub",
               item.get(
                 "sub_lord",
                  ""
               )
            ),

            "retrograde":
                False
        })

        if sign_num not in natal_chart:

            natal_chart[sign_num] = []

        natal_chart[sign_num].append(
            p
        )

    # --------------------------------
    # TRANSIT CHART
    # --------------------------------

    transit_chart = {}

    for p, data in planets.items():

        sign_num = data.get(
            "sign_num",
            1
        )

        if sign_num not in transit_chart:

            transit_chart[sign_num] = []

        label = p

        if data.get("is_retrograde"):

            label += "Ⓡ"

        transit_chart[sign_num].append(
            label
        )

    # --------------------------------
    # CUSPS
    # --------------------------------

    transit_cusps = []

    for i in range(12):

        transit_cusps.append({

            "house":
                i + 1,

            "degree":
                round(
                    cusps[i],
                    2
                ),

            "sign":
                get_sign_name(
                    cusps[i]
                ),

            "sign_degree":
                decimal_to_dms(
                    cusps[i] % 30
                ),

            "nak":
                get_nakshatra_lord(
                    cusps[i]
                ),

            "sub":
                get_sub_lord(
                    cusps[i],
                    get_nakshatra(
                        cusps[i]
                    )[1]
                )
        })

    
    # --------------------------------
    # RUNNING DASA
    # --------------------------------

    def calculate_dynamic_dasa(dt_obj):

        vim_order = [

            "Ket",
            "Ven",
            "Sun",
            "Mon",
            "Mar",
            "Rah",
            "Jup",
            "Sat",
            "Mer"
        ]

        # reference natal datetime
        natal_ref = datetime(
            1972,
            10,
            26,
            0,
            13,
            0
        )

        years_elapsed = (
            dt_obj - natal_ref
        ).days / 365.25

        maha_index = int(
            years_elapsed // 7
        ) % len(vim_order)

        antar_index = int(
            years_elapsed // 2
        ) % len(vim_order)

        praty_index = int(
            years_elapsed * 3
        ) % len(vim_order)

        suk_index = int(
            years_elapsed * 7
        ) % len(vim_order)

        return " ".join([

            vim_order[maha_index],

            vim_order[antar_index],

            vim_order[praty_index],

            vim_order[suk_index]
        ])

    running_dasa = calculate_dynamic_dasa(
        dt_utc
    )


    # --------------------------------
    # SAFE FINAL RETURN
    # --------------------------------

    return {

        "datetime":
            dt_utc.strftime(
                "%d-%m-%Y %H:%M:%S"
            ),

        "asc_sign":
            asc_sign,

        "asc_degree":
            round(
                asc_degree,
                2
            ),

        "planets":
            transit_planets,

        "transit_table":
            transit_table,

        "natal_table":
            natal_table,

        "cusps":
            transit_cusps,

        "transit_chart":
            transit_chart,

        "natal_chart":
            natal_chart,

        "running_dasa":
            running_dasa
    }
