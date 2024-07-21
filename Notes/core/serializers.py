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
    user = serializers.CharField()
    class Meta: 
        model = Label
        fields = '__all__'
        
# serializer for the note class
class NoteSerializer(serializers.ModelSerializer): 
    author = serializers.CharField()
    label = serializers.CharField(allow_null=True, required=False)
    can_edit = serializers.SerializerMethodField()

    class Meta: 
        model = Note
        fields = ['id','author', 'label', 'title', 'brief', 'content', 'created', 'modified', 'can_edit', 'private']
        
    def create(self, validated_data):
        # removing the nested label and author objects and saving them separately
        author = validated_data.pop('author')
        author = User.objects.get(username=author)
        label = validated_data.get('label') # label = string or None
        if label:
            validated_data.pop('label') 
            label, created = Label.objects.get_or_create(user=author, title=label)
        note = Note.objects.create(**validated_data)
        note.label = label # sets note to a label object or None
        note.author = author
        note.save()
        return note
    
    def update(self, instance: Note, validated_data):
        label = validated_data.get('label')
        if label:
            pass # new label will be updated here
        instance.title = validated_data.get('title', instance.title)
        instance.brief = validated_data.get('brief', instance.brief)
        instance.content = validated_data.get('content', instance.content)
        instance.private = validated_data.get('private', instance.private)
        instance.save()
        return instance
    
    
    """
     This method sets the write access for request.user.
     Convention for naming such methods is get_<field_name>.  
     It is bounded to a SerializerMethodField instance. 
    """
    def get_can_edit(self, obj):
        request = self.context.get('request')
        return request.user == obj.author or request.user in obj.can_edit.all()