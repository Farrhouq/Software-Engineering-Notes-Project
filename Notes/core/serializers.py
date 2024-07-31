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
    labelId = serializers.CharField(write_only=True, required=False) # * It seems id's are read-only (of course you don't even have the id until the object is created) but I need the id value so I've just used another field
    class Meta: 
        model = Label
        fields = '__all__'
    
    def create(self, validated_data):
        username = validated_data.pop('user')
        # print(validated_data)
        # labelId  is not required for creating a new label
        user = User.objects.get(username=username)
        label = Label.objects.create(**validated_data)
        label.user = user
        label.save()
        return label
    
    def update(self, instance, validated_data):
        instance.color = validated_data.get('color', instance.color) # only color can be updated for a label
        instance.save()
        return instance
# serializer for the note class
class NoteSerializer(serializers.ModelSerializer): 
    author = serializers.CharField()
    # label = serializers.CharField(allow_null=True, required=False)
    label = LabelSerializer(allow_null=True)
    can_edit = serializers.SerializerMethodField()

    class Meta: 
        model = Note
        fields = ['id','author', 'label', 'title', 'brief', 'private', 'content', 'created', 'modified', 'can_edit']
        
    def create(self, validated_data):
        # removing the nested label and author objects and saving them separately
        author = validated_data.pop('author')
        author = User.objects.get(username=author)
        label = validated_data.get('label') # label = dictionary or None
        print(label)
        if label:
            validated_data.pop('label') 
            label = Label.objects.get(user=author, id=label.get('labelId')) # Labels are created before the note so it would already exist (we just need to get it)
        note = Note.objects.create(**validated_data)
        note.label = label # sets note to a label object or None
        note.author = author
        note.save()
        return note
    
    def update(self, instance: Note, validated_data):
        label = validated_data.get('label')
        print('the current label is', label)
        if label:
            validated_data.pop('label') 
            label = Label.objects.get(user=instance.author, id=label.get('labelId'))
        instance.label = label 
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