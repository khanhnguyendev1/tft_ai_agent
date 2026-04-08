VALID_CHAMPS = [
    "Aatrox","Ahri","Darius","Swain","Sion","Mel",
    "Kindred","Leblanc","Draven","Ornn","Briar",
    "KogMaw","Yunara","Ngộ Không","Lissandra",
    "Vayne","Nasus","Warwick","Jinx","Ekko","Lux","Yasuo"
]

def clean_game_state(state):
    if not state:
        return None

    cleaned_board = []

    for champ in state.get("board", []):
        name = champ.get("name")

        if name in VALID_CHAMPS:
            cleaned_board.append({"name": name})

    state["board"] = cleaned_board
    return state