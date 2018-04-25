import requests
import json
import googlemaps

from datetime import datetime


gmaps = googlemaps.Client(key='AIzaSyCVsFWhJzGfxcs1vr98chFN0w5dcSPh_Tc')

url = "http://localhost:8003/usermgmt/user"



querystring = {"username" : "admin"}



#response = requests.request("GET", url, params=querystring)



now = datetime.now()
directions_result = gmaps.distance_matrix("Vancouver, BC, Canada|Annapolis, MD, USA",
                                     "San Francisco, California, USA|Victoria, BC, Canada")

#print directions_result

#results = json.dumps(directions_result)
rows = directions_result["rows"]

for row in rows:
	#print row["elements"][0]['distance']['value']
	for element in row["elements"]:
		#print element['distance']['value']
		print element

#print json.dumps(directions_result)
