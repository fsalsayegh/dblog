from django.shortcuts import render , redirect
from .models import Fatmaa , Like
from .forms import PostForm , UserSignUp , UserLogin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404 , JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate


def usersignup(request):
	context = {}
	form = UserSignUp() #add the model form (usersignup) to a variable
	context['form']= form


	if request.method == "POST": #checks if there is any data submitted in the form
		form = UserSignUp(request.POST) #save the form with the data inside the variable
		if form.is_valid(): #checks if the form submited is correct 
			user= form.save() #save the form in user variable
			username = user.username #retrieve the username from the form
			password = user.password #retrieve the password from the form

			user.set_password(password) #hashing the password to make it more secure (hide password)
			user.save() #save the form

			auth = authenticate(username=username, password=password) #used to login after signing up #authinticate the username and password of the user
			login(request, auth) #login the user to the page

			return redirect("list") #return to the list page
		messages.warning(request, form.errors) #an error message will be showen if the form is not valid
		return redirect("signup") #return to the signup page
	return render(request, 'signup.html', context) #return to the signup page if the user didn't submit any data to the form


def userlogin(request):
	context = {}
	form = UserLogin() #add the form (usersignup) to a variable #note: it is not a model form ; it is a form
	context['form']= form


	if request.method == "POST":
		form = UserLogin(request.POST)
		if form.is_valid():
			#note: we should always use cleaned_data when using a form of type form 
			some_username = form.cleaned_data['username'] #retrieve the username from the form 
			some_password = form.cleaned_data['password'] #retrieve the password from the form

			auth = authenticate(username=some_username, password=some_password)  #authinticate the username and password of the user #checks if there is a username with this password
			if auth is not None: #checks the username and the password are correct and exists in the database 
				login(request, auth)
				return redirect("home:list")
			messages.warning(request, 'Incorret Username/Password combination') #an error message will show if the username or the password is not correct 
			return redirect("home:login")
		messages.warning(request, form.errors)#an error message will be showen if the form is not valid
		return redirect("home:login")
	return render(request, 'login.html', context) #return to the signup page if the user have not submit yet any data to the form

def userlogout(request):
	logout(request) 
	return redirect("login")


def post_list(request):
	today = timezone.now().date() #a function to display time

	if request.user.is_staff:#checks if the current user is from the stuff 
		objects=Fatmaa.objects.all() #retrieve or show all the model Fatmaa objects including the draft and not published posts to the stuff user 
	else:
		objects= Fatmaa.objects.filter(draft=False, publish_date__lte=today) #show only the posts with no draft or the publish posts to the normal user

	query= request.GET.get('q') #get whatever inside the GET request (q) 
	if query: #if query has data inside 
		objects=objects.filter(

			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)
			).distinct() #filter or find the wanted posts based on the title , content , first name and last name

		#objects= Fatmaa.objects.all().order_by('-title', '-id')
	paginator = Paginator(objects, 3) #Show 3 objects per page

	number = request.GET.get('page') #get the number of the page the object is located in #get whatever inside the GET request (page) #note: page is a number
	try:
		objects = paginator.page(number) #show the specific object and its specific page number
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		objects = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results or empty
		objects = paginator.page(paginator.num_pages)

	context ={"post_items": objects, "today": today}
	return render(request, "list.html", context)



def post_detail(request, post_slug):
	today= timezone.now().date()
	item = Fatmaa.objects.get(slug=post_slug) #retrieve the object with the specific slug (detail of a specific object)
	liked=False
	if not (request.user.is_staff): #if the user is not a stuff user
		if item.draft or item.publish_date > today: #if the current date (today) is less than the future posts date (published-draft)  
			raise Http404 #show page not found 


	if request.user.is_authenticated(): #checks if the current user is logged in or not cause the user should be logged in to like a post or unlike
		if Like.objects.filter(post=item, user=request.user).exists(): #getting who did like and to which post 
			liked = True # will be true if there is a like in a post
		else:
			liked = False

	like_count= item.like_set.count() #count the number of likes in a post  #a set of likes in a post

	context ={"item": item , "liked" :liked, "liked_count": like_count}
	return render(request, "detail.html", context)



def post_create(request):
	if not request.user.is_staff:
		raise Http404

	form = PostForm(request.POST or None , request.FILES or None) #if there is a POST request (data submitted to form) and an image (request.FILES) or didn't submit any (none)
	if form.is_valid():
		fatma_post=form.save(commit=False) #the form should not be saved yet
		fatma_post.author= request.user #retrieve the current user from the form
		fatma_post.save() #save the form

		messages.success(request, "Awesome, you just added a blog post !")
		return redirect("list")
	context ={"form":form}
	return render(request, "post_create.html", context)

def post_update(request, post_slug):
	if not request.user.is_staff:
		raise Http404

	item = Fatmaa.objects.get(slug=post_slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=item)
	if form.is_valid():
		form.save()
		messages.info(request, "you just changed a blog post")
		return redirect("list")
	context ={"form":form, "item":item}
	return render(request, "post_update.html", context)

def post_delete(request, post_slug):
	if not request.user.is_staff:
		raise Http404
	Fatmaa.objects.get(slug=post_slug).delete() #delete a specific object or post
	messages.warning(request, "deleted")
	return redirect("list")



def like_button(request , post_id):
	post_object = Fatmaa.objects.get(id=post_id) #retrieve the specific object or post of specific id

	like, created = Like.objects.get_or_create(user=request.user, post=post_object) #checks wheather the current logged in user did like or not to a specific post  
	if created: # if the current loged in user did not has like this post previously , then create one 
		action = "like" #active the button to like
	else:
		like.delete() #delete the like object from the Like fields 
		action = "unlike" #unlike the post if the current logged in user who already has a like to the post
	like_count= post_object.like_set.count() 

	response={
	"like_count": like_count , "action":action

	}
	return JsonResponse(response, safe=False)


	
	
  