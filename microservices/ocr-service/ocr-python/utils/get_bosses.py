import json


def current_boss_by_level(level):
    with open('./ocr-python/data/current_raid_boss.json', encoding="utf-8") as crb:
        bosses_raids_level = json.load(crb)
        for bosses_id in bosses_raids_level:
            if bosses_id['Level'] == str(level):
                dex_id = bosses_id['DexID']

    return dex_id


def current_boss_names_by_id(bosses):
    boss_names = []
    with open('./ocr-python/data/pokedex.json', encoding="utf-8") as pokedex:
        pokemons = json.load(pokedex)
        for pokemon_info in pokemons:
            for boss_id in bosses:
                if pokemon_info['id'] == boss_id:
                    boss_names.append(pokemon_info['name'])

    return boss_names
