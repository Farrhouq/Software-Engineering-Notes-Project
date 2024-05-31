from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, Label


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['username', 'email']

class LabelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Label
        fields = '__all__'
        
# serializer for the note class
class NoteSerializer(serializers.ModelSerializer): 
    author = serializers.ReadOnlyField(source='author.email', allow_null=True)
    label = LabelSerializer()
    
    class Meta: 
        model = Note
        fields = ['id','author', 'label', 'title', 'text', 'created', 'modified']
        
    def create(self, validated_data):
        # removing the nested label object and saving it separately
        label = validated_data.pop('label') 
        label, created = Label.objects.get_or_create(**label)
        note = Note.objects.create(**validated_data)
        note.label = label
        note.save()
        return note