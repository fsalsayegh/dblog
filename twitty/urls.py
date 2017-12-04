from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'^twitty_search/$', views.tweet_search, name="twitty_search")
   

]