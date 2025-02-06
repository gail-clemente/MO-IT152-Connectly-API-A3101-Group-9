from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to only allow admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Admin").exists()
    

class IsPostAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
    
class IsCommentAuthor(BasePermission):
    """
    Custom permission to allow only the author of a comment to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an account to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id  # Allow access only if the user is the owner