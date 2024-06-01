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

# PLEASE DO NOT TOUCH: For Testing

# from .components import noteReader
# class RenderNote(APIView):
#     def get(self, request, id):
#         note = Note.objects.get(id=id)
#         user = User.objects.first()
#         html = noteReader(user, note)
#         print(note.modified.ctime())
#         return HttpResponse(html)
    
#     def patch(self, request, id):
#         print('patch is working')
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT) 
        

