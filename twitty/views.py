from django.shortcuts import render
from urllib.parse import quote
import requests
from django.http import JsonResponse
from allauth.socialaccount.admin import SocialApp
from requests_oauthlib import OAuth1

def tweet_search(request):
	#url="https://api.twitter.com/1.1/search/tweets.json?q=%23freebandnames&since_id=24012619984051000&max_id=250126199840518145&result_type=mixed&count=4"
	search_term = "#python"
	query = quote(search_term)

	url="https://api.twitter.com/1.1/search/tweets.json?q=%s"%(query)

	user = request.user #add the current user name to the variable user
	social_account = user.socialaccount_set.get(user=user.id)#get the specific logged in user from a set of social accounts(twitter or github,...)
	social_token = social_account.socialtoken_set.get(account=social_account.id) #get the token for that social account which is (twitter)

	token = social_token.token #access the token field of that social account
	token_secret = social_token.token_secret#get the token secret from social token

	social_app = SocialApp.objects.get(provider=social_account.provider) #retrieve the socialApp of a current user logged in (is it a twitter or github account?) 
	client_id = social_app.client_id #get the client id from social app
	client_secret = social_app.secret #get the client secret(secret key) from the social app

	auth_value = OAuth1(client_id , client_secret, token, token_secret) #We used OAuth1 to combine all the needed values (4 values) , if it one value then no need for OAuth1  

	response = requests.get(url, auth=auth_value) #get url request and give response

	return JsonResponse(response.json(), safe=False)

