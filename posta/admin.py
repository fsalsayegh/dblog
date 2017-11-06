from django.contrib import admin
from .models import Fatmaa

class AdminFatma(admin.ModelAdmin):
	list_display =["title"]
	search_fields = ["title"]
	class Meta:
		model=Fatmaa
			
admin.site.register(Fatmaa, AdminFatma)

