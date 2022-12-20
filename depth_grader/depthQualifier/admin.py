from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SequenceModel)

admin.site.register(MethodProposal)
admin.site.register(Sequence)
admin.site.register(SeqDepthResults)