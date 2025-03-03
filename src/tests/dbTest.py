import math

from src.entities.actors.actor import Actor
import json
from pathlib import Path

actorDictionary = {
    "id": 0,
    "name": 'TestName',
    "description": 'TestDesc',
    "armorClass": 10,
    "hitPoints": 10,
    "averageSave": 0.0,
    "toHitBonus": 0,
    "saveDC": 0,
    "baseDPR": 0.0,
    "maxDpr": 0.0
}

##test = Actor.fromDictionary(actorDictionary)
##Actor.insertActorDirect(test)

##print(test.name)
root = Path(__file__).parent.parent
data_path = root/'resources/playercharacters/ACTest/fvtt-Actor-actestdefault_equippedarmor-0QfxTPkPy7AAdang.json'
with open(data_path) as file:
    json_data = json.load(file)

    result = int(10)
    dexMod = int(math.floor((json_data['system']['abilities']['dex']['value'] - 10) / 2))

    for each in json_data['items']:
        attunement_required = str(each['system']['attunement'])
        attuned = bool(each['system']['attuned'])
        equipped = bool(each['system']['equipped'])
        dexcap = each['system']['armor']['dex']
        base_armor = int(each['system']['armor']['value'])
        bonus_armor = each['system']['armor']['magicalBonus']

        if bonus_armor is None:
            bonus_armor = int(0)

        armor_type = str(each['system']['type']['value'])

        armor_types_list = ['light', 'medium', 'heavy']

        if (attunement_required == 'required') & (attuned == False):
            continue

        if armor_types_list.__contains__(armor_type):
            if dexcap is not None:
                result = base_armor + min(dexMod, dexcap) + bonus_armor
        else:
            result += base_armor + bonus_armor


    print(result)

    ##print(Actor.getArmorClass(json_data))