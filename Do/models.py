from django.db import models

# Create your models here.
class File_Filed(models.Model):
    file=models.FileField(null=True)