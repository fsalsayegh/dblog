from django.http import JsonResponse
from django.shortcuts import render
import requests

def place_text_search(request):
	key= "AIzaSyBGaugK8KUB2-t4QShjpOs_M1B3s2i6MHk" #a key to access google place API services
	query = request.GET.get( "query" , "Coded") #a dynamic way to choose the location of the place you are looking for
	url ="https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&region=kw&key=%s"%(query, key)

	next_page= request.GET.get('nextpage') #get whatever in the nextpage 
	if next_page is not None: #if there is more results of list of places
		url+="&pagetoken"+next_page #add the parameter &pagetoken to the end of the url

	response = requests.get(url) #making a get request to the url
	context={'response':response.json()} #get a response of the request
	return render(request, "place_search.html", context)
	#return JsonResponse(response.json(), safe=False)


def place_detail(request):
	key="AIzaSyBGaugK8KUB2-t4QShjpOs_M1B3s2i6MHk" #a key to access google detail which and it is the same as the place API key
	place_id=request.GET.get('place_id','') #a dynamic way to choose any specific place id

	url = "https://maps.googleapis.com/maps/api/place/details/json?key=%s&placeid=%s"%(key, place_id)
	map_key = "AIzaSyCrqwdrlrwhfGK9mlZPVFoWC7RTq_AmSJ4" #a key to access google map(geolocation key) for the map

	response = requests.get(url)
	context={'response':response.json() , "map": map_key}
	return render(request, 'place_detail.html', context)
	#return JsonResponse(response.json(), safe=False)




