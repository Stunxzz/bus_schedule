from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ScheduleModel
import os
from django.conf import settings


@receiver(post_save, sender=ScheduleModel)
def table_created(sender, instance, created, **kwargs):

    for obj in ScheduleModel.objects.all():
        if obj.excel.name != instance.excel.name:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, obj.excel.name))
                print(obj.excel.name)
                obj.delete()
            except:
                pass
