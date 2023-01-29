# REGULAR imports
import pathlib2 as pathlib

from django.http import HttpResponseRedirect
# DJANGO imports
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

# LOCAL imports
from .forms import UploadMethodZipForm
from .models import *
from .src.functions import *
from .tasks import process_the_depth_method

# EOF imports
#=================================

TEMPLATE_PATH = 'depthQualifier/'
FUNCTIONS_PATH = str(pathlib.Path(__file__).parent) + "/src/"

def index(request):
    return render(request, TEMPLATE_PATH + 'index.html')

def downloads(request):
    sequences = Sequence.objects.all()
    context = {'sequences' : sequences}

    return render(request, TEMPLATE_PATH + 'downloads.html', context=context)

def addDepthMethod(request):
    if(request.method == 'POST'):
        form = UploadMethodZipForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES.getlist('src')[0]
            print("FILE:", request.FILES['src'])
            
            # create new Method object
            MethodProposal.objects.create(method_name = form.cleaned_data['method_name'],
                                          desc = form.cleaned_data['desc'],
                                          src = f)
            
            depth_name = str(form.cleaned_data['method_name'])
            
            # UNZIP DATA and process depths in order to obtain PSNR and bitrate results
            obj = MethodProposal.objects.get(method_name = depth_name)
            print("Processing depth method of ID: {}".format(obj.id))
            
            # create new SeqDepthResult object
            for sequence in Sequence.objects.all():
                if sequence.seq_name == 'all_sequences':
                    continue
                SeqDepthResult.objects.create(method_id = obj,
                                                seq_id = sequence)
                print("DEPTH: {} : {}".format(obj.id, sequence.id))
            
            process_the_depth_method.delay(obj.id)
            return HttpResponseRedirect('../methods')
    else:
        form = UploadMethodZipForm()
        
    return render(request, TEMPLATE_PATH + 'depth_form.html', {'form': form})

QUERY_BASE = '''SELECT met.upload_date, met.id, met.method_name, met.desc, met.src,
                res_1.synth_PSNR_1018 AS seq_1_PSNR_1018, 
                res_1.synth_PSNR_3042 AS seq_1_PSNR_3042, 
                res_1.synth_PSNR_none AS seq_1_PSNR_raw, 
                res_1.synth_bitrate_1018 AS seq_1_bitrate_1018,
                res_1.synth_bitrate_3042 AS seq_1_bitrate_3042,
                res_1.synth_bitrate_none AS seq_1_bitrate_raw,
                res_2.synth_PSNR_1018 AS seq_2_PSNR_1018, 
                res_2.synth_PSNR_3042 AS seq_2_PSNR_3042, 
                res_2.synth_PSNR_none AS seq_2_PSNR_raw,
                res_2.synth_bitrate_1018 AS seq_2_bitrate_1018,
                res_2.synth_bitrate_3042 AS seq_2_bitrate_3042,
                res_2.synth_bitrate_none AS seq_2_bitrate_raw
            FROM depthQualifier_methodproposal met
                INNER JOIN depthQualifier_seqdepthresult res_1
                    ON res_1.method_id = met.id AND res_1.seq_id = (
                                                            SELECT id
                                                            FROM depthQualifier_sequence
                                                            WHERE seq_name = 'PoznanFencing')
                INNER JOIN depthQualifier_seqdepthresult res_2
                    ON res_2.method_id = met.id AND res_2.seq_id = (
                                                            SELECT id
                                                            FROM depthQualifier_sequence
                                                            WHERE seq_name = 'Carpark')'''

ORDER_STRING = '\nORDER BY '

def MethodList(request):
    
    qs = QUERY_BASE
    if(request.method == 'GET' and request.GET.__contains__('sort')):
        value = request.GET.__getitem__('sort')
        
        # TODO: insert sorting buttons inside table (list) headers
        
        if value == 'idUP':
            order_fields = ['met.id']
        elif value == 'idDOWN':
            order_fields = ['met.id DESC']
        elif value == 'nameUP':
            order_fields = ['met.method_name']
        elif value == 'nameDOWN':
            order_fields = ['met.method_name DESC']
        elif value == 'dateUP':
            order_fields = ['met.upload_date']
        elif value == 'dateDOWN':
            order_fields = ['met.upload_date DESC']
        else:
            print('ERROR: No such value in sorting form!')
        
        qs += ORDER_STRING + ",".join(order_fields)
        
    RESULTS = MethodProposal.objects.raw(qs)
    
    # for obj in RESULTS:
    #     print(type(obj.upload_date))
    
    context = {'est_methods': RESULTS}
    
    return render(request, TEMPLATE_PATH + 'depth_est_methods.html', context=context)

def delete_method_view(request, method_id=None):
    try:
        method = MethodProposal.objects.get(id=method_id)
        delete_method(method)
        method_name = method.method_name
        # while deleting this object, it deletes also connected SeqDepthResult object
        method.delete()
        
        # DEBUG
        print('DELETE: Method "{}" of id ({}) has been deleted!'.format(method_name, method_id))
    except ObjectDoesNotExist:
        print("ERROR: was trying to delete non-existing MethodProposal object of id {}!".format(method_id))
    finally:
        return HttpResponseRedirect('../../methods')
    
def display_method_view(request, method_id=None):
    try:
        method = MethodProposal.objects.get(id=method_id)
        context = {'method': method}
        return render(request, TEMPLATE_PATH + 'display_method.html', context=context)
    except ObjectDoesNotExist:
        print("ERROR: was trying to display non-existing MethodProposal object of id {}!".format(method_id))
        return HttpResponseRedirect('../../methods')