# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings
from .models import Task, RESTTask, ExecutionResult, Environment
from urlparse import urlparse
import socket
import logging

log = logging.getLogger(__name__)

def is_service_available(host,port):
    result = False
    try:
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con.settimeout(2)
        is_available = con.connect_ex((host,port))
        if is_available == 0:
            result = True
    except socket.error:
        result = False
    return result

def check_jenkins_availability():
    result = None
    list = ""
    all_environments = Environment.objects.all()
    for environment in all_environments:
        if (not is_service_available(urlparse(environment.jenkins_url).hostname, urlparse(environment.jenkins_url).port)):
            list = list + urlparse(environment.jenkins_url).hostname + ' '

    if len(list)>0:
        result =  "WARNING! It looks like some of external services are not available. \n Affected hosts are: %s" % list
    return result


def healthIndex(request):
    return HttpResponse("Hello, world. You're at Tasks index.")

def statusIndex(request,date):
    results = ExecutionResult.objects.filter(date__gt=date)
    log.debug(results)
    context = {'result_records': results}
    return render(request, 'status.html', context)

def resultIndex(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.call_api(request)
    return redirect('all_index')

def restResultIndex(request, task_id):
    task = RESTTask.objects.get(pk=task_id)
    task.call_api(request)
    return redirect('all_index')

def allTasksIndex(request):
    # List all Tasks found
    all_jenkins_tasks = Task.objects.all()
    all_rest_tasks = RESTTask.objects.all()
    default_env = {}
    for env in settings.ENVIRONMENTS:
        if env['default']:
            default_env = env
    context = {'task_list': all_jenkins_tasks, 
                'rtask_list': all_rest_tasks, 
                'message': check_jenkins_availability(), 
                'env_list': settings.ENVIRONMENTS,
                'default_env': default_env}
    return render(request, 'tlist.html', context)


@login_required
def historyIndex(request, result_id):
    result = ExecutionResult.objects.get(pk=result_id)
    if result.jenkins_job_name != 'None':
        result.refresh_results()
        result.save()
    context = {'result_record': result}  
    return render(request, 'history.html', context)


@login_required
def taskFormIndex(request, task_id):

    class TaskForm(forms.Form):
        def __init__(self,*args,**kwargs):
            task_id = kwargs.pop('task_id')
            super(TaskForm, self).__init__(*args, **kwargs)
            task_params = Task.objects.get(pk=task_id)
            for param in task_params.parameters.all():
                self.fields[param.name] = forms.CharField(max_length=50, label=param.name, initial=param.default_value)
            self.fields['snow_number'] = forms.CharField(max_length=50, label='Service Now Incident', initial='')

    
    task_selected = Task.objects.get(id=task_id)
    context = {'task': task_selected, "form" : TaskForm(task_id = task_id), 'message': check_jenkins_availability()}
    return render(request, 'tform.html', context)


@login_required
def rtaskFormIndex(request, task_id):

    class TaskForm(forms.Form):
        def __init__(self,*args,**kwargs):
            task_id = kwargs.pop('task_id')
            super(TaskForm, self).__init__(*args, **kwargs)
            task_params = RESTTask.objects.get(pk=task_id)
            for param in task_params.parameters.all():
                self.fields[param.name] = forms.CharField(max_length=50, label=param.name, initial=param.default_value)
            self.fields['snow_number'] = forms.CharField(max_length=50, label='Service Now Incident', initial='')

    
    task_selected = RESTTask.objects.get(id=task_id)
    context = {'task': task_selected, "form" : TaskForm(task_id = task_id)}
    return render(request, 'tform.html', context)
