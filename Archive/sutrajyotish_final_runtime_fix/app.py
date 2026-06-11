from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect
)

from datetime import (
    datetime,
    timedelta
)

import pytz

from geopy.geocoders import Nominatim

from engine.transit_engine import (
    generate_transit_data
)

from engine.charts import (
    generate_charts,
    build_horary_chart
)

app = Flask(__name__)

app.secret_key = "sutrajyotish_kp_secret_2026"

geolocator = Nominatim(
    user_agent="sutrajyotish"
)

# -------------------------------
# LMT CORRECTION
# -------------------------------

def apply_lmt(dt_naive, lon):

    try:

        lon = float(lon)

        IST_REF = 82.5

        diff_deg = lon - IST_REF

        diff_minutes = diff_deg * 4

        return dt_naive - timedelta(
            minutes=diff_minutes
        )

    except Exception as e:

        print("LMT Error:", e)

        return dt_naive


# -------------------------------
# GEOCODER
# -------------------------------

def get_lat_lon_from_place(place):

    if not place or len(place.strip()) < 2:

        return None, None

    try:

        location = geolocator.geocode(place)

        if location:

            return (

                float(location.latitude),

                float(location.longitude)
            )

    except Exception as e:

        print("Geocode error:", e)

    return None, None


# -------------------------------
# HOME
# -------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/sutracard")
def sutracard():

    return render_template(
        "sutracard.html"
    )


@app.route("/numerology")
def numerology():

    return render_template(
        "numerology.html"
    )


# -------------------------------
# WORKSPACE
# -------------------------------

@app.route("/workspace")
def workspace():

    if not session.get(
        "workspace_ready"
    ):

        return redirect("/")

    return render_template(
        "workspace.html"
    )

@app.route("/workspace_data")
def workspace_data():

    return jsonify({

    "birth_datetime":
        session.get(
            "birth_datetime",
            ""
        ),

    "latitude":
        session.get(
            "latitude",
            ""
        ),

    "longitude":
        session.get(
            "longitude",
            ""
        ),

    "sidereal_time":
        session.get(
            "sidereal_time",
            ""
        ),

    "transit_chart":
        session.get(
            "transit_chart",
            {}
        ),


        "natal_chart":
        session.get(
            "natal_chart",
            {}
        ),
      "bhav_chart":
      session.get(
        "bhav_chart",
        {}
    ),
    
    "natal_table":
        session.get(
            "natal_table",
            []
        ),
        
  "kp_grid":
        session.get(
            "kp_grid",
            []
        ),

    "running_dasa":
        session.get(
            "running_dasa",
            ""
        ),

    "asc_ruling":
        session.get(
            "asc_ruling",
            ""
        ),

    "moon_ruling":
        session.get(
            "moon_ruling",
            ""
        ),

    "day_lord":
        session.get(
            "day_lord",
            ""
        ),
        
    "running_dasa":
    session.get(
        "running_dasa",
        ""
    ),    
    })
    


# -------------------------------
# GENERATE
# -------------------------------

@app.route(
    "/generate",
    methods=["POST"]
)
def generate():

    try:

        mode = request.form.get(
            "mode",
            "natal"
        )

        # -------------------------------
        # NATAL MODE
        # -------------------------------

        if mode == "natal":

            dob = request.form.get(
                "dob",
                ""
            )

            tob = request.form.get(
                "tob",
                ""
            )

            place = request.form.get(
                "place",
                ""
            )

            lat = request.form.get(
                "lat",
                ""
            )

            lon = request.form.get(
                "lon",
                ""
            )

            if lat and lon:

                lat = float(lat)

                lon = float(lon)

            else:

                if place:

                    geo_lat, geo_lon = (

                        get_lat_lon_from_place(
                            place
                        )
                    )

                    if geo_lat and geo_lon:

                        lat = geo_lat

                        lon = geo_lon

                    else:

                        raise ValueError(
                            "Unable to detect location"
                        )

                else:

                    raise ValueError(
                        "Please enter either Place or Lat/Lon"
                    )

            timezone = request.form.get(
                "timezone"
            )

            if not timezone:

                timezone = "Asia/Kolkata"

          
            result = generate_charts(

                dob,
                tob,
                lat,
                lon,
                timezone
            )
            
            print("RESULT KEYS:", result.keys())

            print("LAGNA:", result.get("lagna_chart"))

            print("BHAV:", result.get("bhav_chart"))

            current_dasa = result.get(
                "current_dasa",
                {}
            )

            if isinstance(current_dasa, dict):

                session["running_dasa"] = " ".join([

                    str(
                        current_dasa.get(
                            "maha",
                            ""
                        )
                    ),

                    str(
                        current_dasa.get(
                            "antar",
                            ""
                        )
                    ),

                    str(
                        current_dasa.get(
                            "pratyantar",
                            ""
                        )
                    )

                ]).strip()

            else:

                session["running_dasa"] = str(
                    current_dasa
                )
            
            # -------------------------------
            # SESSION STORAGE
            # -------------------------------
            session["natal_planets"] = (
                result.get(
                    "planets",
                    []
                )
            )

            session["natal_chart"] = (
                result.get(
                    "lagna_chart",
                    {}
                )
            )

            session["natal_table"] = (
                result.get(
                    "planets",
                    []
                )
            )
            session["bhav_chart"] = (
                result.get(
                    "bhav_chart",
                     {}
               )
           )

            session["kp_grid"] = (
               result.get(
                  "kp_grid",
                   []
               )
            )

            session["transit_chart"] = (
                result.get(
                    "lagna_chart",
                    {}
                )
            )

            session["birth_datetime"] = (
                f"{dob} {tob}"
            )

            session["latitude"] = lat

            session["longitude"] = lon

            session["sidereal_time"] = (
                result.get(
                    "sidereal_time",
                    ""
                )
            )

            session["asc_ruling"] = (

                result.get(
                    "asc_ruling"
                )

                or

                result.get(
                    "ascendant_ruling"
                )

                or

                ""

            )

            session["moon_ruling"] = (

                result.get(
                    "moon_ruling"
                )

                or

                result.get(
                    "moon_rp"
                )

                or

                ""

            )

            session["day_lord"] = (

                result.get(
                    "day_lord"
                )

                or

                ""

            )

            session["workspace_ready"] = True

            # -------------------------------
            # RESTORE ORIGINAL UI
            # -------------------------------

            return render_template(

                "index.html",

                lat=lat,
                lon=lon,

                planets=result.get(
                    "planets",
                    []
                ),

                cusps=result.get(
                    "cusps",
                    []
                ),

                kp_grid=result.get(
                    "kp_grid",
                    []
                ),

                lagna_chart=result.get(
                    "lagna_chart",
                    {}
                ),

                bhav_chart=result.get(
                    "bhav_chart",
                    {}
                ),

                dasa_tree=result.get(
                    "dasa_tree",
                    []
                ),

                vimshottari_rows=result.get(
                    "vimshottari_rows",
                    []
                ),

                kp_249=result.get(
                    "kp_249",
                    []
                ),

                asc_sign=result.get(
                    "asc_sign",
                    ""
                ),

                asc_degree=result.get(
                    "asc_degree",
                    0
                ),

                horary_result=result.get(
                    "horary_result"
                )
            )

        # -------------------------------
        # HORARY MODE
        # -------------------------------

        else:

            question = request.form.get(
                "question",
                ""
            )

            number = int(

                request.form.get(
                    "horary_number",
                    1
                )
            )

            place = request.form.get(
                "horary_place",
                ""
            )

            geo_lat, geo_lon = (

                get_lat_lon_from_place(
                    place
                )
            )

            if geo_lat is None:

                raise ValueError(
                    "Unable to detect place"
                )

            lat = geo_lat

            lon = geo_lon

            horary_timezone = request.form.get(
                "horary_timezone"
            )

            if not horary_timezone:

                horary_timezone = (
                    "Asia/Kolkata"
                )

            horary_dob = request.form.get(
                "horary_dob"
            )

            horary_time = request.form.get(
                "horary_time"
            )

            LOCAL_TZ = pytz.timezone(
                horary_timezone
            )

            dt_local = datetime.strptime(

                f"{horary_dob} {horary_time}",

                "%d-%m-%Y %H:%M"
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

            result = build_horary_chart(

                number,
                dt_utc,
                lat,
                lon
            )

            result["horary_result"] = {

                "question":
                    question,

                "number":
                    number,

                "sign":
                    result["asc_sign"],

                "degree":
                    result["asc_degree"]
            }

            return render_template(

                "index.html",

                horary_result=
                    result.get(
                        "horary_result"
                    ),

                lagna_chart=result.get(
                    "lagna_chart",
                    {}
                ),

                bhav_chart=result.get(
                    "bhav_chart",
                    {}
                ),

                kp_grid=result.get(
                    "kp_grid",
                    []
                ),

                planets=result.get(
                    "planets",
                    []
                ),

                cusps=result.get(
                    "cusps",
                    []
                ),

                kp_249=result.get(
                    "kp_249",
                    []
                ),

                asc_sign=result.get(
                    "asc_sign",
                    ""
                ),

                asc_degree=result.get(
                    "asc_degree",
                    0
                )
            )

    except Exception as e:

        import traceback

        traceback.print_exc()

        return render_template(

            "index.html",

            error=str(e)
        )


# -------------------------------
# KP HORARY
# -------------------------------

@app.route(
    "/horary",
    methods=["POST"]
)
def horary():

    try:

        question = request.form[
            "question"
        ]

        number = int(

            request.form[
                "horary_number"
            ]
        )

        place = request.form.get(
            "place",
            ""
        )

        lat, lon = (

            get_lat_lon_from_place(
                place
            )
        )

        if lat is None or lon is None:

            raise ValueError(
                "Unable to detect place"
            )

        IST = pytz.timezone(
            "Asia/Kolkata"
        )

        now_ist = datetime.now(IST)

        dt_utc = now_ist.astimezone(
            pytz.utc
        )

        dt_utc = dt_utc.replace(
            tzinfo=None
        )

        result = build_horary_chart(

            number,
            dt_utc,
            lat,
            lon
        )

        horary_result = {

            "question":
                question,

            "number":
                number,

            "degree":
                result["asc_degree"],

            "sign":
                result["asc_sign"]
        }

        return render_template(

            "index.html",

            horary_result=
                horary_result,

            lagna_chart=result[
                "lagna_chart"
            ],

            bhav_chart=result[
                "bhav_chart"
            ],

            kp_grid=result[
                "kp_grid"
            ],

            planets=result[
                "planets"
            ],

            cusps=result[
                "cusps"
            ],

            kp_249=result[
                "kp_249"
            ],

            asc_sign=result[
                "asc_sign"
            ],

            asc_degree=result[
                "asc_degree"
            ]
        )

    except Exception as e:

        import traceback

        traceback.print_exc()

        return render_template(

            "index.html",

            error=str(e)
        )


# --------------------------------
# TRANSIT API
# --------------------------------

@app.route(
    "/transit_api",
    methods=["POST"]
)
def transit_api():

    try:

        data = request.json

        print(
            "TRANSIT REQUEST:",
            data
        )

        lat = float(
            data.get("lat")
        )

        lon = float(
            data.get("lon")
        )

        timezone = data.get(

            "timezone",

            "Asia/Kolkata"
        )

        dt_str = data.get(
            "datetime"
        )

        LOCAL_TZ = pytz.timezone(
            timezone
        )

        dt_local = datetime.strptime(

            dt_str,

            "%Y-%m-%d %H:%M:%S"
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

        result = generate_transit_data(

            dt_utc,
            lat,
            lon,

            session.get(
                "natal_planets",
                []
            )
        )

        session["transit_chart"] = (
            result.get(
                "transit_chart",
                {}
            )
        )

        print(
            "TRANSIT RESULT:",
            result
        )

        return jsonify(result)

    except Exception as e:

        import traceback

        traceback.print_exc()

        return jsonify({

            "error":
                str(e)
        })


# --------------------------------
# RECTIFICATION API
# --------------------------------

@app.route(
    "/rectification_api",
    methods=["POST"]
)
def rectification_api():

    try:

        data = request.json

        dt = datetime.strptime(

            data["datetime"],

            "%Y-%m-%d %H:%M:%S"
        )

        lat = float(
            data["lat"]
        )

        lon = float(
            data["lon"]
        )

        result = generate_transit_data(

            dt,
            lat,
            lon,

            session.get(
                "natal_planets",
                []
            )
        )

        return jsonify(result)

    except Exception as e:

        print(
            "RECTIFICATION ERROR:",
            e
        )

        return jsonify({

            "error":
                str(e)
        })


# -------------------------------
# HEALTH
# -------------------------------

@app.route("/health")
def health():

    return jsonify({

        "status":
            "ok"
    })


# -------------------------------
# RUN
# -------------------------------

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000
    )
