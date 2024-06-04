from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrCanReadNote(BasePermission):
    message = 'not allowed to view this note'
    
    def has_permission(self, request, view):
        return True # returns true for now (I'm taking a break)
    
    
class IsAuthorOrCanEditNote(BasePermission):
    message = 'not allowed to edit this not'
    
    def has_permission(self, request, view):
        return True # returns true for now (I'm taking a break)
        