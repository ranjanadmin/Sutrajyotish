# geocoder.py (FINAL — ROBUST)

import requests


def get_lat_lon_from_place(place):
    """
    Multi-layer geocoder:
    1. OpenStreetMap (Nominatim)
    2. Fallback to manual failure handling
    """

    if not place or len(place.strip()) < 2:
        return None, None, "Invalid place"

    place = place.strip()

    # -------------------------------
    # 🔹 PRIMARY: OpenStreetMap
    # -------------------------------
    try:
        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": place,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "SutraJyotishApp"
        }

        res = requests.get(url, params=params, headers=headers, timeout=5)

        if res.status_code == 200:
            data = res.json()

            if data and len(data) > 0:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return lat, lon, None

    except Exception as e:
        print("OSM Error:", e)

    # -------------------------------
    # ❌ FAILED
    # -------------------------------
    return None, None, "Could not resolve place name"