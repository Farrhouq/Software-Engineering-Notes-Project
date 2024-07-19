import random
from django.contrib.auth.models import User
from .models import Label, Note


def run():
    # Just checking the usage of random.choice
    users = User.objects.all()
    user = random.choice(users)
    print(user)
    
def assignLabelsToUsers():
    """
    """
    notes = Note.objects.all()
    for note in notes:
        # If the existing note label was not assigned to a user (which should be the note author) 
        # then we check if there's a new label with the same name created by the author
        # If one doesn't exist we create it and delete the old one.
        print(f'{note.author}, {note.label.user if note.label else ""}, {note.label.title if note.label else ""}')
        # if note.label and not note.label.user:
        #     label, created = Label.objects.get_or_create(user=note.author, title=note.label.title) # label assigned to author with the same name exists ?
        #     note.label.delete() # delete old label
        #     note.label = label # assign new label to note
        #     note.save()
    print('Done assigning labels to users randomly')
    
    