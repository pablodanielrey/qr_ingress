from django.db import models

import uuid
import logging
# Create your models here.

class Access(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    access = models.DateTimeField()

    firstname = models.CharField(max_length=1024, null=True)
    lastname = models.CharField(max_length=1024, null=True)
    username = models.CharField(max_length=1024, null=True)
    email = models.EmailField(null=True)
    number = models.CharField(max_length=1024, null=True)
    grade = models.CharField(max_length=500, null=True)
    timestamp = models.IntegerField()
    


class SyncModel:
    def __init__(self):
        pass
    
    def sync(self):
        for a in  Access.objects.all():
            logging.getLogger(self.__class__.__qualname__).info(f'sincronizando {a}')