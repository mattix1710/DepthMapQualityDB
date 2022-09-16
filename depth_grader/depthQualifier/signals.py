from django.db.models.signals import pre_save
from django.dispatch import receiver

from depth_grader.depthQualifier.models import SequenceModel

@receiver(pre_save, sender=SequenceModel)
def signal_handler(sender, instance, **kwargs):
    print("CURRENTLY ADDING NEW ELEMENT")
    print("INSTANCE:", instance)