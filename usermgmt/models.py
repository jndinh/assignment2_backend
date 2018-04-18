# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=20, null=False, blank=False, unique=True)
	password = models.CharField(max_length=20, null=False, blank=False)
	latitude = models.FloatField(blank = True, null = True)
	longitude = models.FloatField(blank = True, null = True)
	timestamp = models.BigIntegerField(blank = True, null = True)
