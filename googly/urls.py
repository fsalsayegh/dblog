from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^psearch/$', views.place_text_search, name='place-search'),
    

    ]