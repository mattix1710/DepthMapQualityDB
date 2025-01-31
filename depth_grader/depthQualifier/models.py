from django.db import models
from django.core.exceptions import ValidationError
import re

# importing own file (for better function separation)
from .validators import *

############################
# VALIDATORS
#

# MATEUSZ
def method_location(instance, method_name):
    file_name = str(method_name)
    file_extension = file_name[file_name.index('.'):].lower()

    name = str(instance.method_name).lower().replace(' ', '_')

    # when returns: create folder of method_name title and name the file as it is
    return 'proposed_methods/' + name + '/' + name + file_extension

# MATEUSZ
def validate_method_name_exist(value):
    for elem in MethodProposal.objects.all():
        if(elem.method_name.lower() == value.lower()):
            raise ValidationError('Project of the same name already exists!')

# MATEUSZ
#
# regular expression propositions:
# ^[\w][\w #&()+*\\\/-]{1,}$

# method_name - name of a method given by user in form
def validate_method_name_correct(method_name):
    if not re.search(r"^[a-zA-Z_0-9][a-zA-Z_ 0-9]{1,}$", method_name):
        if not re.search("^.{2,}$", method_name):
            raise ValidationError('Title should have at least 2 characters!')
        raise ValidationError('Title encloses invalid characters!\nIt should include only a-z, A-Z, 0-9, _ and space characters.')
    
# MATEUSZ
def validate_sequence_name_exist(value):
    for elem in Sequence.objects.all():
        if(elem.seq_name.lower() == value.lower()):
            raise ValidationError('Project of the same name already exists!')

# MATEUSZ
def validate_sequence_name_correct(value):
    if not re.search("^[a-zA-Z_]{5,}$", value):
        if not re.search("^.{5,}$", value):
            raise ValidationError('Sequence name should have at least 5 characters!')
        raise ValidationError('Sequence name encloses invalid characters!\nIt should include only a-z, A-Z and _ (underscore) characters.')
    
# MATEUSZ
def sequence_location(instance, seq_name):
    file_name = str(seq_name)
    file_extension = file_name[file_name.index('.'):].lower()

    name = str(instance.title).lower().replace(' ', '_')

    # when returns: create folder of sequence_name title and name the file as it is
    return 'textures/' + 'texture_' + name + file_extension

############################
# MODELS
#

class MethodProposal(models.Model):
    id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=30, unique=True, validators=[validate_method_name_exist, validate_method_name_correct])
    desc = models.TextField()
    upload_date = models.DateField(auto_now=True)
    src = models.FileField(upload_to=method_location, validators=[validate_archive_method])
    
    def __str__(self) -> str:
        return self.method_name

# Sequence can be updated only from admin perspective
class Sequence(models.Model):
    id = models.AutoField(primary_key=True)
    seq_name = models.CharField(max_length=30, unique=True, validators=[validate_sequence_name_exist, validate_sequence_name_correct])
    seq_src = models.FileField(upload_to=sequence_location, validators=[validate_archive_sequence])
    
    def __str__(self) -> str:
        return self.seq_name
    
class SeqDepthResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    method_id = models.ForeignKey(MethodProposal, on_delete=models.CASCADE, db_column='method_id', to_field='id')   # while deleting method - delete its data
    seq_id = models.ForeignKey(Sequence, on_delete=models.PROTECT, db_column='seq_id', to_field='id')               # while deleting test sequence - protect calcutions
    synth_PSNR_1018    = models.FloatField(null=True)
    synth_bitrate_1018 = models.FloatField(null=True)
    synth_PSNR_3042    = models.FloatField(null=True)
    synth_bitrate_3042 = models.FloatField(null=True)
    synth_PSNR_none    = models.FloatField(null=True)
    synth_bitrate_none = models.FloatField(null=True)
    
    def __str__(self) -> str:
        return "{} : {}".format(self.method_id, self.seq_id)