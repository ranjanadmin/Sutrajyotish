from engine.kp_engine import build_kp_grid
from engine.sutra_engine import build_sutra_grid
from engine.dasha_engine import generate_vimshottari_dasha


# ================= NORMALIZE SUTRA =================
def normalize_sutra(sutra):

    for row in sutra:

        for key in ["planet_houses", "star_houses", "sub_houses"]:

            val = row.get(key)

            # ✅ HANDLE STRING → LIST
            if isinstance(val, str):
                row[key] = [
                    int(x.strip())
                    for x in val.split(",")
                    if x.strip().isdigit()
                ]

            # ✅ HANDLE NONE
            elif val is None:
                row[key] = []

    return sutra


# ================= MAIN SERVICE =================
def generate_full_chart(planets, cusps, dt, lagna_chart, bhav_chart, lagna_signs):

    # ---------------- PLANET TABLE ----------------
    planet_table = []

    for p, d in planets.items():
        try:
            planet_table.append({
                "planet": p,
                "degree": round(d.get("longitude", 0), 2),
                "sign": d.get("sign", "")
            })
        except Exception:
            continue

    # ---------------- CUSP TABLE ----------------
    cusp_table = [
        {"house": i + 1, "degree": round(c, 2)}
        for i, c in enumerate(cusps or [])
    ]

    # ---------------- KP GRID ----------------
    try:
        kp_grid = build_kp_grid(planets)
    except Exception as e:
        print("❌ KP GRID ERROR:", e)
        kp_grid = []

    # ---------------- SUTRA GRID ----------------
    try:
        sutra_grid = build_sutra_grid(
            planets,
            lagna_chart,
            bhav_chart,
            lagna_signs
        )

        sutra_grid = normalize_sutra(sutra_grid)

        # ✅ DEBUG HERE (CORRECT PLACE)
        print("🔍 SUTRA GRID:", sutra_grid)

    except Exception as e:
        print("❌ SUTRA GRID ERROR:", e)
        sutra_grid = []

    # ---------------- DASHA ----------------
    try:
        moon_longitude = planets.get("Moon", {}).get("longitude")

        if moon_longitude is not None:
            dasha = generate_vimshottari_dasha(
                moon_longitude,
                dt
            )
        else:
            print("❌ Moon longitude missing")
            dasha = []

    except Exception as e:
        print("❌ DASHA ERROR:", e)
        dasha = []

    # ---------------- RETURN ----------------
    return {
        "lagna_chart": lagna_chart or {},
        "bhav_chart": bhav_chart or {},

        "planets": planet_table,
        "cusps": cusp_table,

        "kp_grid": kp_grid,
        "sutra_grid": sutra_grid,
        "dasha": dasha
    }