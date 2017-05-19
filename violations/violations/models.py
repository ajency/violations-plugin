from django.db import models

from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField

from types_vio.models import Type

class Violation(models.Model):
	vio_type = models.ForeignKey(Type, blank=True, null=True, default=None) ## -- Violation Type -- ##
	vio_date = models.DateTimeField(auto_now_add=True) ## -- Violation date -- ##
	who_id = models.IntegerField() ## -- Who Violated - ID -- ##
	who_type = models.CharField('Who Type', max_length=50, blank=True, null=True) ## -- Who violated - type -- ##
	who_meta = models.TextField(max_length=2000)#ArrayField(models.CharField(max_length=500), blank=True) ## -- Who violated - details -- ##
	whom_id = models.IntegerField() ## -- To Whom was it violated - id -- ##
	whom_type = models.CharField('Whom Type', max_length=50, blank=True, null=True) ## -- To Whom was it violated - type -- ##
	whom_meta = models.TextField(max_length=2000)#ArrayField(models.CharField(max_length=500), blank=True) ## -- To Whom was it violated - meta -- ##
	cc_list = ArrayField(models.IntegerField(), blank=True) ## -- cc_list - People who will evaluate - ID list -- ##
	cc_list_meta = ArrayField(models.TextField(max_length=2000), blank=True) ## -- cc_list - People who will evaluate - Meta list -- ##
	bcc_list = ArrayField(models.IntegerField(), blank=True) ## -- bcc_list - People who will evaluate - ID list -- ##
	bcc_list_meta = ArrayField(models.TextField(max_length=2000), blank=True) ## -- bcc_list - People who will evaluate - Meta list -- ##
	status = models.CharField('Status', max_length=50, blank=True, null=True) ## -- status of the Violation - (active / ignore / archive ) -- ##
	violation_nature = models.CharField('Violation Nature', max_length=50, blank=True, null=True) ## -- nature of the Violation - ( pre-violation / post-violation ) -- ##

	class Meta:
		app_label = 'violations'
		#ordering = ('shortcode',) ## -- Order By 'shortcode' -- ##