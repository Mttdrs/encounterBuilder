import sqlite3
import json
from sqlite3 import Connection
import src.db.dbConst as dbConst
from typing import Dict



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





            
