import sqlite3
import json
import math
from sqlite3 import Connection

import src.db.dbConst as dbConst
from typing import Dict

def getDefaultEquippedArmorAC(jsonDict: Dict) -> int:
    # presumi che la scheda sia stata compilata correttamente e che l'equip abbia senso
    # Trova in items[] tutti gli oggetti che abbiano armor.value != null (possono essere armature, scudi o altri oggetti che diano bonus alla CA)
    # Trova in questa lista l'armatura (presumiamo sia solo una) e determina: AC base, max Dex, eventuali bonus.
    # Per ciascun altro oggetto nella lista, somma il valore di AC e aggingilo alla formula: Base + min(Dex | max Dex) + magical bonus + other bonuses

    # items.system.attunement = "required"? per tutti gli oggetti che danno AC
    # effects.changes.key = "system.attributes.ac.bonus"
        # effects.changes.value (convertire stringa a int)
    # items.system.type.value = "shield" per gli scudi
    #
    for each in Dict['items']:
        attunementRequirement: str(each['system']['attunement'])
    # TEST: RETURN 1
    return 1

def getUnarmoredMonkAC(jsonDict: Dict) -> int:
    dexMod = int(math.floor((jsonDict['system']['abilities']['dex']['value'] - 10) / 2))
    wisMod = int(math.floor((jsonDict['system']['abilities']['wis']['value'] - 10) / 2))
    return 10 + dexMod + wisMod

def getUnarmoredBarbarianAC(jsonDict: Dict) -> int:
    dexMod = int(math.floor((jsonDict['system']['abilities']['dex']['value'] - 10) / 2))
    conMod = int(math.floor((jsonDict['system']['abilities']['con']['value'] - 10) / 2))
    return 10 + dexMod + conMod

def getUnarmoredBardAC(jsonDict: Dict) -> int:
    dexMod = int(math.floor((jsonDict['system']['abilities']['dex']['value'] - 10) / 2))
    chaMod = int(math.floor((jsonDict['system']['abilities']['cha']['value'] - 10) / 2))
    return 10 + dexMod + chaMod

def getMageArmorDraconicResilienceAC(jsonDict: Dict) -> int:
    dexMod = int(math.floor((jsonDict['system']['abilities']['dex']['value'] - 10) / 2))
    return 13 + dexMod

    
class Actor:

    sqlFields: str = "NAME, DESCRIPTION, ARMORCLASS, HITPOINTS, AVERAGESAVE, TOHITBONUS, SAVEDC, BASEDPR, MAXDPR"

    def __init__(self, id=0, name="Name", description="Description", armorClass=10, hitPoints=10, averageSave=0.0, toHitBonus=0, saveDC=0, baseDPR=0.0, maxDPR=0.0):
        self.id = id
        self.name = name
        self.description = description
        self.armorClass = armorClass
        self.hitPoints = hitPoints
        self.averageSave = averageSave
        self.toHitBonus = toHitBonus
        self.saveDC = saveDC
        self.baseDPR = baseDPR
        self.maxDPR = maxDPR
    
    def fromQuery(actor_id: int):
        try:
            conn: Connection = sqlite3.connect(dbConst.dbPath)
            cur = conn.cursor()

            cur.execute("SELECT " + Actor.sqlFields +  " FROM ACTORS WHERE ID = ?", actor_id)
            row = tuple(cur.fetchone())
            
            if row is None:
                raise ValueError(f"No Actor found with id: {actor_id}.")
            
            name, description, armorClass, hitPoints, averageSave, toHitBonus, saveDC, baseDPR, maxDPR = row

            return Actor(name=name, description=description, armorClass=armorClass, hitPoints=hitPoints, averageSave=averageSave, toHitBonus=toHitBonus, saveDC=saveDC, baseDPR=baseDPR, maxDPR=maxDPR)

        except sqlite3.Error as e:
            raise Exception(f"SQLite error: {e}")
            
        finally:
            if conn:
                conn.close()

    def fromDictionary(data: dict[str, any]):
        name = data.get('name', None)
        description = data.get('description', None)
        armorClass = data.get('armorClass', None)
        hitPoints = data.get('hitPoints', None)
        averageSave = data.get('averageSave', None)
        toHitBonus = data.get('toHitBonus', None)
        saveDC = data.get('saveDC', None)
        baseDPR = data.get('baseDPR', None)
        maxDPR = data.get('maxDPR', None)

        return Actor(name=name, description=description, armorClass=armorClass, hitPoints=hitPoints, averageSave=averageSave, toHitBonus=toHitBonus, saveDC=saveDC, baseDPR=baseDPR, maxDPR=maxDPR)

    def insertActorDirect(self) -> None:

        try:
            with sqlite3.connect(dbConst.dbPath) as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO ACTORS ( " + Actor.sqlFields + " ) VALUES (?,?,?,?,?,?,?,?,?)", (self.name, self.description, self.armorClass, self.hitPoints, self.averageSave, self.toHitBonus, self.saveDC, self.baseDPR, self.maxDPR))
                
        except sqlite3.Error as e:
            raise Exception(f"SQLite error: {e}")
            
    def updateActorDirect(self, id: int):
        try:
            conn = sqlite3.connect(dbConst.dbPath)
            cur = conn.cursor()

            cur.execute('''UPDATE ACTORS SET 
                        NAME = ?, DESCRIPTION = ?, ARMORCLASS = ?, HITPOINTS = ?, AVERAGESAVE = ?, TOHITBONUS = ?, SAVEDC = ?, BASEDPR = ?, MAXDPR = ? 
                        WHERE ID = ?''',
                         (self.name, self.description, self.armorClass, self.hitPoints, self.averageSave, self.toHitBonus, self.saveDC, self.baseDPR, self.maxDPR, id))

            conn.commit()
        
        except sqlite3.Error as e:
            raise Exception(f"SQLite error: {e}")
            
        finally:
            if conn:
                conn.close()

    def fromJsonFile(jsonFilePath: str):
        try:
            with open(jsonFilePath, "r") as file:
                actorJsonDict = json.load(file)

        except Exception as e:
            print(f"si è verificato un errore durante l'import del file Json.")
    
    def mapJsonDict(jsonDict: Dict) -> Dict:
        pass

    def getArmorClass(jsonDict: Dict) -> int:
        jsonFlatAc: int = jsonDict["system"]["attributes"]["ac"]["flat"]
        if jsonFlatAc != None:
            return jsonFlatAc
        
        
        jsonAcCalc: str = jsonDict["system"]["attributes"]["ac"]["calc"]
        match jsonAcCalc:
            case "unarmoredBard":
                return getUnarmoredBardAC(jsonDict)
            case "unarmoredMonk":
                return getUnarmoredMonkAC(jsonDict)
            case "unarmoredBarbarian":
                return getUnarmoredBarbarianAC(jsonDict)
            case "mage" | "draconic":
                return getMageArmorDraconicResilienceAC(jsonDict)
            case _:
                return getDefaultEquippedArmorAC(jsonDict)
                


            
