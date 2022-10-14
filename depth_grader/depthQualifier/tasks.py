# depthQualifier/tasks.py

from celery import shared_task

from depth_grader.depthQualifier.src.functions import batchSynthesis, zipUnpack


@shared_task
def process_the_sequence(seq):
    zipUnpack(str(seq.src))
    batchSynthesis(seq)