from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, Label


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta: 
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LabelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Label
        fields = '__all__'
        
# serializer for the note class
class NoteSerializer(serializers.ModelSerializer): 
    author = serializers.CharField()
    label = serializers.CharField()
    can_edit = serializers.SerializerMethodField()

    class Meta: 
        model = Note
        fields = ['id','author', 'label', 'title', 'text', 'created', 'modified', 'can_edit']
        
    def create(self, validated_data):
        # removing the nested label and author objects and saving them separately
        author = validated_data.pop('author')
        author = User.objects.get(username=author)
        label = validated_data.pop('label') 
        label, created = Label.objects.get_or_create(title=label)
        note = Note.objects.create(**validated_data)
        note.label = label
        note.author = author
        note.save()
        return note
    
    """
     This method sets the write access for request.user.
     Convention for naming such methods is get_<field_name>.  
     It is bounded to a SerializerMethodField instance. 
    """
    def get_can_edit(self, obj):
        request = self.context.get('request')
        return request.user in obj.can_edit.all()