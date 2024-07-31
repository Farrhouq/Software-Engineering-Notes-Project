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
from .models import Note, Label
from .permissions import CanReadNote
from .utils import assignLabelsToUsers

class CreateNote(generics.CreateAPIView):
    serializer_class = NoteSerializer
    
class UpdateNote(generics.UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    

class DeleteNote(generics.DestroyAPIView): 
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    

"""
This view is used to retrieve a particular note.
Permissions are checked if request.user has read access this view.
Further permissions are checked by the serializer if request.user has read access. 
A boolean field 'can_edit' is added to the retrieved note to show write access.
"""
class GetNote(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    # permission_classes = [CanReadNote] # * I noticed that If you add permissions to a view the authorization credentials are required in the request
    # Above line is commented out for testing but it must be enforced for security reasons
    
class GetNotes(generics.ListAPIView): 
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        request = self.request
        user = request.user
        print(request.query_params)
        getAll = request.query_params.get('all')
        getFor = request.query_params.get('username')
        # * getting all notes for test purposes
        if getAll is not None and getAll == 'True':
            return Note.objects.all()
        label = request.query_params.get('label')
        if user.is_authenticated:
            if label:
                return Note.objects.filter(author__username=getFor, label__title=label)  # return notes of a particular label for a particular user
            return Note.objects.filter(author__username=getFor) 
        return Note.objects.none() # no notes for unauthenticated users
    
class CreateLabel(generics.CreateAPIView):
    serializer_class = LabelSerializer
    
class DeleteLabel(generics.DestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    
class UpdateLabel(generics.UpdateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    
class GetLabels(generics.ListAPIView):
    serializer_class = LabelSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Label.objects.filter(user=user)
        return Label.objects.none()
    
class GetUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# This checks whether the server is running 
class Status(APIView):
    def get(self, request):
        # assignLabelsToUsers()
        return Response({'status': 'API is alive and well'})

# ValidateData function is being used instead for the signup
class SignUp(generics.CreateAPIView):
    serializer_class = UserSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
class Login(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK:
            token = AccessToken(response.data['access'])
            id = token.payload.get('user_id')
            user = User.objects.get(id=id) 
            response.data['user'] = UserSerializer(user).data
            print(response.data)
        return super().finalize_response(request, response, *args, **kwargs)

# ! PLEASE DO NOT TOUCH: For Testing

# from .components import noteReader
# class RenderNote(APIView):
#     # permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, id):
#         user = request.user
#         note = Note.objects.get(id=id)
#         canEdit = user.is_authenticated and (note.author == user or user in note.can_edit.all())
#         html = noteReader(note, canEdit, user.username if canEdit else 'Not logged in')
#         return HttpResponse(html)
    
# from .components import updatedDateTime
# class SaveNoteTest(generics.UpdateAPIView):
#     serializer_class = NoteSerializer
#     queryset = Note.objects.all() 
    
#     def finalize_response(self, request, response, *args, **kwargs):
#         # If the update was successful
#         if response.status_code == status.HTTP_200_OK: 
#             id = response.data.get('id')
#             note = Note.objects.get(id=id)
#             html = updatedDateTime(note)
#             return HttpResponse(html)
#             # response.status_code = status.HTTP_204_NO_CONTENT # so that htmx does not do any swapping
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
    
# using the view to test various payloads sent from the frontend
class Test(APIView):
    def get(self, request):
        return Response({'message': 'hello'})
    
    def post(self, request):
        print(request.data)
        return Response({'message': 'data received and processed successfully'})

from .forms import CreateUserForm
# validate data using django built-in form validation
class ValidateData(APIView):
    def post(self, request):
        form = CreateUserForm(request.data)
        if form.is_valid():
            user = form.save()
            return Response({'username': user.username, 'email': user.email})
        return Response(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)
from rest_framework_simplejwt.authentication import JWTAuthentication
class CheckToken(APIView):
    def get(self, request): 
        # if not request.user.is_authenticated: # for anonymous users
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message': 'token is still active'}) 
    
class CheckUsername(APIView): 
    def get(self, request):
        print('request has been received')
        username = request.query_params.get('username')
        try: 
            User.objects.get(username=username) 
        except User.DoesNotExist:
            return Response({'message': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response() 
            