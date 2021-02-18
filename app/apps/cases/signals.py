import logging
import sys

from apps.camunda.services import CamundaService
from apps.cases.models import Case
from apps.openzaak.helpers import create_open_zaak_case
from celery import shared_task
from django.db import transaction
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Case, dispatch_uid="case_init_in_camunda")
def create_case_instance_in_camunda(sender, instance, created, **kwargs):
    if created and "test" not in sys.argv:

        @shared_task(bind=True, default_retry_delay=10)
        def start_instance(self, identification):
            camunda_id = CamundaService().start_instance(
                case_identification=identification
            )
            instance.camunda_id = camunda_id
            instance.save()

        task = start_instance.s(identification=instance.identification).delay
        transaction.on_commit(task)


@receiver(post_save, sender=Case)
def create_case_instance_in_openzaak(sender, instance, created, **kwargs):
    if created and "test" not in sys.argv:
        try:
            create_open_zaak_case(
                identification=instance.identification, description=instance.description
            )
        except Exception as e:
            logger.error(e)
