from scheduler.models import Task
from scheduler.models import Log
from django.forms import ModelForm

class TaskForm(ModelForm):
  class Meta:
    model = Task
    fields = '__all__'

class LogForm(ModelForm):
  class Meta:
    model = Log
    fields = '__all__'