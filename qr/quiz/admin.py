from django.contrib import admin

# Register your models here.
from django.db.models.base import ModelBase
from . import models as models_quiz

for name, var in models_quiz.__dict__.items():
    if type(var) is ModelBase:
        admin.site.register(var)