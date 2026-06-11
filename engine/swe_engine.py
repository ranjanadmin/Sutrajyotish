import swisseph as swe
from datetime import datetime
import pytz
from engine.constants import *

# ✅ KP AYANAMSA
swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)

PLANET_MAP = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE
}

def get_jd(dob, tob, tz="Asia/Kolkata"):
    dt = datetime.strptime(dob + " " + tob, "%Y-%m-%d %H:%M")
    local = pytz.timezone(tz).localize(dt)
    utc = local.astimezone(pytz.utc)

    return swe.julday(
        utc.year, utc.month, utc.day,
        utc.hour + utc.minute / 60
    )


def get_planets(jd):
    data = {}

    for p, code in PLANET_MAP.items():
        lon = swe.calc_ut(jd, code, swe.FLG_SIDEREAL)[0][0]
        data[p] = lon

    data["Ketu"] = (data["Rahu"] + 180) % 360
    return data


def get_houses(jd, lat, lon):

    cusps, ascmc = swe.houses_ex(
        jd,
        lat,
        lon,
        b'P',
        swe.FLG_SIDEREAL
    )

    asc = ascmc[0]
    return asc, cusps


def get_sign(lon):
    return SIGNS[int(lon // 30)]


# ✅ FIXED: TRUE KP HOUSE LOGIC
def get_house_from_cusps(lon, cusps):
    for i in range(12):
        start = cusps[i]
        end = cusps[(i + 1) % 12]

        if start < end:
            if start <= lon < end:
                return i + 1
        else:
            if lon >= start or lon < end:
                return i + 1

    return 1


def get_nakshatra(lon):
    size = 360 / 27
    idx = int(lon // size)
    return idx, NAKSHATRA_LORDS[idx]


def get_sub_lord(lon):
    size = 360 / 27
    frac = (lon % size) / size
    sub_idx = int(frac * 9)
    return NAKSHATRA_LORDS[sub_idx]