import json

def loadJsonFile(path):
    jsonText = '' 
    try:   
        with open(path, "r") as stable_memory:
            jsonText = stable_memory.read()
            dataBase = json.loads(jsonText)
    except:
        if 'agg' in path:
            dataBase = {}
        else: 
            dataBase = []    
    return dataBase

def saveData(path,sensorMetaData):
    try:
        with open(path, "w+") as stable_memory:
            json.dump(sensorMetaData,stable_memory)
    except:
        pass
    