from django.db import models

from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save

# Create your models here.

class Type(models.Model):
	shortcode = models.CharField('ShortCode', max_length=50, unique=True) ## -- Slug / shortcode / quick-word for the Type -- ##
	display = models.CharField('Display', max_length=50, blank=True, null=True) ## -- Front end display of the Type -- ##
	severity = models.CharField('Severity', max_length=50, blank=True, null=True) ## -- Severity of the Type (high / medium / low) -- ##
	group = models.CharField('Group', max_length=50, blank=True, null=True) ## -- Group the type comes under -- ##
	configurable_counts	= models.TextField(max_length=2000) ## -- Minimum counts on a Type per Day / Person -- ##

	class Meta:
		app_label = 'types_vio'
		#ordering = ('shortcode',) ## -- Order By 'shortcode' -- ##