import requests
import json
from keep_alive import keep_alive
from time import sleep
import datetime

loopactive = True

metrics = []
desiredmetrics = ["temperature", "dewpoint", "windDirection", "windSpeed", "windGust", "barometricPressure", "seaLevelPressure", "visibility", "maxTemperatureLast24Hours", "minTemperatureLast24Hours", "precipitationLastHour", "precipitationLast3Hours", "precipitationLast6Hours", "relativeHumidity", "windChill", "heatIndex"]

def getmetrics():

  global metrics
  metrics = []
  
  response = requests.get("https://api.weather.gov/stations/PHNL/observations/latest")

  json_data = json.loads(response.text)
  
  while not json_data["properties"]["temperature"]["value"]:
    print("null; retrying")
    response = requests.get("https://api.weather.gov/stations/PHNL/observations/latest")
    json_data = json.loads(response.text)
    sleep(30)

  metrics.append({"timestamp":json_data["properties"]["timestamp"]})
  metrics.append({"textDescription":json_data["properties"]["textDescription"]})

  for mtr in desiredmetrics:
    metrics.append({mtr:json_data["properties"][mtr]["value"]});
    
  return(metrics)

def program_run():
  sleep(60*(60-datetime.datetime.now().minute))
  while True:
    outputdata = open("weatherdata.txt", "a")
    outputdata.write(json.dumps(getmetrics()) + "\n")
    outputdata.close()
    print("logged")
    sleep(60*60)

keep_alive()
program_run()