from django.db import models
from datetime import date, timedelta
from django.utils import timezone
from django.forms import ModelForm

class Task(models.Model):
  task = models.CharField(max_length=200)
  hole = models.CharField(max_length=200)
  frequency_days = models.IntegerField(default=2)
  next_due_date = models.DateField(default=timezone.now)

class Log(models.Model):
  task = models.CharField(max_length=200)
  hole = models.CharField(max_length=200)
  date_completed = models.DateField(default=(date.today() +timedelta(days = 100)))

class Equipment(models.Model):
  equipment_name = models.CharField(max_length=200)
  hours_used = models.IntegerField(default=0)

