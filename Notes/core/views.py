# django imports 
from django.http import HttpResponse
from django.contrib.auth.models import User

# rest framework imports
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions 
from rest_framework.response import Response 

# other imports
from .serializers import NoteSerializer, LabelSerializer, UserSerializer
from .models import Note
from .permissions import CanReadNote

class CreateNote(generics.CreateAPIView):
    serializer_class = NoteSerializer
    
class UpdateNote(generics.UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    """
    This view is used to retrieve a particular note.
    Permissions are checked if request.user has read access this view.
    Further permissions are checked by the serializer if request.user has read access. 
    A boolean field 'can_edit' is added to the retrieved note to show write access.
    """
class GetNote(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [CanReadNote]

class GetNotes(generics.ListAPIView): 
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class CreateLabel(generics.CreateAPIView):
    serializer_class = LabelSerializer

# This checks whether the server is running 
class Status(APIView):
    def get(self, request):
        return Response({'status': 'API is alive and well'})
    
class SignUp(generics.CreateAPIView):
    serializer_class = UserSerializer

# ! PLEASE DO NOT TOUCH: For Testing

# from .components import noteReader

# class RenderNote(APIView):
#     def get(self, request, id):
#         note = Note.objects.get(id=id)
#         html = noteReader(note)
#         return HttpResponse(html)
    
# class SaveNoteTest(generics.UpdateAPIView):
#     serializer_class = NoteSerializer
#     queryset = Note.objects.all() 
    
#     def finalize_response(self, request, response, *args, **kwargs):
#         # If the update was successful
#         if response.status_code == status.HTTP_200_OK: 
#             response.status_code = status.HTTP_204_NO_CONTENT # so that htmx does not do any swapping
#         return super().finalize_response(request, response, *args, **kwargs)
        
# ! PLEASE DO NOT TOUCH: For Testing
class GetSharedNotes(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        notes = user.readable_notes.all()
        return notes

class ReadNote(generics.RetrieveAPIView):
    serializer_class = NoteSerializer
    permission_classes = [CanReadNote]