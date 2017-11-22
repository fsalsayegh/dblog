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
	form = UserSignUp()
	context['form']= form


	if request.method == "POST":
		form = UserSignUp(request.POST)
		if form.is_valid():
			user= form.save()
			username = user.username
			password = user.password

			user.set_password(password)
			user.save()

			auth = authenticate(username=username, password=password)
			login(request, auth)

			return redirect("list")
		messages.warning(request, form.errors)
		return redirect("signup")
	return render(request, 'signup.html', context)


def userlogin(request):
	context = {}
	form = UserLogin()
	context['form']= form


	if request.method == "POST":
		form = UserLogin(request.POST)
		if form.is_valid():
			
			some_username = form.cleaned_data['username']
			some_password = form.cleaned_data['password']

			auth = authenticate(username=some_username, password=some_password)
			if auth is not None:
				login(request, auth)
				return redirect("list")
			messages.warning(request, 'Incorret Username/Password combination')
			return redirect("login")
		messages.warning(request, form.errors)
		return redirect("login")
	return render(request, 'login.html', context)

def userlogout(request):
	logout(request)
	return redirect("login")


def post_list(request):
	today = timezone.now().date()

	if request.user.is_staff:
		objects=Fatmaa.objects.all()
	else:
		objects= Fatmaa.objects.filter(draft=False, publish_date__lte=today)

	query= request.GET.get('q')
	if query:
		objects=objects.filter(

			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)
			).distinct()

		#objects= Fatmaa.objects.all().order_by('-title', '-id')
	paginator = Paginator(objects, 3) # Show 25 contacts per page

	number = request.GET.get('page')
	try:
		objects = paginator.page(number)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		objects = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		objects = paginator.page(paginator.num_pages)

	context ={"post_items": objects, "today": today}
	return render(request, "list.html", context)



def post_detail(request, post_slug):
	today= timezone.now().date()
	item = Fatmaa.objects.get(slug=post_slug)
	liked=False
	if not (request.user.is_staff):
		if item.draft or item.publish_date > today:
			raise Http404


	if request.user.is_authenticated():
		if Like.objects.filter(post=item, user=request.user).exists():
			liked = True
		else:
			liked = False

	like_count= item.like_set.count()

	context ={"item": item , "liked" :liked, "liked_count": like_count}
	return render(request, "detail.html", context)



def post_create(request):
	if not request.user.is_staff:
		raise Http404

	form = PostForm(request.POST or None , request.FILES or None)
	if form.is_valid():
		fatma_post=form.save(commit=False)
		fatma_post.author= request.user
		fatma_post.save()

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
	Fatmaa.objects.get(slug=post_slug).delete()
	messages.warning(request, "deleted")
	return redirect("list")



def like_button(request , post_id):
	post_object = Fatmaa.objects.get(id=post_id)

	like, created = Like.objects.get_or_create(user=request.user, post=post_object)
	if created:
		action = "like"
	else:
		like.delete()
		action = "unlike"
	like_count= post_object.like_set.count()

	response={
	"like_count": like_count , "action":action

	}
	return JsonResponse(response, safe=False)


	
	
  