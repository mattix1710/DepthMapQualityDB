# REGULAR imports
import pathlib2 as pathlib

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
# DJANGO imports
from django.shortcuts import render
from django.views.generic.list import ListView
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# LOCAL imports
from .forms import UploadMethodZipForm#, UploadZipForm
from .models import *
from .src.functions import *
from .tasks import process_the_depth_method#, process_the_sequence

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

##############################################
# multicolumn
# NEW METHOD VERSIONs

# addSequence - equivalent
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
            
            # depth_name = (str(form.cleaned_data['title'])).lower().replace(' ', '_')
            depth_name = str(form.cleaned_data['method_name'])
            
            # UNZIP DATA and process depths in order to obtain PSNR and bitrate results
            # try:
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
            # except MethodProposal.DoesNotExist:
            #     print("ERROR: uploaded method wasn't saved!")
            # except:
            #     print("SOME ERROR...")
            # finally:
            return HttpResponseRedirect('../methods')
    else:
        form = UploadMethodZipForm()
        
    return render(request, TEMPLATE_PATH + 'depth_form.html', {'form': form})

QUERY_BASE = '''SELECT met.id, met.method_name, met.desc, met.src,
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
        else:
            print('ERROR: No such value in sorting form!')
        
        qs += ORDER_STRING + ",".join(order_fields)
        
    RESULTS = MethodProposal.objects.raw(qs)
    
    context = {'est_methods': RESULTS}
    
    return render(request, TEMPLATE_PATH + 'depth_est_methods.html', context=context)
    

def testing(request):
    
    ############ TEMP data
    # obj = SequenceModel.objects.get(id=9)
    # processPSNR(obj, str(obj.src))
    ############ EOF TEMP data
    
    methodID = SeqDepthResult.objects.all()
    if(request.method == 'GET' and request.GET.__contains__('process')):

        value = request.GET.__getitem__('process')
        
        if(value == 'methods'):
            #inserting MODEL records to the database
            method1 = MethodProposal(method_name = 'A**', desc = 'This is simple text', src = '/src/Poznan/12')
            method2 = MethodProposal(method_name = 'AAA', desc = 'New simple text to be different', src = '/src/Poznan/34')
            method3 = MethodProposal(method_name = 'PanapiRapis_s', desc = 'The other text that shook the Creator', src = '/src/Poznan/46')
            
            method1.save()
            method2.save()
            method3.save()
        elif(value == 'sequences'):
            seq1 = Sequence(seq_name = 'PoznanFencing', seq_src = 'seq_src/thisSeq11')
            seq2 = Sequence(seq_name = 'Carpark', seq_src = 'seq_src/thisSeq22')
            
            seq1.save()
            seq2.save()
        elif(value == 'depths'):
            # for i in range(1,25):
            #     SeqDepthResult.objects.filter(pk=i).delete()
            
            #########################################################
            # WHAT'S THAT QUERY: getting_all_objects.WHERE_method_name=sth.retrieve_value_list_of_PK[get_first_element]      <-- REMEMBER: only one element will be in the table!!
            methodID1 = MethodProposal.objects.get(pk=MethodProposal.objects.all().extra(where=["method_name='A**'"]).values_list("pk", flat=True)[0])
            # WHAT'S THAT QUERY: getting_values_of_SEQ_ID.WHERE_seq_name=sth.retrieve_first_element_which_is_dictionary
            seqID1 = Sequence.objects.get(pk=Sequence.objects.values('id').extra(where=["seq_name='PoznanFencing'"])[0]['id'])
            methodID2 = MethodProposal.objects.get(pk=MethodProposal.objects.values('method_id').extra(where=["method_name='AAA'"])[0]['id'])
            seqID2 = Sequence.objects.get(pk=Sequence.objects.values('id').extra(where=["seq_name='Carpark'"])[0]['id'])
            methodID3 = MethodProposal.objects.get(pk=MethodProposal.objects.values('method_id').extra(where=["method_name='PanapiRapis_s'"])[0]['id'])
            
            # TODO: depth1 gives ERRORs!!!
            depth1 = SeqDepthResult(method_id = methodID1, seq_id = seqID1, synth_PSNR_1018 = 23.54, synth_bitrate_1018 = 87.76, synth_PSNR_3042 = 28.47, synth_bitrate_3042 = 24.89, synth_PSNR_none = 90.34, synth_bitrate_none = 11.42)
            depth1.save()
            depth2 = SeqDepthResult(method_id = methodID1, seq_id = seqID2, synth_PSNR_1018 = 73.35, synth_bitrate_1018 = 345.73, synth_PSNR_3042 = 37.82, synth_bitrate_3042 = 99.23, synth_PSNR_none = 3.535, synth_bitrate_none = 52.63)
            depth2.save()
            depth3 = SeqDepthResult(method_id = methodID2, seq_id = seqID1, synth_PSNR_1018 = 132.451, synth_bitrate_1018 = 4.12, synth_PSNR_3042 = 75.1234, synth_bitrate_3042 = 7.32, synth_PSNR_none = 78.23, synth_bitrate_none = 35.34)
            depth3.save()
            depth4 = SeqDepthResult(method_id = methodID2, seq_id = seqID2, synth_PSNR_1018 = 12.1212, synth_bitrate_1018 = 31121.12, synth_PSNR_3042 = 143.12, synth_bitrate_3042 = 765.4, synth_PSNR_none = 88.54, synth_bitrate_none = 41.86)
            depth4.save()
            depth5 = SeqDepthResult(method_id = methodID3, seq_id = seqID2, synth_PSNR_1018 = 623.1234, synth_bitrate_1018 = 634.23, synth_PSNR_3042 = 99.73, synth_bitrate_3042 = 45.73, synth_PSNR_none = 73.23, synth_bitrate_none = 2.00)
            depth5.save()
            depth6 = SeqDepthResult(method_id = methodID3, seq_id = seqID1, synth_PSNR_1018 = 65.65, synth_bitrate_1018 = 3.04, synth_PSNR_3042 = 5.24, synth_bitrate_3042 = 62.16, synth_PSNR_none = 846.24, synth_bitrate_none = 34.345)
            depth6.save()
            
    # methodID = MethodProposal.objects.get(pk=MethodProposal.objects.values('method_id').extra(where=["method_name='AAA'"])[0]['method_id'])
    
    # seqID = Sequence.objects.get(pk=Sequence.objects.values('seq_id').extra(where=["seq_name='Carpark'"])[0]['seq_id'])
    
    # print("METHOD:", methodID)
    # print("SEQ:", seqID)
    
    
    # for i in range(31, 37):
    #     SeqDepthResult.objects.get(depth_id=i).delete()
    
    
    # displaying multiple tables in one view
    methods = MethodProposal.objects.all()
    sequences = Sequence.objects.all()
        
    # depths = SeqDepthResult.objects.all()
    
    # TODO: rethink displaying FK data: i.e. instead seq_id -> display its name
    # depths = SeqDepthResult.objects.filter(method_id=methodID).values()
    depths = SeqDepthResult.objects.all()
    
    # TODO: adding columns matching queryset (seq_names in depths)
    # depth_seq = Sequence.get_seq_name(methodID)
    
    
    ######################################
    # overall depth results table
    # results = MethodProposal.objects.select_related('seqdepthresult').values(
    #     'seqdepthresult__synth_PSNR_1018', 'seqdepthresult__synth_PSNR_3042', 'seqdepthresult__synth_PSNR_none').annotate(
            
    #         seq_id=FilteredRelation(
    #             'sequence', condition=Q(sequence__seq_name='PoznanFencing'),
    #         )
    #     )
    results = MethodProposal.objects.raw('''SELECT met.id, met.method_name, met.desc, 
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
                                                            WHERE seq_name = 'Carpark')''')
    
    # display keys available in this custom QUERY        
    # print(results[0].__dict__.keys())
    
    ###############
    ###############

    # depth_method = MethodProposal.objects.get(method_name = 'XXXXX')

    # mul_process_data(depth_method, str(depth_method.src))
    
    init_methods = MethodProposal.objects.all()
    
    join_res1 = SeqDepthResult.objects.all().select_related('method_id')
    
    sec_res = SeqDepthResult.objects.all().values('method_id', 'seq_id', 'synth_PSNR_1018').filter(seq_id = Sequence.objects.get(seq_name = 'Carpark'))
    
    print(type(init_methods))
    print(join_res1)
    print(type(sec_res))
    
    ###############
    ###############
    
    # print(depths)
    context = {'methods' : methods, 'sequences' : sequences, 'depths' : depths, 'results': results}

    return render(request, TEMPLATE_PATH + 'testing.html', context=context)

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