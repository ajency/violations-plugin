from django.db import models

from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.postgres.fields import HStoreField, ArrayField

from violations.models import Violation

# Create your models here.

class Comment(models.Model):
	violation = models.ForeignKey(Violation, blank=True, null=True, default=None, related_name='comments')
	who_id = models.IntegerField()
	who_meta = models.TextField(max_length=1000)#ArrayField(models.CharField(max_length=500), blank=True)
	comment = models.TextField('Comment', blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		app_label = 'comments'