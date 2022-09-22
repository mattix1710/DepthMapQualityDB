# REGULAR imports
from pathlib import Path
import subprocess
import pathlib

# DJANGO imports
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.contrib import messages

# LOCAL imports
from .forms import UploadZipForm
from .src.functions import *
from .models import *

# EOF imports
#=================================

TEMPLATE_PATH = 'depthQualifier/'
FUNCTIONS_PATH = str(pathlib.Path(__file__).parent) + "/src/"

DEBUG = "INFO: "

# Create your views here.
def index(request):
    print(DEBUG + "site rendering")
    # template = loader.get_template(TEMPLATE_PATH + "index.html")
    # print(template)
    # return HttpResponse(template.render)
    return render(request, TEMPLATE_PATH + 'index.html')
    # return HttpResponse("<br><br><center><h1>Here will be placed a database of cute HTTP cats!</h1></center>")

def addSequence(request):
    if request.method == 'POST':
        form = UploadZipForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES.getlist('src')[0]
            # CURRENT_LOCATION = form.cleaned_data['title']           # INFO: meh - działa tylko w tym pliku...
            SequenceModel.objects.create(title = form.cleaned_data['title'],
                                        desc = form.cleaned_data['desc'],
                                        src = f)

            # perform operations on given files
            seqTitle = (str(form.cleaned_data['title'])).lower().replace(' ', '_')

            # TODO: unzip and calculate estimated PSNR
            # UNZIP DATA from the newly created object
            for obj in SequenceModel.objects.all():
                if obj.title == form.cleaned_data['title']:
                    # display a message
                    print("Hello")
                    # zipUnpack(str(obj.src))
                    # batchSynthesis(obj)

            # form.save()

            return HttpResponseRedirect('../sequences')
    else:
        form = UploadZipForm()

    return render(request, TEMPLATE_PATH + 'sequence_form.html', {'form': form})

class SequenceList(ListView):
    template_name = TEMPLATE_PATH + 'sequences.html'
    context_object_name = 'seq_list'

    def get_queryset(self):
        # table sorting
        if(self.request.method == 'GET' and self.request.GET.__contains__('sort')):         # if GET method was set
            switch = {
                'titleUP'   : SequenceModel.objects.order_by('title'),
                'titleDOWN' : SequenceModel.objects.order_by('-title'),             # "-" is used for managing descending order
                'idUP'      : SequenceModel.objects.order_by('id'),
                'idDOWN'    : SequenceModel.objects.order_by('-id'),
            }

            # return chosen order or (if there is no such position) - defualt one
            return switch.get(self.request.GET.__getitem__('sort'), SequenceModel.objects.all())


        return SequenceModel.objects.all()

def testing(request):
    if(request.method == 'GET' and request.GET.__contains__('process')):

        value = request.GET.__getitem__('process')
        # if(value == 'compress'):
        #     batchCompress()
        # elif(value == 'decompress'):
        #     batchDecompress()
        # if(value == 'synthesis'):
        #     batchSynthesis()

    # checkPrint()

    return render(request, TEMPLATE_PATH + 'testing.html')

def delete_view(request, seq_id=None):
    object = SequenceModel.objects.get(id=seq_id)
    deleteFile(object)
    objTitle = object.title
    object.delete()
    print('Sequence "' + str(objTitle) + '" has been deleted!')
    return HttpResponseRedirect('../../sequences')