# depthQualifier/tasks.py

from celery import shared_task

from .models import MethodProposal
from .src.functions import mul_zip_unpack, mul_batch_synthesis, mul_process_data

# TODO: TO DELETE
# MATEUSZ
# @shared_task
# def process_the_sequence(seq_id):          # arguments in this function need to be serializable (i.e. string, int, etc.)
#     seq = SequenceModel.objects.get(id=seq_id)
#     print("SRC:", seq.src)
    # zipUnpack(str(seq.src))
    # batchSynthesis(seq)
    # processPSNR(seq, str(seq.src))
    
##############################################
# multicolumn

# MATEUSZ
@shared_task
def process_the_depth_method(method_id):
    depth_method = MethodProposal.objects.get(id=method_id)
    mul_zip_unpack(str(depth_method.src))          # probably DONE
    mul_batch_synthesis(depth_method)              # probably DONE
    # processing PSNR and bitrate data METHOD
    # mul_process_data(depth_method, str(depth_method.src))