from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
	message = "hahahaha you don't access."

	def has_object_permission(self, request, view, obj): #has_object_permission is a function from BasePermission  
		if (request.user == obj.author) or (request.user.is_staff): #checks if the current user is the author of the post or from staff
			return True
		else:
			return False