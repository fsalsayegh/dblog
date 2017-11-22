from django.http import JsonResponse
from django.shortcuts import render
import requests

def place_text_search(request):
	key= "AIzaSyCS0JKWzwh49JM_6xetUZOTQlQvKlhrLIQ"
	query = "Coded"
	url ="https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&region=kw&key=%s"%(query, key)


	response = requests.get(url)
	context = {"response": response.json()}
	return render(request, "place_search.html", context)
		
	#return JsonResponse(response.json(), safe=False)




