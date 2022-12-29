# depthQualifier/tasks.py

from celery import shared_task

from .models import SequenceModel, MethodProposal
from .src.functions import batchSynthesis, zipUnpack, processPSNR, zipUnpack_m, batchSynthesis_m

# MATEUSZ
@shared_task
def process_the_sequence(seq_id):          # arguments in this function need to be serializable (i.e. string, int, etc.)
    seq = SequenceModel.objects.get(id=seq_id)
    print("SRC:", seq.src)
    # zipUnpack(str(seq.src))
    # batchSynthesis(seq)
    # processPSNR(seq, str(seq.src))
    
##############################################
# multicolumn

@shared_task
def process_the_depth_method(method_id):
    depth_method = MethodProposal.objects.get(id=method_id)
    zipUnpack_m(str(depth_method.src))          # probably DONE
    batchSynthesis_m(depth_method)              # probably DONE