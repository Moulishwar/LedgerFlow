from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.services import get_or_create_party_ledger
from parties.models import Party


@receiver(post_save, sender=Party)
def create_party_ledger(sender, instance, created, **kwargs):
    if created:
        get_or_create_party_ledger(instance)
