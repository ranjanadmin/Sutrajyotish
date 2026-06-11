# time_utils.py (FINAL)

from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder

tf = TimezoneFinder()


def get_timezone_from_latlon(lat, lon):
    try:
        tz_name = tf.timezone_at(lat=lat, lng=lon)

        if tz_name:
            return pytz.timezone(tz_name)

    except Exception as e:
        print("Timezone error:", e)

    # Fallback to IST
    return pytz.timezone("Asia/Kolkata")


def convert_to_utc(date_str, time_str, lat, lon):
    try:
        # Parse datetime
        dt_local = datetime.strptime(
            f"{date_str} {time_str}",
            "%Y-%m-%d %H:%M"
        )

        # Detect timezone
        tz = get_timezone_from_latlon(lat, lon)

        # Localize (handles DST automatically)
        dt_local = tz.localize(dt_local)

        # Convert to UTC
        dt_utc = dt_local.astimezone(pytz.utc)

        return dt_local, dt_utc, tz

    except Exception as e:
        print("Time conversion error:", e)
        return None, None, None