from engine.timeline_prediction_engine import (
    build_24_month_timeline
)
from engine.prediction_engine import (
    predict_career_horary,
    get_planet_score
)

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect
)

from flask_cors import CORS
from datetime import (
    datetime,
    timedelta
)


from engine.dasa_decision_engine import (
    evaluate_dba
)

import pytz
import os
import json
import razorpay
import hmac
import hashlib

from geopy.geocoders import Nominatim

from engine.transit_engine import (
    generate_transit_data
)

from engine.charts import (
    generate_charts,
    build_horary_chart
)

from flask_session import Session

app = Flask(__name__)
CORS(app)
# -------------------------------
# RAZORPAY
# -------------------------------

razorpay_client = razorpay.Client(
    auth=(
        os.environ.get(
            "RAZORPAY_KEY_ID"
        ),
        os.environ.get(
            "RAZORPAY_KEY_SECRET"
        )
    )
)
app.secret_key = "sutrajyotish_kp_secret_2026"

# -------------------------------
# SERVER SIDE SESSION
# -------------------------------

SESSION_DIR = os.path.join(
    os.getcwd(),
    "flask_session"
)

os.makedirs(
    SESSION_DIR,
    exist_ok=True
)

app.config["SESSION_TYPE"] = "filesystem"

app.config["SESSION_PERMANENT"] = False

app.config["SESSION_FILE_DIR"] = SESSION_DIR

app.config["SESSION_USE_SIGNER"] = True

app.config["SESSION_KEY_PREFIX"] = "sutra_"

Session(app)

SIGN_LORD_NAME = {
    "Mars":"Mars",
    "Venus":"Venus",
    "Mercury":"Mercury",
    "Moon":"Moon",
    "Sun":"Sun",
    "Jupiter":"Jupiter",
    "Saturn":"Saturn"
}



# -------------------------------
# WORKSPACE CACHE
# -------------------------------


CACHE_DIR = "workspace_cache"
# -------------------------------
# CONSULTATION STORAGE
# -------------------------------

CONSULTATION_DIR = "consultation_data"

os.makedirs(
    CONSULTATION_DIR,
    exist_ok=True
)

CONSULTATION_FILE = os.path.join(
    CONSULTATION_DIR,
    "consultations.json"
)

if not os.path.exists(
    CONSULTATION_FILE
):
    with open(
        CONSULTATION_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump([], f)

os.makedirs(
    CACHE_DIR,
    exist_ok=True
)

def save_workspace_cache(data):

    with open(
        os.path.join(
            CACHE_DIR,
            "natal_workspace.json"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            default=str
        )

def load_workspace_cache():

    path = os.path.join(
        CACHE_DIR,
        "natal_workspace.json"
    )

    if not os.path.exists(path):
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


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

@app.route("/transit_workspace")
def transit_workspace():

    return render_template(
        "transit_workspace.html"
    )
# -------------------------------
# WORKSPACE
# -------------------------------

@app.route("/workspace")
def workspace():

    data = load_workspace_cache()

    if not data:

        return redirect("/")

    return render_template(
        "workspace.html"
    )


@app.route("/horary_workspace")
def horary_workspace():

    data = load_workspace_cache()

    if not data:
        return redirect("/")

    return render_template(
        "horary_workspace.html"
    )


@app.route("/horary_workspace_data")
def horary_workspace_data():

    return jsonify(
        load_workspace_cache()
    )


@app.route("/workspace_data")
def workspace_data():

    data = load_workspace_cache()

    print(
        "WORKSPACE CACHE LOADED:",
        data.keys()
    )

    return jsonify({

        **data,

        "dasa_tree": data.get(
            "dasa_tree",
            []
        ),

        "vimshottari_rows": data.get(
            "vimshottari_rows",
            []
        ),

        "current_dasa": data.get(
            "current_dasa",
            {}
        )
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
            print(
                  "WORKSPACE LAGNA:",
                   result.get("lagna_chart_workspace")
            )

            print("BHAV:", result.get("bhav_chart"))

            current_dasa = result.get(
                "current_dasa",
                {}
            )

            if isinstance(current_dasa, dict):

                session["natal_running_dasa"] = " ".join([

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

                session["natal_running_dasa"] = str(
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

            session["natal_lagna_chart_workspace"] = (
                result.get(
                    "lagna_chart_workspace",
                    {}
                )
            )

            session["natal_table"] = (
                result.get(
                    "planets",
                    []
                )
            )

            session["natal_cusps"] = (
                result.get(
                    "cusps",
                    []
                )
            )

            session["natal_kp249"] = (
                result.get(
                    "kp_249",
                    []
                )
            )
            session["natal_bhav_chart"] = (
                result.get(
                    "bhav_chart",
                     {}
               )
           )

            session["natal_kp_grid"] = (
               result.get(
                  "kp_grid",
                   []
               )
            )

            session["transit_chart"] = (
                result.get(
                    "lagna_chart_workspace",
                    {}
                )
            )

            session["natal_birth_datetime"] = (
                f"{dob} {tob}"
            )

            session["natal_latitude"] = lat

            session["natal_longitude"] = lon

            session["natal_sidereal_time"] = (
                result.get(
                    "sidereal_time",
                    ""
                )
            )

            session["natal_asc_ruling"] = (

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

            session["natal_moon_ruling"] = (

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

            session["natal_day_lord"] = (

                result.get(
                    "day_lord"
                )

                or

                ""

            )

            session["natal_workspace_ready"] = True

            workspace_payload = {

                "birth_datetime":
                    f"{dob} {tob}",

                "latitude": lat,

                "longitude": lon,

                "sidereal_time":
                    result.get(
                        "sidereal_time",
                        ""
                    ),

                "natal_chart":
                    result.get(
                        "lagna_chart",
                        {}
                    ),

                "lagna_chart_workspace":
                    result.get(
                        "lagna_chart_workspace",
                        {}
                    ),

                "bhav_chart":
                    result.get(
                        "bhav_chart",
                        {}
                    ),

                "natal_table":
                    result.get(
                        "planets",
                        []
                    ),

                "cusps":
                    result.get(
                        "cusps",
                        []
                    ),

                "kp_249":
                    result.get(
                        "kp_249",
                        []
                    ),

                "kp_grid":
                    result.get(
                        "kp_grid",
                        []
                    ),

                "running_dasa":
                    session.get(
                        "natal_running_dasa",
                        ""
                    ),

                "current_dasa":
                    result.get(
                        "current_dasa",
                        {}
                    ),

                "asc_ruling":
                    result.get(
                        "asc_ruling",
                        ""
                    ),

                "moon_ruling":
                    result.get(
                        "moon_ruling",
                        ""
                    ),

                "moon_sign_lord":
                    result.get(
                        "moon_sign_lord",
                        ""
                    ),

                "day_lord":
                    result.get(
                        "day_lord",
                        ""
                    ),

                "vimshottari_rows": (

                    result.get(
                        "vimshottari_rows",
                        []
                    )

                ),

                "dasa_tree": (

                    result.get(
                        "dasa_tree",
                        []
                    )

                )
            }

            save_workspace_cache(
                workspace_payload
            )


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

                vimshottari_rows=(

                    result.get(
                        "vimshottari_rows",
                        []
                    )

                    or

                    result.get(
                        "dasa_tree",
                        []
                    )

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

            value = str(
                request.form.get(
                    "horary_number",
                    ""
                )
            ).strip()

            if not value:

                raise ValueError(
                    "Please enter Horary Number (1-249)"
                )

            number = int(value)

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

            # HORARY WORKFLOW ISOLATION
            session["horary_mode"] = True
            session["horary_chart"] = result.get(
                "lagna_chart",
                {}
            )

            session["horary_kp_grid"] = result.get(
                "kp_grid",
                []
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

            # --------------------------------
            # HORARY WORKSPACE CACHE
            # --------------------------------

            horary_payload = {

                "birth_datetime":
                    f"{horary_dob} {horary_time}",

                "latitude": lat,

                "longitude": lon,

                "natal_chart":
                    result.get(
                        "lagna_chart",
                        {}
                    ),

                "lagna_chart_workspace":
                    result.get(
                        "lagna_chart_workspace",
                        {}
                    ),

                "bhav_chart":
                    result.get(
                        "bhav_chart",
                        {}
                    ),

                "natal_table":
                    result.get(
                        "planets",
                        []
                    ),

                "cusps":
                    result.get(
                        "cusps",
                        []
                    ),

                "kp_249":
                    result.get(
                        "kp_249",
                        []
                    ),

                "kp_grid":
                    result.get(
                        "kp_grid",
                        []
                    ),

                "current_dasa":
                    result.get(
                        "current_dasa",
                        {}
                    ),

                "moon_sign_lord":
                    result.get(
                        "moon_sign_lord",
                        ""
                    ),

                "vimshottari_rows":
                    result.get(
                        "vimshottari_rows",
                        []
                    ),

                "dasa_tree":
                    result.get(
                        "dasa_tree",
                        []
                    )
            }

            save_workspace_cache(
                horary_payload
            )

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

        session["transit_datetime"] = dt_str

        if result.get("running_dasa"):

            session["transit_running_dasa"] = (
                result.get(
                    "running_dasa",
                    ""
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

        print(
            "TRANSIT RUNNING DASA:",
            result.get(
                "running_dasa"
            )
        )

        return jsonify({

            "success": True,

            "lagna_chart_workspace":
                result.get(
                    "lagna_chart_workspace",
                    {}
                ),

            "bhav_chart":
                result.get(
                    "bhav_chart",
                    {}
                ),

            "planets":
                result.get(
                    "planets",
                    []
                ),

            "natal_table":
                result.get(
                    "planets",
                    []
                ),

            "cusps":
                result.get(
                    "cusps",
                    []
                ),

            "kp_grid":
                result.get(
                    "kp_grid",
                    []
                ),

            "kp_249":
                result.get(
                    "kp_249",
                    []
                ),

            "running_dasa":
                session.get(
                    "natal_running_dasa",
                    ""
                ),

            "current_dasa":
                result.get(
                    "current_dasa",
                    {}
                ),

            "asc_ruling":
                result.get(
                    "asc_ruling",
                    ""
                ),

            "moon_ruling":
                result.get(
                    "moon_ruling",
                    ""
                ),

            "moon_sign_lord":
                result.get(
                    "moon_sign_lord",
                    ""
                ),

            "day_lord":
                result.get(
                    "day_lord",
                    ""
                ),

            "vimshottari_rows":
                result.get(
                    "vimshottari_rows",
                    []
                ),

            "dasa_tree":
                result.get(
                    "dasa_tree",
                    []
                ),


            "transit_chart":
                result.get(
                    "transit_chart",
                    {}
                ),

            "natal_chart":
                session.get(
                    "lagna_chart_workspace",
                    {}
                ),

            "transit_table":
                result.get(
                    "transit_table",
                    []
                ),

            "natal_table":
                session.get(
                    "natal_table",
                    []
                ),

            "running_dasa":
                result.get(
                    "running_dasa",
                    ""
                )
        })

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
# WORKSPACE TIME SHIFT API
# -------------------------------

@app.route(
    "/workspace_time_adjust",
    methods=["POST"]
)
def workspace_time_adjust():

    try:

        data = request.json

        birth_dt = datetime.strptime(
            data["birth_datetime"],
            "%d-%m-%Y %H:%M"
        )

        seconds = int(
            data.get("seconds", 0)
        )

        updated_dt = (
            birth_dt +
            timedelta(seconds=seconds)
        )

        cache = load_workspace_cache()

        lat = cache.get("latitude")
        lon = cache.get("longitude")

        if lat is None:
            lat = session.get(
                "natal_latitude"
            )

        if lon is None:
            lon = session.get(
                "natal_longitude"
            )

        if lat is None:
            lat = data.get("latitude")

        if lon is None:
            lon = data.get("longitude")

        lat = float(lat or 0)

        lon = float(lon or 0)

        print(
            "WORKSPACE TIME ADJUST:",
            lat,
            lon
        )

        timezone = "Asia/Kolkata"

        result = generate_charts(

            updated_dt.strftime("%d-%m-%Y"),

            updated_dt.strftime("%H:%M"),

            lat,
            lon,
            timezone
        )

        session["natal_birth_datetime"] = (
            updated_dt.strftime(
                "%d-%m-%Y %H:%M"
            )
        )

        session["natal_lagna_chart_workspace"] = (
            result.get(
                "lagna_chart_workspace",
                {}
            )
        )

        session["natal_bhav_chart"] = (
            result.get(
                "bhav_chart",
                {}
            )
        )

        session["natal_kp_grid"] = (
            result.get(
                "kp_grid",
                []
            )
        )

        session["natal_running_dasa"] = (
            str(
                result.get(
                    "current_dasa",
                    {}
                )
            )
        )

        return jsonify({

            "success": True,

            "birth_datetime":
                session["natal_birth_datetime"],

            "lagna_chart_workspace":
                session["natal_lagna_chart_workspace"],

            "bhav_chart":
                session["natal_bhav_chart"],

            "kp_grid":
                session["natal_kp_grid"],

            "current_dasa":
                result.get(
                    "current_dasa",
                    {}
                ),

            "asc_ruling":
                result.get(
                    "asc_ruling",
                    ""
                ),

            "moon_ruling":
                result.get(
                    "moon_ruling",
                    ""
                ),

            "day_lord":
                result.get(
                    "day_lord",
                    ""
                ),

            "vimshottari_rows": (

                result.get(
                    "vimshottari_rows",
                    []
                )

            ),

            "dasa_tree": (

                result.get(
                    "dasa_tree",
                    []
                )

            ),

            "running_dasa":
                " ".join([

                    str(
                        result.get(
                            "current_dasa",
                            {}
                        ).get(
                            "maha",
                            ""
                        )
                    ),

                    str(
                        result.get(
                            "current_dasa",
                            {}
                        ).get(
                            "antar",
                            ""
                        )
                    ),

                    str(
                        result.get(
                            "current_dasa",
                            {}
                        ).get(
                            "pratyantar",
                            ""
                        )
                    )

                ]).strip()
        })

    except Exception as e:

        import traceback

        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        })


# -------------------------------
# RESET WORKFLOW
# -------------------------------

@app.route(
    "/reset_workflow",
    methods=["POST"]
)
def reset_workflow():

    try:

        session.clear()

        import shutil

        if os.path.exists(CACHE_DIR):

            shutil.rmtree(
                CACHE_DIR,
                ignore_errors=True
            )

        os.makedirs(
            CACHE_DIR,
            exist_ok=True
        )

        return jsonify({

            "success": True
        })

    except Exception as e:

        return jsonify({

            "success": False,
            "error": str(e)
        })

@app.route(
    "/api/prediction/career",
    methods=["POST"]
)
def api_prediction_career():

    try:

        data = request.json or {}

        kp_grid = data.get(
            "kp_grid",
            []
        )

        current_dasa = data.get(
            "current_dasa",
            {}
        )

        print("KP GRID SAMPLE:")
        print("=" * 80)
        print("KP GRID")
        print(kp_grid)
        print("=" * 80)

        prediction = predict_career_horary(
            kp_grid
        )
        workspace = load_workspace_cache()

        vimshottari_rows = workspace.get(
           "vimshottari_rows",
            []
        )

        timeline24 = build_24_month_timeline(
          kp_grid,
          vimshottari_rows
       )
      
        maha = current_dasa.get(
            "maha",
            ""
        )

        bhukti = current_dasa.get(
            "antar",
            ""
        )

        antara = current_dasa.get(
            "pratyantar",
            ""
        )

        maha_score = 0
        bhukti_score = 0
        antara_score = 0

        maha_info = {}
        bhukti_info = {}
        antara_info = {}

        try:

            maha_info = get_planet_score(
                kp_grid,
                maha
            )

            bhukti_info = get_planet_score(
                kp_grid,
                bhukti
            )

            antara_info = get_planet_score(
                kp_grid,
                antara
            )

            maha_score = (
                maha_info["score"]
                if isinstance(maha_info, dict)
                else maha_info
            )

            bhukti_score = (
                bhukti_info["score"]
                if isinstance(bhukti_info, dict)
                else bhukti_info
            )

            antara_score = (
                antara_info["score"]
                if isinstance(antara_info, dict)
                else antara_info
            )

        except Exception as e:

            print(
                "DBA scoring error:",
                e
            )

            timeline = evaluate_dba(
            maha_score,
            bhukti_score,
            antara_score
        )

        if (
            prediction["positive_hits"] >
            prediction["negative_hits"]
        ):

            status = "POSITIVE"
            income = "GAIN"

        else:

            status = "MIXED"
            income = "MIXED"

        timeline_text = (
            f"Most likely manifestation window: "
            f"{timeline24.get('best_window', 'Under Analysis')}"
        )
        prediction["prediction_summary"] = (
          prediction.get("prediction_summary", [])
        )

        prediction.update({

            "status": status,

            "income": income,

            "timeline": timeline_text,

            "best_window":
                timeline24.get(
                    "best_window",
                    "Under Analysis"
                ),

            "risk_window":
                timeline24.get(
                    "risk_window",
                    "Under Analysis"
                ),

            "timeline_event":
                timeline24.get(
                    "event",
                    "NONE"
                ),

            "timeline_confidence":
                timeline24.get(
                    "confidence",
                    "LOW"
                ),

            "dba":
                timeline24.get(
                    "dba",
                    ""
                ),

            
            "maha_strength":
                (
                    maha_info.get(
                        "strength",
                        ""
                    )
                    if isinstance(maha_info, dict)
                    else ""
                ),

            "bhukti_strength":
                (
                    bhukti_info.get(
                        "strength",
                        ""
                    )
                    if isinstance(bhukti_info, dict)
                    else ""
                ),

            "antara_strength":
                (
                    antara_info.get(
                        "strength",
                        ""
                    )
                    if isinstance(antara_info, dict)
                    else ""
                )

        })

        return jsonify(
            prediction
        )

    except Exception as e:

        import traceback

        traceback.print_exc()

        return jsonify({
            "error": str(e)
        })
# HEALTH
# -------------------------------

@app.route("/health")
def health():

    return jsonify({

        "status":
            "ok"
    })

@app.route("/palmistry")
def palmistry():

    return render_template(
        "palmistry.html"
    )
    
@app.route(
    "/api/profession_prediction",
    methods=["POST"]
)
def api_profession_prediction():

    try:

        data = request.get_json()

        horary_number = int(
            data.get(
                "horary_number",
                1
            )
        )

        question = data.get(
            "question",
            "PROMOTION"
        )

        # --------------------------------
        # Current Time
        # --------------------------------

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

        # --------------------------------
        # Default Location
        # --------------------------------

        lat = 28.6139
        lon = 77.2090

        # --------------------------------
        # Horary Chart
        # --------------------------------

        chart = build_horary_chart(
            horary_number,
            dt_utc,
            lat,
            lon
        )

        kp_grid = chart.get(
            "kp_grid",
            []
        )

        vimshottari_rows = chart.get(
            "vimshottari_rows",
            []
        )

        # --------------------------------
        # Prediction Engine
        # --------------------------------

        prediction = predict_career_horary(
            kp_grid
        )
        # --------------------------------
        # Question Mapping
        # --------------------------------

        question_text = (
            question or ""
        ).upper()

        question_type = "PROMOTION"

        if "CHANGE" in question_text:

            question_type = "JOB_CHANGE"

        elif (
            "NEW JOB" in question_text
            or
            "EMPLOYMENT" in question_text
        ):

            question_type = "EMPLOYMENT"

        # --------------------------------
        # Timeline Engine
        # --------------------------------

        timeline = build_24_month_timeline(
            kp_grid,
            vimshottari_rows,
            question_type=question_type
        )
        
        career_promise = (
            "Career promise exists. "
            "Employment and service-related matters "
            "are strongly activated."
        )

        current_outlook = (
            "Income generation and financial "
            "improvement are indicated. "
            "The native is likely to receive support "
            "for professional growth, employment "
            "opportunities, or career advancement."
        )

        positive_indicators = (
            f"Career Score: {prediction.get('career_score', 0)}. "
            f"Severity: {prediction.get('severity', 'NEUTRAL')}. "
            f"Career Mode: {prediction.get('career_mode', 'SERVICE')}. "
            f"Positive Factors: {prediction.get('positive_hits', 0)}."
        )

        if prediction.get("negative_hits", 0) == 0:

            challenges = (
                "No major adverse indicators are "
                "currently visible."
            )

        else:

            challenges = (
                f"{prediction.get('negative_hits', 0)} "
                "adverse indicators require "
                "careful monitoring."
            )

        outlook_24_month = (
            f"Best Window: "
            f"{timeline.get('best_window', 'Under Analysis')}"
        )

        return jsonify({

            "success": True,

            "prediction":
                prediction.get(
                    "severity",
                    "NEUTRAL"
                ),

            "career_score":
                prediction.get(
                    "career_score",
                    0
                ),

            "career_mode":
                prediction.get(
                    "career_mode",
                    "SERVICE"
                ),

            "positive_hits":
                prediction.get(
                    "positive_hits",
                    0
                ),

            "negative_hits":
                prediction.get(
                    "negative_hits",
                    0
                ),

            "status":
                (
                    "POSITIVE"
                    if prediction.get(
                        "positive_hits",
                        0
                    )
                    >
                    prediction.get(
                        "negative_hits",
                        0
                    )
                    else "MIXED"
                ),

            "income":
                (
                    "GAIN"
                    if "INCOME_GAIN"
                    in prediction.get(
                        "events",
                        []
                    )
                    else "NORMAL"
                ),

            "best_window":
                timeline.get(
                    "best_window",
                    "Under Analysis"
                ),

            "career_promise":
                career_promise,

            "current_outlook":
                current_outlook,

            "positive_indicators":
                positive_indicators,

            "challenges":
                challenges,

            "outlook_24_month":
                outlook_24_month,

            "summary":
                prediction.get(
                    "prediction_summary",
                    []
                ),

            "events":
                prediction.get(
                    "events",
                    []
                ),

            "event_descriptions":
                prediction.get(
                    "event_descriptions",
                    []
                )

        })
    except Exception as e:

        import traceback

        traceback.print_exc()

        return jsonify({

            "success": False,

            "error": str(e)

        })
if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )