from os import scandir
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


def testSingleFile():
    global data_path, file, json_data, result
    data_path = root / 'resources/playercharacters/ACTest/fvtt-Actor-actestbard-5pRcYzainoOCcrrx.json'
    with open(data_path) as file:
        json_data = json.load(file)

        result = Actor.getArmorClass(json_data)

        print(result)


def testDirectory():
    global file, json_data, result
    directory = root / 'resources/playercharacters/ACTest'
    for entry in scandir(directory):
        if entry.is_file() & entry.name.endswith('.json'):
            with open(entry) as file:
                json_data = json.load(file)

                result = Actor.getArmorClass(json_data)

                print(f'{json_data["name"]}, {json_data["system"]["attributes"]["ac"]["calc"]}:  {result}')


testDirectory()

