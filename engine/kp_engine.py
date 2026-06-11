NAKSHATRA_LORDS = [
"Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"
]

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
def get_star_sub(deg):

    nak = int(deg / (13.3333))
    star_lord = NAKSHATRA_LORDS[nak % 9]

    sub_index = int((deg % 13.3333) / 1.111)
    sub_lord = NAKSHATRA_LORDS[sub_index % 9]

    return star_lord, sub_lord

def build_cusp_table(cusps):

    rows = []

    for idx, deg in enumerate(cusps, start=1):

        sign_index = int(deg / 30)

        sign_name = SIGNS[sign_index]

        sign_deg = deg % 30

        d = int(sign_deg)

        m = int((sign_deg - d) * 60)

        s = int(
            (
                (
                    sign_deg - d
                ) * 60 - m
            ) * 60
        )

        from engine.charts import (
             get_nakshatra,
            get_sub_lord
        )
  
        nak_name, star_lord = get_nakshatra(deg)

        sub_lord = get_sub_lord(
            deg,
            star_lord
       )

        rows.append({

          "house": idx,

         "degree":
             round(
                deg,
                2
            ),

        "sign":
           sign_name,

       "sign_degree":
            f"{d:02d}°{m:02d}'{s:02d}\"",

      # primary fields
      "nakshatra":
          star_lord,

      "sub_lord":
         sub_lord,

    # compatibility fields
    "nak":
        star_lord,

    "sub":
        sub_lord,

    "stl":
        star_lord,

    "sl":
        sub_lord
})

    return rows

def generate_kp_grid(charts):

    kp = {}

    for p, info in charts["planets"].items():

        deg = info["degree"]
        house = charts["planet_houses"][p]

        star_lord, sub_lord = get_star_sub(deg)

        kp[p] = {
            "house": house,
            "star_lord": star_lord,
            "sub_lord": sub_lord
        }

    return kp