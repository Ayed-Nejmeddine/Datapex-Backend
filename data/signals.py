"""Signals"""
from django.db.models.signals import post_init
from django.dispatch import receiver

from data.models.basic_models import Document


@receiver(post_init, sender=Document)
def post_init_document(sender, instance, **kwargs):
    """fill out all the fields of the document model"""
    if instance.id:
        instance.size = instance.document_path.size / 1024
        instance.name = instance.document_path.name
        instance.doc_type = instance.name.split(".")[-1]
        instance.save()
