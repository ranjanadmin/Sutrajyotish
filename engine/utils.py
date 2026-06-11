import requests

OPENCAGE_API_KEY = "YOUR_API_KEY_HERE"


def get_lat_lon_from_place(place):
    try:
        url = "https://api.opencagedata.com/geocode/v1/json"
        params = {
            "q": place,
            "key": OPENCAGE_API_KEY
        }

        res = requests.get(url, params=params).json()

        if res["results"]:
            lat = res["results"][0]["geometry"]["lat"]
            lon = res["results"][0]["geometry"]["lng"]
            return lat, lon

    except Exception as e:
        print("Geocoding error:", e)

    return None, None