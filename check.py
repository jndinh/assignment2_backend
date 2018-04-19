import requests
import googlemaps

from datetime import datetime


gmaps = googlemaps.Client(key='AIzaSyCVsFWhJzGfxcs1vr98chFN0w5dcSPh_Tc')

url = "http://localhost:8003/usermgmt/user"



querystring = {"username" : "admin"}



#response = requests.request("GET", url, params=querystring)



now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

print directions_result
