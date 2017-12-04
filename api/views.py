from rest_framework.generics import ListAPIView , RetrieveAPIView ,DestroyAPIView , CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from posta.models import Fatmaa  #we add posta.models not .models cause not in the same directory 

from .serializers import *
from .permissions import IsAuthor
from django.db.models import Q
from rest_framework.filters import SearchFilter #import library to filter
from django_comments.models import Comment

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils import timezone

class CommentListView(ListAPIView): #show the comment for all list objects
	serializer_class = CommentListSerializer
	permission_classes = [AllowAny]
	
	def get_queryset(self, *args, **kwargs):
		queryset = Comment.objects.all()
		query = self.request.GET.get('query')
		if query:
			queryset = queryset.filter(
				Q(object_pk=query)|
				Q(user=query)
				).distinct()
		return queryset

class CommentCreateView(CreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentCreateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(
			content_type=ContentType.objects.get_for_model(Fatmaa), #getting a model (ContentType) from a model(Mode)
			site=Site.objects.get(id=1),
			user=self.request.user,
			user_name=self.request.user.username,
			submit_date=timezone.now()
			)

class PostListView(ListAPIView): 
	#note: queryset and serializer_class are not variables so thier names should be the same
	queryset = Fatmaa.objects.all() #shows the posta list of objects
	serializer_class = PostListSerializer #serialize the object to put them in json structure 
	filter_backends = [SearchFilter,] #option 1 to to filter through the list  
	search_fields=['title', 'content', 'author__username'] #to filter the search based on title ,content and author name #author is a foriegnkey which is an object.. the username of an object #refere to the field from an object #when refering to the field need __ but . used  when using it 
	permission_classes = [AllowAny] 

	#option 2 to filter through the list 
	# def get_queryset(self, *args, **kwargs): #we used func cause this is a class and we did it before in func not a class 
	# 	queryset = Fatmaa.objects.all()
	# 	query = self.request.GET.get('query') #retrieve what inside the GET request #self used for request 
	# 	if query:
	# 		queryset = queryset.filter(
	# 			Q(title__icontains=query)|
	# 			Q(content__icontains=query)
	# 			).distinct()
	# 	return queryset 

class PostCreateView(CreateAPIView): 
	
	queryset = Fatmaa.objects.all() 
	serializer_class = PostCreateUpdateSerializer 
	permission_classes = [IsAuthenticated] 
	
	def perform_create(self, serializer): #it is a method which means functions for class #allows you to overwrite what happens when the object get created or save 
		serializer.save(author=self.request.user) #add the current auther of the post instead of the defualt value which is 1 assigned in the posta model 

class PostDetailView(RetrieveAPIView): 
	queryset = Fatmaa.objects.all() 
	serializer_class = PostDetailSerializer 
	lookup_field = 'slug' #the field from the object I need to identify it is called slug
	lookup_url_kwarg = 'post_slug' #the parameter
	permission_classes = [AllowAny,]
	

class PostDeletelView(DestroyAPIView): 
	queryset = Fatmaa.objects.all() 
	serializer_class = PostListSerializer  # we used serializer in the delete view to show which object in the list is deleted
	lookup_field = 'slug' #the field from the object I need to identify it is called slug
	lookup_url_kwarg = 'post_slug' #
	permission_classes = [IsAuthenticated , IsAdminUser] #should be logged in and as a stuff member


class PostUpdateView(RetrieveUpdateAPIView): 
	queryset = Fatmaa.objects.all() 
	serializer_class = PostCreateUpdateSerializer  # we used serializer in the delete view to show which object in the list is deleted
	lookup_field = 'slug' #the field from the object I need to identify it is called slug
	lookup_url_kwarg = 'post_slug'
	permission_classes =[IsAuthenticated , IsAuthor] #checks if you logged in then if it is the author's post




