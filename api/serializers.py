from rest_framework import serializers
from posta.models import Fatmaa
from django_comments.models import Comment

class CommentListSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Comment
		fields = ['object_pk', 'user', 'comment', 'submit_date'] #object_pk refers to the id of the post 

class CommentCreateSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Comment
		fields = ['object_pk', 'comment']

class PostListSerializer(serializers.ModelSerializer): #add a link to the detail page for each object
	author = serializers.SerializerMethodField() #method are functions for a class so need to use functions
	detail_page = serializers.HyperlinkedIdentityField(
		view_name="api:detail",
		lookup_field="slug",
		lookup_url_kwarg="post_slug"

		)
	class Meta:
		model = Fatmaa
		fields = ['title', 'author', 'publish_date', 'detail_page']

	def get_author(self, obj): #have to say person and before it get 
		return str(obj.author.username) #to show the author's name from the author object not the id #str is to return a string 

class PostDetailSerializer(serializers.ModelSerializer):
	author = serializers.SerializerMethodField() 
	comments = serializers.SerializerMethodField() 
	delete = serializers.HyperlinkedIdentityField(
		view_name="api:delete",
		lookup_field="slug",
		lookup_url_kwarg="post_slug" )

	update = serializers.HyperlinkedIdentityField(
		view_name="api:update",
		lookup_field="slug",
		lookup_url_kwarg="post_slug" )

	class Meta:
		model = Fatmaa
		fields = "__all__"
		
	def get_author(self, obj):
		return str(obj.author.username)
	def get_comments(self, obj):
		comment_list = Comment.objects.filter(object_pk=obj.id)
		comments=CommentListSerializer(comment_list, many=True).data
		return comments


class PostCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fatmaa
		fields = ['title', 'content', 'publish_date' , 'draft' , 'img']