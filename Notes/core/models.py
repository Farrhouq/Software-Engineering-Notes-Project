from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4 

# Inherit from this model to use a uuid as the primary key
class AbstractModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    class Meta:
        abstract = True

class Label(AbstractModel): 
    title = models.CharField(max_length=128)
    
    def __str__(self):
        return self.title

class Note(AbstractModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='notes')
    label = models.ForeignKey(Label, on_delete=models.CASCADE, null=True, related_name='notes')
    title = models.CharField(max_length=128)
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    private = models.BooleanField(default=True) # Can only be viewed by specific people otherwise everyone can read it (through shared link)
    public_to = models.ManyToManyField(User, related_name='readable_notes') # if note is private this specifies those allowed to read it (through shared link)
    can_edit = models.ManyToManyField(User, related_name='editable_notes') # if note is private this specifies those allowed to edit it (through shared link)    
    
    def __str__(self) -> str:
        return self.title
    
