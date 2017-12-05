from rest_framework import serializers
from posta.models import Fatmaa
from django_comments.models import Comment
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


class UserLoginSerializer(serializers.Serializer): #didnt use modelserializer cause not modifing anything in the database
	username = serializers.CharField()
	password = serializers.CharField(style={"input_type":"password"} , write_only=True)
	token = serializers.CharField(read_only=True, allow_blank=True) #read_only=True means dont want the user to create the token dont want the user to create the token #allow_blank=True because a user will not always get a token back if he doesn't log in successfully

	def validate(self, data): #handles all data validation #buitl in function in Serializer
		username = data.get('username') #get the username from database
		password = data.get('password')

		if username == '': #if didnt enter a username 
			raise serializers.ValidationError('A username is required to login')

		user = User.objects.filter(username=username) #take the username
		if user.exists(): #if the username is exists in database
			user_obj = user.first()
		else:
			raise serializers.ValidationError("this username does not exists")

		if user_obj: #checks if the password of the wanted username is correct and match it 
			if not user_obj.check_password(password): #a method from the user model to check if the password is correct or not #return true or false(boolen)
				raise serializers.ValidationError("Incorrect credentials, please try again")
		
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER 

		payload = jwt_payload_handler(user_obj) # a function generate a token and assign it to a user 
		token = jwt_encode_handler(payload)	# encoded the token that generated
		data["token"] = token #return the token along with the data
		return data


class UserCreateSerializer(serializers.ModelSerializer): #for signup
	password = serializers.CharField(style={"input_type":"password"} , write_only=True) #hide the pass when type it #write_only=True used to hide the password on the response
	class Meta:
		model = User
		fields = ['username', 'password']

	def create(self, validated_data):
		username = validated_data['username'] #retrieve the username
		password = validated_data['password']
		new_user = User(username=username) #take the username and put it in new_user but don't save it yet
		new_user.set_password(password) #hashing the pass
		new_user.save()
		return validated_data


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['email', 'username', 'first_name', 'last_name']


class CommentListSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Comment
		fields = ['object_pk', 'user', 'comment', 'submit_date'] #object_pk refers to the id of the post 

class CommentCreateSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Comment
		fields = ['object_pk', 'comment']

class PostListSerializer(serializers.ModelSerializer): #add a link to the detail page for each object
	author = UserSerializer()   #serializers.SerializerMethodField() #method are functions for a class so need to use functions
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
	author = UserSerializer() #display the user info as a dictionary cause the data of user is serialized
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
		comment_list = Comment.objects.filter(object_pk=obj.id) #Filters and gets the comments that are related to the specified Post object
		comments=CommentListSerializer(comment_list, many=True).data #serialize the data so that we can get it in JSON format
		return comments #We save the serialized data in the variable comments and return it


class PostCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fatmaa
		fields = ['title', 'content', 'publish_date' , 'draft' , 'img']