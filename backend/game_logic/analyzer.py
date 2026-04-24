TRAITS = {
    "Yasuo": ["Duelist"],
    "Ahri": ["Sorcerer"],
    "Jinx": ["Gunner"],
    "Lux": ["Mage"],
    "Warwick": ["Bruiser"],
    "Nasus": ["Shurima"]
}

def analyze_board(state):
    trait_count = {}

    for champ in state.get("board", []):
        name = champ.get("name")
        traits = TRAITS.get(name, [])

        for t in traits:
            trait_count[t] = trait_count.get(t, 0) + 1

    main_trait = None
    if trait_count:
        main_trait = max(trait_count, key=trait_count.get)

    return {
        "traits": trait_count,
        "main_trait": main_trait
    }


def suggest_playstyle(state):
    level = state.get("level", 0)
    gold = state.get("gold", 0)

    if gold >= 50:
        return "Nên eco, giữ tiền để lấy lợi tức"
    elif level < 6:
        return "Nên up level sớm"
    elif gold < 20:
        return "Không nên roll nhiều, giữ tiền"
    else:
        return "Có thể roll nhẹ để mạnh hơn"