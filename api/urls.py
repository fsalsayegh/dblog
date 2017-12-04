from django.conf.urls import url
#from .views import PostListView ,PostDetailView
from . import views

urlpatterns = [
    #path list/create/detail/delete or update 
    url(r'^$', views.PostListView.as_view(), name='list'), # if you used (from .views import PostListView ,PostDetailView) instead of ....from . import views... should be... views.PostListView.as_view()
    url(r'^create/$', views.PostCreateView.as_view(), name='create'), #should add create in the second line cause this is the original location or path 
    url(r'^comments/$', views.CommentListView.as_view(), name='comment-list'),
    url(r'^comment/$', views.CommentCreateView.as_view(), name='comment-create'),
    url(r'^(?P<post_slug>[-\w]+)/detail/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^(?P<post_slug>[-\w]+)/delete/$', views.PostDeletelView.as_view(), name='delete'), #we added /delete/ cause there are to ways etheir delete or update inside the detail
    url(r'^(?P<post_slug>[-\w]+)/update/$', views.PostUpdateView.as_view(), name='update'),
   

    ]

    