from django.shortcuts import render
from .models import Fatmaa

def post_list(request):
	objects= Fatmaa.objects.all()
	context ={"post_items": objects}
	return render(request, "list.html", context)

def post_detail(request, post_id):
	item = Fatmaa.objects.get(id=post_id)
	context ={"item": item}
	return render(request, "detail.html", context)
	
  