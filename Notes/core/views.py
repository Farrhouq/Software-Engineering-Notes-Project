# django imports 
from django.http import HttpResponse
from django.contrib.auth.models import User

# rest framework imports
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
# other imports
from .serializers import NoteSerializer, LabelSerializer
from .models import Note

class CreateNote(generics.CreateAPIView):
    serializer_class = NoteSerializer
    
class UpdateNote(generics.UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class GetNote(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class GetNotes(generics.ListAPIView): 
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class CreateLabel(generics.CreateAPIView):
    serializer_class = LabelSerializer

# ! PLEASE DO NOT TOUCH: For Testing

from .components import noteReader

class RenderNote(APIView):
    def get(self, request, id):
        note = Note.objects.get(id=id)
        html = noteReader(note)
        return HttpResponse(html)
    
class SaveNoteTest(generics.UpdateAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects.all() 
    
    def finalize_response(self, request, response, *args, **kwargs):
        # If the update was successful
        if response.status_code == status.HTTP_200_OK: 
            response.status_code = status.HTTP_204_NO_CONTENT # so that htmx does not do any swapping
        return super().finalize_response(request, response, *args, **kwargs)
        

