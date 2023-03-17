from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import logging
#from pyDes import *
import base64
logger = logging.getLogger(__name__)

class WeatherMachine(object):
    def __init__(self):
      self.client_id = '3765fee16e4122e2b9a03cba6bc828e6'

    # def decrypt_url(self,url):
    #   des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0",pad=None, padmode=PAD_PKCS5)
    #   enc_url = base64.b64decode(url.strip())
    #   dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
    #   return dec_url
    
    def fetchWeather(self,location):
        try:
          # req = requests.get('https://www.jiosaavn.com/api.php?__call=autocomplete.get&_marker=0&query='+song+'&ctx=android&_format=json&_marker=0')
          # resonse = req.json()
          # songs_data = resonse['songs']['data']
          geo = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={location}&appid=3765fee16e4122e2b9a03cba6bc828e6")
          geo_location = geo.json()
          
          if geo_location != []:
            place = geo_location[0]['name']
            lat = geo_location[0]['lat']
            lon = geo_location[0]['lon']
            print(place,lat,lon)

            try:
              req = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&APPID=3765fee16e4122e2b9a03cba6bc828e6")
              response = req.json()
              main = response['weather'][0]['main']
              description = response['weather'][0]['description']
              temp = round(response['main']['temp'] - 273.15,2)
              feels_like = round(response['main']['feels_like'] - 273.15,2)
              country = response['sys']['country']
              return {'country':country, 'main':main,'description':description,'temp':temp,'feels_like':feels_like}

            except:
              return "cannot fetch the weather at the moment"
          # if songs_data != []:
          #   song_id = songs_data[0]['id']
          #   title = songs_data[0]['title']
          #   data = requests.get('https://www.jiosaavn.com/api.php?__call=song.getDetails&cc=in&_marker=0%3F_marker%3D0&_format=json&pids='+song_id)
          #   data = data.json()
          #   encrypted_url = data[song_id]['encrypted_media_url']
          #   return {'url':self.decrypt_url(encrypted_url),'title':title}
          
          else:
            # client = soundcloud.Client(client_id=self.client_id)
            # tracks = client.get('/tracks', q=song,limit=1)
            # stream_url = client.get(tracks[0].stream_url, allow_redirects=False)
            # return {'url':stream_url.location,'title':tracks[0].title}
            return "please try again"
            
        except:
          return {'country':'','main':'','description':'','temp':'','feels_like':''}

class ActionFetchWeather(Action):

       def name(self) -> Text:
         return "action_weather"

       def run(self, dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
           location = tracker.get_slot('location')
           if location is not None:
             machine = WeatherMachine()
             data = machine.fetchWeather(location)
             print(data)
             #if data=='please try again':
             if type(data)==str:
               dispatcher.utter_message(data)
             
             elif data['main'] is not '':
               dispatcher.utter_message(f"The weather in {location} is {data['description']}. The temperature is {data['temp']} but feels like {data['feels_like']}")
               #dispatcher.utter_custom_json({"main":'audio',"url":data['url'],'title':data['title']})
             else:
               dispatcher.utter_message(f"I couldn't find the weather in {location}.")
           else:
             dispatcher.utter_message("What weather should I fetch?")
        
           return []
