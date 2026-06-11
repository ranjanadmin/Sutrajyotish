from datetime import datetime, timedelta
from engine.constants import *
from engine.swe_engine import get_nakshatra

def generate_dasha(charts):

    moon_lon = charts["planets"]["Moon"]
    _, lord = get_nakshatra(moon_lon)

    start = datetime.now()

    tree = []
    flat = []

    current = lord

    for i in range(9):

        years = DASHA_YEARS[current]
        end = start + timedelta(days=years * 365)

        tree.append({
            "lord": current,
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d")
        })

        flat.append({"lord": current})

        start = end
        keys = list(DASHA_YEARS.keys())
        current = keys[(keys.index(current) + 1) % 9]

    return {
        "dasa_tree": tree,
        "vimshottari_rows": flat
    }