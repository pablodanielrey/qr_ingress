from django.db import models

import uuid
import datetime

# Create your models here.

class ExternalUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100)
    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    username = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    idnumber = models.CharField(max_length=500)


class Access(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ExternalUser, on_delete=models.CASCADE)
    qrcode = models.CharField(max_length=2048)
    date_readed = models.DateTimeField(default=datetime.datetime.utcnow())
    sync_to_server = models.DateTimeField(null=True)


class Blacklisted(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ExternalUser, on_delete=models.CASCADE)
    date_blacklisted = models.DateTimeField(default=datetime.datetime.utcnow())