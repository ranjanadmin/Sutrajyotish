# ============================================
# PLANET SIGNIFICATOR ENGINE (ROW-1 ONLY)
# ============================================

def get_planet_significators(planet, bhav_placement, lordship_map):
    """
    Row-1: Planet significators only

    Rules:
    - Placement from Bhav Chalit
    - Ownership from Lagna
    """

    houses = set()

    if bhav_placement:
        houses.add(bhav_placement)

    houses.update(lordship_map.get(planet, []))

    return sorted(houses)