from django.http import HttpResponse
from django.shortcuts import render
from scheduler.models import Task
from scheduler.models import Log
import pandas as pd
from golf_todo.forms import TaskForm
import requests
import json
import time
import urllib.request
from json import dumps
from datetime import date, timedelta, datetime
import os
import csv

  #changing python env to EST time
os.environ['TZ'] = 'America/New_York'
time.tzset()

def weatherApi(now):
  current_weather = "https://api.weatherapi.com/v1/forecast.json?key=54e7336c726549aea0c175718212410&q=48906&days=2&aqi=no&alerts=no"
  with urllib.request.urlopen(current_weather) as current_weather:
    data = json.loads(current_weather.read().decode())

  date_all = []
  date = []
  time = []
  chance_rain = []
  for entry in data['forecast']['forecastday']:
    for hour in entry['hour']:
      date_all.append(hour['time'].split(' ')[0])
      time.append(int(hour['time'].split(' ')[1].split(':')[0]))
      chance_rain.append(hour['chance_of_rain'])

#data for only next 12 hours, weatherapi sends 24hr data for 2days requested
  next_12_hrs = now + timedelta(hours=12)
  next_12_hr = int(next_12_hrs.hour)
  cur_hr = int(now.hour)

  if int(next_12_hrs.day) > int(now.day):
    next_12_hr_idx = next_12_hr + 24
  else:
    next_12_hr_idx = next_12_hr

  time_12hrs = time[time.index(cur_hr):next_12_hr_idx]
  chance_rain_12hrs = chance_rain[time.index(cur_hr):next_12_hr_idx]

  day_avgdata = data['forecast']['forecastday'][0]['day']

  context = {
    'time': time_12hrs,
    'chance_rain': chance_rain_12hrs,
    'test': next_12_hr_idx,
    'day_avgdata': day_avgdata,
  }

  return(context)

def home(request):
  current_time = datetime.now()
  check_time = date.today()
  tomorrow = check_time + timedelta(days=1)
  
  weather = weatherApi(current_time)

  if request.method == 'POST':
    form = TaskForm(request.POST)

    if (isinstance(int(request.POST['id']),int)):
      task_to_update = Task.objects.get(id=int(request.POST['id']))
      task_to_update.next_due_date = timedelta(days=task_to_update.frequency_days) + check_time
      task_to_update.save()

      new_entry = Log.objects.create(
        task = task_to_update.task,
        hole = task_to_update.hole,
        date_completed = check_time,
      )
      new_entry.save()

  else:
    form = TaskForm()

  dun_time = check_time - timedelta(days=2)
  log_entries = Log.objects.filter(date_completed__gte=dun_time).order_by('-date_completed')
  tasks = Task.objects.filter(next_due_date__lte=tomorrow)
  context = {

      'tasks': tasks,
      'form': form,
      'logs': log_entries,
      'time': weather['time'],
      'chance_rain': weather['chance_rain'],
      'maxtemp': weather['day_avgdata']['maxtemp_f'],
      'mintemp': weather['day_avgdata']['mintemp_f'],
      'humidity': weather['day_avgdata']['avghumidity'],
      'desc': weather['day_avgdata']['condition']['text'],
  }
  
  return render(request, 'index.html', context=context)


def log(request):

  if request.method == 'POST':
    form = TaskForm(request.POST)

    if (isinstance(int(request.POST['id']),int)):
      task_to_update = Task.objects.get(id=int(request.POST['id']))
      task_to_update.frequency_days = int(request.POST['freq-input'])
      task_to_update.save()

  else:
    form = TaskForm()

  log_entries = Log.objects.all().order_by('-date_completed')
  context = { 
    'logs': log_entries,
    }
  
  return render(request, 'log.html', context=context)

def export(request):
  # Create the HttpResponse object with the appropriate CSV header.
  response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="RSG_Task_Log.csv"'},
    )

  writer = csv.writer(response)

  for entry in Log.objects.all():
    writer.writerow([entry.task, entry.hole,entry.date_completed])

  return response

def tasks(request):
  tasks = Task.objects.all()
  context = { 
    'tasks': tasks,
    }
  
  return render(request, 'task.html', context=context)


'''
def getForecast():
  hourly_forecast = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/329381?apikey=MR2VVK6jYPJ7ZvS5c9R1tA7HszjSt7xM&details=true"
  temps = []
  humidity = []
  time = []
  precipitation = []
  rain = []
  prec_hr_data = []

  with urllib.request.urlopen(hourly_forecast) as hourly_forecast:
    data = json.loads(hourly_forecast.read().decode())
    for hour_data in data:
      temps.append(hour_data["Temperature"]["Value"])
      humidity.append(hour_data["RelativeHumidity"])
      time.append(hour_data["DateTime"])
      precipitation.append(hour_data["PrecipitationProbability"])
      rain.append(hour_data["Rain"]["Value"])
  
  hours = []

  for idx, timestamp in enumerate(time):
    timestamp = timestamp.split("T")[1].split("-")[0].split(":")[0]
    hours.append(int(timestamp))

  context = {
    'temps': temps,
    'humidity': humidity,
    'rain': rain,
    'None': 'None',
    'time': hours,
    'prec_hourly': dumps(precipitation),
  }

  return(context)

def getCurrentWeather():
  current_weather = "http://dataservice.accuweather.com/currentconditions/v1/329381?apikey=MR2VVK6jYPJ7ZvS5c9R1tA7HszjSt7xM&details=true"
  with urllib.request.urlopen(current_weather) as current_weather:
    data = json.loads(current_weather.read().decode())

    context = {
      'temp': data[0]['Temperature']['Imperial']['Value'],
      'humidity': data[0]['RelativeHumidity'],
      'prec': data[0]['PrecipitationType'],

    }
  return(context)

  hourly_forecast_dict = getForecast()
  current_weather_dict = getCurrentWeather()

  forecast_dict = weatherApi(current_time)
  for key, value in forecast_dict:
    forecast_dict[key]['date-time'] = forecast_dict[key]['date']

      'hour_temps': hourly_forecast_dict['temps'],
      'humidity': hourly_forecast_dict['humidity'],
      'prec_hourly': hourly_forecast_dict['prec_hourly'],
      'cur_temp': current_weather_dict['temp'],
      'cur_hum': current_weather_dict['humidity'],
      'prec': current_weather_dict['prec'],
      'time': hourly_forecast_dict['time'],

'''