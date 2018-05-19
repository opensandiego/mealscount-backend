# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Models for MealsCount Backend

# Model for a MealsCount School

class MC_SCHOOL(models.Model):
	school_name = models.CharField(max_length=200)
	total_number_of_students = models.IntegerField()
	identified_student_population = models.IntegerField()
	request = models.ForeignKey(MC_REQUEST, on_delete=models.PROTECT)

# Model for a MealsCount Request

class MC_REQUEST(models.Model):
	request_time = models.DateTimeField()
	pending = models.BooleanField()
	result = models.ForeignKey(MC_RESULT, on_delete=models.PROTECT, null=true)

# Model for a MealsCount Response

class MC_RESULT(models.Model):
	json_string = models.CharField(max_length=10000)