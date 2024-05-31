# django imports 

# rest framework imports
from rest_framework.generics import CreateAPIView, ListAPIView

# other imports
from .serializers import NoteSerializer, LabelSerializer
from .models import Note

class CreateNote(CreateAPIView):
    serializer_class = NoteSerializer
    
class GetNotes(ListAPIView): 
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class CreateLabel(CreateAPIView):
    serializer_class = LabelSerializer

