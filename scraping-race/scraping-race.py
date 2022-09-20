import requests
import json
import pandas as pd

formatData="json" # json / csv
nameFile = "race"
incidents = 1
cameras = 1
radars = 1
oilStations = 1
blackPoints = 1
parkings = 1

url = "https://mapas.race.es/WebServices/srvRace.asmx/ObtenerDatos?pstrIncidencias=" + \
    str(incidents)+"&pstrCamaras="+str(cameras)+"&pstrRadares="+str(radars) + \
    "&pstrGasolineras="+str(oilStations)+"&pstrPuntosNegros=" + \
    str(blackPoints)+"&pstrParking="+str(parkings)

headers = {
    "authority": "infocar.dgt.es",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "host": "mapas.race.es",
    "referer": "https://mapas.race.es/",
}
response = requests.get(url, headers=headers)
initialText = response.text
splitText = response.text.split('<string xmlns="http://tempuri.org/">')
textOk = splitText[1].split("</string>")[0]

jsonRequest = json.loads(textOk)

items = {}
incidentsItems = []
camerasItems = []
radarsItems = []
oilStationsItems = []
blackPointsItems = []
parkingsItems = []


def get_object(type, item, id=None, image=None):
    if type == "incidents":
        return {
            "id": str(id),
            "lat": str(item["Latitud"]),
            "lng": str(item["Longitud"]),
            "type": str(item["Tipo"]),
            "date": item["Fecha"],
            "reason": item["Causa"],
            "level": item["Nivel"],
            "province": item["Provincia"],
            "poblation": item["Poblacion"],
            "street": item["Carretera"]
        }

    if type == "cameras":
        return {
            "id": str(item["Id"]),
            "lat": str(item["Latitud"]),
            "lng": str(item["Longitud"]),
            "image": image
        }

    if type == "radars" or type == "oilStations" or type == "blackPoints" or type == "parkings":
        return {
            "id": str(item["Id"]),
            "lat": str(item["Latitud"]),
            "lng": str(item["Longitud"]),
        }


if incidents == 1:
    i = 1
    for itemIncidence in jsonRequest["Incidencias"]:
        obj = get_object('incidents', itemIncidence, str(i))
        incidentsItems.append(obj)
        i += 1
    items["incidents"] = incidentsItems

if cameras == 1:
    for itemCameras in jsonRequest["Camaras"]:
        image = "http://infocar.dgt.es/etraffic/data/camaras/" + \
            str(itemCameras['Id'])+".jpg"
        obj = get_object('cameras', itemCameras, "", image)
        camerasItems.append(obj)
    items["cameras"] = camerasItems

if radars == 1:
    for itemRadar in jsonRequest["Radares"]:
        obj = get_object('radars', itemRadar)
        radarsItems.append(obj)
    items["radars"] = radarsItems

if oilStations == 1:
    for ItemsOilStation in jsonRequest["Gasolineras"]:
        obj = get_object('oilStations', ItemsOilStation)
        oilStationsItems.append(obj)
    items["oilStations"] = oilStationsItems

if blackPoints == 1:
    for itemBlackPoint in jsonRequest["PuntosNegros"]:
        obj = get_object('blackPoints', itemBlackPoint)
        blackPointsItems.append(obj)
    items["blackPoints"] = blackPointsItems

if parkings == 1:
    for itemParking in jsonRequest["Parking"]:
        obj = get_object('parkings', itemParking)
        parkingsItems.append(obj)
    items["parkings"] = parkingsItems

if formatData == "json":
    f = open(nameFile + '.' + formatData, "w")
    itemsDumps = json.dumps(items, indent=2)
    f.write(itemsDumps)
elif formatData == "csv":
    incidentsDF = pd.DataFrame(items["incidents"])
    camerasDF = pd.DataFrame(items["cameras"])
    radarsDF = pd.DataFrame(items["radars"])
    oilStationsDF = pd.DataFrame(items["oilStations"])
    blackPointsDF = pd.DataFrame(items["blackPoints"])
    parkingsDF = pd.DataFrame(items["parkings"])

    incidentsDF.to_csv(nameFile + "_incidents." + formatData, index=False)
    camerasDF.to_csv(nameFile + "_cameras." + formatData, index=False)
    radarsDF.to_csv(nameFile + "_radars." + formatData, index=False)
    oilStationsDF.to_csv(nameFile + "_oilStations." + formatData)
    blackPointsDF.to_csv(nameFile + "_blackPoints." + formatData, index=False)
    parkingsDF.to_csv(nameFile + "_parkings." + formatData, index=False)

print('✅ '+ formatData +' file/s generated')
