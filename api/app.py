from fastapi import FastAPI, Request
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
import re
import requests
import datetime
import pydantic
import motor.motor_asyncio
import pytz

app = FastAPI()


origins = [
    "https://simple-smart-hub-client.netlify.app",
    "http://127.0.0.1:8000",
    "https://gw-ecse3038-iot-project.onrender.com"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://gawaynewright10:RFOWLlQnLSfSYZ9x@cluster0.mzrx4mq.mongodb.net/")
db = client.iot_platform
Sensor_Data = db['Sensor_Data']
data = db['data']



# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")

location = geolocator.geocode("Hyderabad")


def get_sunset():
    latitude =  location.latitude
    longitude = location.longitude

    sunset_api_url = f'https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}'

    sunset_api_response = requests.get(sunset_api_url)
    sunset_api_data = sunset_api_response.json()

    sunset_time = datetime.datetime.strptime(sunset_api_data['results']['sunset'], '%I:%M:%S %p').time()
    
    return datetime.datetime.strptime(str(sunset_time),"%H:%M:%S")





regex = re.compile(r'((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')

def parse_time(time_str):
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)



@app.get("/")
async def home():
    return {"message": "ECSE3038 - Project"}


@app.get('/graph')
async def graph(request: Request):
    size = int(request.query_params.get('size'))
    values = await data.find().sort('_id', -1).limit(size).to_list(size)
    data_values = []
    for items in values:
        temperature = items.get("temperature")
        presence = items.get("presence")
        current_time = items.get("current_time")

        data_values.append({
            "temperature": temperature,
            "presence": presence,
            "datetime": current_time
        })

    return data_values


@app.put('/settings')
async def get_Sensor_Data(request: Request):
    status = await request.json()
    #final_sunset_time = str(get_sunset())
    user_temp = status["user_temp"]
    user_light = status["user_light"]
    light_time_off = status["light_duration"]
    

    if user_light == "sunset":
        user_light_idle = get_sunset()
    else:
        user_light_scr = datetime.datetime.strptime(user_light, "%H:%M:%S")
    
    new_user_light = user_light_idle + parse_time(light_time_off)

    output = {
        "user_temp": user_temp,
        "user_light": str(user_light_scr.time()),
        "light_time_off": str(new_user_light.time())
        }
    

    obj = await Sensor_Data.find().sort('_id', -1).limit(1).to_list(1)

    if obj:
        await Sensor_Data.update_one({"_id": obj[0]["_id"]}, {"$set": output})
        new_obj = await Sensor_Data.find_one({"_id": obj[0]["_id"]})
    else:
        new = await Sensor_Data.insert_one(output)
        new_obj = await Sensor_Data.find_one({"_id": new.inserted_id})
    return new_obj



@app.post("/parameters")
async def publisher(request: Request): 
    disposition = await request.json()

    criterion = await Sensor_Data.find().sort('_id', -1).limit(1).to_list(1)
    if criterion:
        temperature = criterion[0]["user_temp"]   
        user_light = datetime.strptime(criterion[0]["user_light"], "%H:%M:%S")
        time_off = datetime.strptime(criterion[0]["light_time_off"], "%H:%M:%S")
    else:
        temperature = 28
        user_light = datetime.strptime("18:00:00", "%H:%M:%S")
        time_off = datetime.strptime("20:00:00", "%H:%M:%S")


    now_time = datetime.datetime.now(pytz.timezone('Jamaica')).time()
    current_time = datetime.datetime.strptime(str(now_time),"%H:%M:%S.%f")


    disposition["light"] = ((current_time < user_light) and (current_time < time_off ) & (disposition["presence"] == 1 ))
    disposition["fan"] = ((float(disposition["temperature"]) >= temperature) & (disposition["presence"]==1))
    disposition["current_time"]= str(datetime.datetime.now())

    new_settings = await data.insert_one(disposition)
    new_obj = await data.find_one({"_id":new_settings.inserted_id}) 
    return new_obj



@app.get("/state")
async def get_state():
    final_entry = await data.find().sort('_id', -1).limit(1).to_list(1)

    if not final_entry:
        return {
            "presence": False,
            "fan": False,
            "light": False,
            "current_time": datetime.datetime.now()
        }

    return final_entry
