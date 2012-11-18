from django.db import models
from django.contrib.auth.models import User

#Signals for API keys:
from tastypie.models import create_api_key

#Add the post-save signal:
models.signals.post_save.connect(create_api_key, sender=User)

#Models
class TimeSeries(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    create_date = models.DateTimeField('date created')
