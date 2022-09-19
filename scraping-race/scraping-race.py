import requests
import json

nameFile = "race.json"
incidences = 1
cameras = 1
radars = 1
oilStations = 1
backPoints = 1
parkings = 1

url = "https://mapas.race.es/WebServices/srvRace.asmx/ObtenerDatos?pstrIncidencias=" + \
    str(incidences)+"&pstrCamaras="+str(cameras)+"&pstrRadares="+str(radars) + \
    "&pstrGasolineras="+str(oilStations)+"&pstrPuntosNegros=" + \
    str(backPoints)+"&pstrParking="+str(parkings)

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
incidencesItems = []
camerasItems = []
radarsItems = []
oilStationsItems = []
blackPointsItems = []
parkingsItems = []


def get_object(type, item, id=None, image=None):
    if type == "incidences":
        return {
            "lat": str(item["Latitud"]),
            "lng": str(item["Longitud"]),
            "id": str(id),
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
            "lat": str(item["Latitud"]),
            "lng": str(item["Longitud"]),
            "id": item["Id"],
            "image": image
        }

    if type == "radars" or type == "oilStations" or type == "blackPoints" or type == "parkings":
        return {
            "lat": str(item["Latitud"]),
            "lng": str(item["Longitud"]),
            "id": str(item["Id"]),
        }


if incidences == 1:
    i = 1
    for itemIncidence in jsonRequest["Incidencias"]:
        obj = get_object('incidences', itemIncidence, str(i))
        incidencesItems.append(obj)
        i += 1
    items["incidents"] = incidencesItems

if cameras == 1:
    for itemRadars in jsonRequest["Camaras"]:
        image = "http://infocar.dgt.es/etraffic/data/camaras/" + \
            str(itemRadars['Id'])+".jpg"
        obj = get_object('camera', itemRadars, "", image)
        camerasItems.append(obj)
    items["cameras"] = camerasItems

if radars == 1:
    for itemRadar in jsonRequest["Radares"]:
        obj = get_object('radars', itemRadar)
        radarsItems.append(obj)
    items["radars"] = radarsItems

if oilStations == 1:
    for ItemsOilStation in jsonRequest["Radares"]:
        obj = get_object('oilStations', ItemsOilStation)
        oilStationsItems.append(obj)
    items["oilStations"] = oilStationsItems

if backPoints == 1:
    for itemBlackPoint in jsonRequest["PuntosNegros"]:
        obj = get_object('blackPoints', itemBlackPoint)
        blackPointsItems.append(obj)
    items["blackPoints"] = blackPointsItems

if parkings == 1:
    for itemParking in jsonRequest["Parking"]:
        obj = get_object('parkings', itemParking)
        parkingsItems.append(obj)
    items["parkings"] = parkingsItems

f = open(nameFile, "w")
itemsDumps = json.dumps(items, indent=2)
f.write(itemsDumps)

print('✅ JSON generated')
