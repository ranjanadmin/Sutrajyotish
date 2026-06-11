# ============================================
# RAHU / KETU SIGNIFICATOR ENGINE
# ============================================

def get_node_significators(
    node_name,
    node_house,
    node_sign,
    planet_houses_map,
    sign_lord_map,
    aspects_map=None,
    conjunction_map=None
):
    """
    Node rules:
    1. Bhav placement
    2. Sign lord houses
    3. Aspect + conjunction planets
    """

    houses = set()

    # 1. placement
    if node_house:
        houses.add(node_house)

    # 2. sign lord
    sign_lord = sign_lord_map.get(node_sign)
    if sign_lord:
        houses.update(planet_houses_map.get(sign_lord, []))

    # 3. conjunction
    if conjunction_map and node_name in conjunction_map:
        for p in conjunction_map[node_name]:
            houses.update(planet_houses_map.get(p, []))

    # 4. aspects
    if aspects_map and node_name in aspects_map:
        for p in aspects_map[node_name]:
            houses.update(planet_houses_map.get(p, []))

    return sorted(houses)