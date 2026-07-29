from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.services import seed_company_accounts
from company.models import Company


@receiver(post_save, sender=Company)
def seed_new_company(sender, instance, created, **kwargs):
    if created:
        seed_company_accounts(instance)
