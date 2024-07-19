from rest_framework.permissions import BasePermission

class CanReadNote(BasePermission):
    message = 'not allowed to view this note'
    
    def has_object_permission(self, request, view, obj):
        # If it's a public note then anyone can read it
        if not obj.private:
            return True
        return request.user == obj.author or request.user in obj.can_read.all()
    
    
class CanEditNote(BasePermission):
    message = 'not allowed to edit this note'
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.user in obj.can_edit.all()
        