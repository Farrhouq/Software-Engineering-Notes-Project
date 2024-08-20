from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4 

# Inherit from this model to use a uuid as the primary key
class AbstractModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    class Meta:
        abstract = True

class Label(AbstractModel): 
    """
    There's this question as to whether labels deserve a separate table
    Generally they don't but other things might come up which we need to add to a label
    For instance the color the associated with that label in the UI
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='labels')
    title = models.CharField(max_length=128)
    color = models.CharField(max_length=50, null=True, default='blue')

    def __str__(self):
        return self.title

class Note(AbstractModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='notes')
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, related_name='notes')
    title = models.CharField(max_length=128, null=True)
    brief = models.TextField(max_length=500, null=True)
    content = models.JSONField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    favorite = models.BooleanField(default=False)
    private = models.BooleanField(default=True) # Can only be viewed by specific people otherwise everyone can read it (through shared link)
    can_read = models.ManyToManyField(User, related_name='readable_notes') # if note is private this specifies those allowed to read it (through shared link)
    can_edit = models.ManyToManyField(User, related_name='editable_notes') # if note is private this specifies those allowed to edit it (through shared link)    

    def __str__(self) -> str:
        return self.brief

class Data(AbstractModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='data')
    invites = models.JSONField(null=True, default=list)
    settings = models.JSONField(null=True, default=dict)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True)
