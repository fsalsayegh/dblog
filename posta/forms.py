from django import forms
from .models import Fatmaa

class PostForm(forms.ModelForm):
	class Meta:
		model = Fatmaa
		fields = ['title' , 'content' ,'img']