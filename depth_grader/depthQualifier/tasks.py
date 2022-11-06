# depthQualifier/tasks.py

from celery import shared_task

from .models import SequenceModel
from .src.functions import batchSynthesis, zipUnpack, processPSNR

# MATEUSZ
@shared_task
def process_the_sequence(seq_id):          # arguments in this function need to be serializable (i.e. string, int, etc.)
    seq = SequenceModel.objects.get(id=seq_id)
    zipUnpack(str(seq.src))
    batchSynthesis(seq)
    processPSNR(seq, str(seq.src))