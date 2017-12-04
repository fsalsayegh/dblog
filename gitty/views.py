from django.shortcuts import render
from django.http import JsonResponse
import requests

def member_list(request):
	user = request.user #add the current user name to the variable user
	social_account = user.socialaccount_set.get(user=user.id)#get the specific logged in user from a set of social accounts(twitter or github,...)
	social_token = social_account.socialtoken_set.get(account=social_account.id) #get the token for that social account which is (github)
	token = social_token.token #access the token field of that social account
	#url = "https://api.github.com/orgs/joinCODED/members"
	url = "https://api.github.com/users/DarthHamza/repos" #To display the repositries of user DarthHamza
	response = requests.get(url, headers={"Authorization": "token " +token}) #pass the autherization key "token" using headers to access the github API serveces
	return JsonResponse(response.json(), safe=False)




