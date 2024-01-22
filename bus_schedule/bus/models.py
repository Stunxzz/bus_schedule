from django.db import models

# Create your models here.


class ScheduleModel(models.Model):
    excel = models.FileField(upload_to="",)


