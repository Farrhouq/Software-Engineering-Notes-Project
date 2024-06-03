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
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='notes') # may be changed to a many-to-many field for collaboration feature (authors) or I'll rather add a coauthor's field (I'm not sure)
    label = models.ForeignKey(Label, on_delete=models.CASCADE, null=True, related_name='notes')
    title = models.CharField(max_length=128)
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # private = models.BooleanField(default=True) # Can only be viewed by specific people
    # shared_to = models.JSONField(default=list) # a list of id's / may be replaced by a database relationship
    
    
    def __str__(self) -> str:
        return self.title
    
# ! not migrated yet
# class UserData(AbstractModel):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='data')
#     received = models.JSONField(default=list) # a list of id's of received notes (a stack will be used to order the id's) / may be replaced by a database relationship