from django.shortcuts import render , redirect
from .models import Fatmaa
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
	objects= Fatmaa.objects.all()
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
	context ={"post_items": objects}
	return render(request, "list.html", context)








def post_detail(request, post_id):
	item = Fatmaa.objects.get(id=post_id)
	context ={"item": item}
	return render(request, "detail.html", context)

def post_create(request):
	item = Fatmaa.objects.all()
	form = PostForm(request.POST or None , request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request, "Awesome, you just added a blog post !")
		return redirect("list")
	context ={"form":form , "item":item}
	return render(request, "post_create.html", context)

def post_update(request, post_id):
	item = Fatmaa.objects.get(id=post_id)
	form = PostForm(request.POST or None, request.FILES or None, instance=item)
	if form.is_valid():
		form.save()
		messages.info(request, "you just changed a blog post")
		return redirect("list")
	context ={"form":form, "item":item}
	return render(request, "post_update.html", context)

def post_delete(request, post_id):
	Fatmaa.objects.get(id=post_id).delete()
	messages.warning(request, "deleted")
	return redirect("list")

	
	
  