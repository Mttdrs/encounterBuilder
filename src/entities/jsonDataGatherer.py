import math
from math import floor

def getEffectBonusAC(each: dict, equipped: bool): ## jsonDict['items']
    if not equipped:
        return 0
    effect_bonus = int(0)
    for effect in each['effects']:
        for change in effect['changes']:
            if change['key'] == str('system.attributes.ac.bonus'):
                effect_bonus += int(change['value'])
    return effect_bonus

def getArmorClass(jsonDict: dict) -> int:
    result = int(0)

    acCalculation: str = str(jsonDict["system"]["attributes"]["ac"]["calc"])

    flatAcCalculations = ['natural', 'flat']
    if flatAcCalculations.__contains__(acCalculation):
        return jsonDict["system"]["attributes"]["ac"]["flat"]

    unarmoredACCalculations = ['unarmoredMonk', 'unarmoredBarb', 'unarmoredBard', 'draconic', 'mage']

    dexMod = int(floor((jsonDict['system']['abilities']['dex']['value'] - 10) / 2))
    wisMod = int(floor((jsonDict['system']['abilities']['wis']['value'] - 10) / 2))
    conMod = int(floor((jsonDict['system']['abilities']['con']['value'] - 10) / 2))
    chaMod = int(floor((jsonDict['system']['abilities']['cha']['value'] - 10) / 2))

    main_armor: int = int(10)
    match acCalculation:
        case "unarmoredMonk":
            main_armor = 10 + wisMod + dexMod
        case "unarmoredBarb":
            main_armor = 10 + conMod + dexMod
        case "unarmoredBard":
            main_armor = 10 + chaMod + dexMod
        case "draconic" | "mage":
            main_armor = 13 + dexMod

    for each in jsonDict['items']:
        attunement_required = str(each['system']['attunement'])
        attuned = bool(each['system']['attuned'])
        equipped = bool(each['system']['equipped'])
        dexcap = each['system']['armor']['dex']
        base_armor = int(each['system']['armor']['value'])
        bonus_armor = each['system']['armor']['magicalBonus']
        effect_bonus = getEffectBonusAC(each, equipped)

        if dexcap is None:
            dexcap = 0

        if bonus_armor is None:
            bonus_armor = int(0)

        armor_type = str(each['system']['type']['value'])
        armor_types_list = ['light', 'medium', 'heavy']
        ## unarmored_types_list = ['clothing','shield']

        if (attunement_required == 'required') & (attuned == False):
            continue

        if not armor_types_list.__contains__(armor_type):  ## Non è un'armatura > scudo o oggetto magico
            result += base_armor + bonus_armor + effect_bonus
        elif not unarmoredACCalculations.__contains__(acCalculation) & armor_types_list.__contains__(armor_type):
            main_armor = base_armor + min(dexMod, dexcap) + bonus_armor + effect_bonus

    return result + main_armor

def getHitPoints(jsonDict: dict) -> float:
    result = float(0)
    conMod = float(floor((jsonDict['system']['abilities']['con']['value'] - 10) / 2))

    levelBonus: float = float(0)
    overallBonus: float = float(0)
    generalHPBonuses = jsonDict['system']['attributes']['hp']['bonuses']
    for key in generalHPBonuses.keys():
        if key == "level":
            levelBonus = float(jsonDict['system']['attributes']['hp']['bonuses']['level'])
        if key == "overall":
            overallBonus = float(jsonDict["system"]["attributes"]["hp"]["bonuses"]['overall'])

    for item in jsonDict["items"]:
        if item["type"] == "class":
            hdSize: float = float(item["system"]["hd"]["denomination"][1:])
            for advancement in item["system"]["advancement"]:
                if advancement["type"] == "HitPoints":
                    for value in advancement["value"].values():
                        result += conMod + levelBonus
                        match value:
                            case "max":
                                result += hdSize
                            case "avg":
                                result += (hdSize/2) + 1
                            case _:
                                result += float(value)

    result += overallBonus
    return result

def getTotalLevel(jsonDict: dict) -> int:
    level: int = int(0)
    ## /system/details
    if jsonDict['type'] == "npc":
        level = int(jsonDict['system']['details']['cr'])

    if jsonDict['type'] == "character":
        for item in jsonDict["items"]:
            if item["type"] == "class":
                level += int(item['system']['levels'])

    return level

def getProfBonus(jsonDict: dict) -> int:
    level: int = getTotalLevel(jsonDict)
    return 2 + (level - 1) // 4

def getSavingThrows(jsonDict: dict) -> dict:
    result: dict = dict({"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0})

    proficiencyBonus = getProfBonus(jsonDict)
    globalSaveBonus: int = int(0)
    abilities: dict = dict(jsonDict['system']['abilities'])

    for item in jsonDict['items']:
        for effect in item['effects']:
            for change in effect['changes']:
                if change['key'] == "system.bonuses.abilities.save":
                    globalSaveBonus += int(change['value'])
                else:
                    for key in result.keys():
                        if change['key'] == "system.abilities."+ key +".bonuses.save":
                            result[key] += int(change['value'])

    for key in abilities.keys():
        abilityMod: int = int(floor((abilities[key]['value'] - 10) / 2))
        result[key] += abilityMod + globalSaveBonus
        if abilities[key]['proficient']:
            result[key] += proficiencyBonus

    return result