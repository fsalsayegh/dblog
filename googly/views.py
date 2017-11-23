from django.http import JsonResponse
from django.shortcuts import render
import requests

def place_text_search(request):
	key= "AIzaSyBGaugK8KUB2-t4QShjpOs_M1B3s2i6MHk"
	query = request.GET.get( "query" , "Coded")
	url ="https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&region=kw&key=%s"%(query, key)

	next_page= request.GET.get('nextpage')
	if next_page is not None:
		url+="&pagetoken"+next_page
	response = requests.get(url)
	context={'response':response.json()}
	return render(request, "place_search.html", context)
	#return JsonResponse(response.json(), safe=False)


def place_detail(request):
	key="AIzaSyBGaugK8KUB2-t4QShjpOs_M1B3s2i6MHk"
	place_id=request.GET.get('place_id','')

	url = "https://maps.googleapis.com/maps/api/place/details/json?key=%s&placeid=%s"%(key, place_id)
	map_key = "AIzaSyCrqwdrlrwhfGK9mlZPVFoWC7RTq_AmSJ4"

	response = requests.get(url)
	context={'response':response.json() , "map": map_key}
	return render(request, 'place_detail.html', context)




