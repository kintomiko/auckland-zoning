import requests
from string import Template
import json
import sys
import time

endpoint_loc = Template('''https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?f=json&singleLine=$addr&outFields=*&outSR=102100''')
endpoint_zone = Template('''https://mapspublic.aucklandcouncil.govt.nz/arcgis3/rest/services/NonCouncil/UnitaryPlanZones/MapServer/1/query?f=json&returnGeometry=true&geometry=%7B%22xmin%22%3A$loc_x%2C%22ymin%22%3A$loc_y%2C%22xmax%22%3A$loc_x%2C%22ymax%22%3A$loc_y%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%2C%22latestWkid%22%3A3857%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100''')

def getLoc(data):
    return {"x": data["candidates"][0]["location"]["x"], "y": data["candidates"][0]["location"]["y"]}

def getJson(url):
    return json.loads(requests.get(url).content.decode('utf-8'))

def getAddr(line):
    fields = line.split(",")
    return (fields[2]+" "+fields[3]+" "+fields[4]).replace("\"", "")

with open(sys.argv[1]) as fp:
    fp.readline()
    fp.readline()
    for line in iter(fp.readline, b''):
        addr = getAddr(line)
        start_time = time.time()
        loc_resp = getJson(endpoint_loc.substitute(addr=addr))
        print(time.time() - start_time)
        loc = getLoc(loc_resp)
        start_time = time.time()
        response = getJson(endpoint_zone.substitute(loc_x=loc["x"], loc_y=loc["y"]))
        print(time.time() - start_time)
        print(addr + "," + json.dumps(loc) + "," + json.dumps(response["features"][0]["attributes"]))
