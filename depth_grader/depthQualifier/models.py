from django.db import models
from .validators import *
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
def seq_location(instance, seq_name):
    folder_name = str(seq_name)
    folder_name = folder_name[:folder_name.rfind('.')].replace(' ', '_')

    return 'sequences/' + folder_name + '/' + str(seq_name)

def validate_project_name_exist(value):
    for elem in SequenceModel.objects.all():
        if(elem.title.lower() == value.lower()):
            raise ValidationError('Project of the same name already exists!')

class SequenceModel(models.Model):
    title = models.CharField(max_length=30, unique=True, validators=[validate_project_name_exist])
    desc = models.TextField()
    src = models.FileField(upload_to=seq_location, validators=[validate_archive_extension])

    def __str__(self):
        return self.title