# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests, os
import json
import jenkins
from django.db import models
from subprocess import Popen, PIPE
from time import sleep
from string import Template

# Create your models here.
class Project(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50)
    jenkins_url = models.URLField(max_length=250)
    jenkins_user = models.CharField(max_length=50)
    jenkins_token = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Parameter(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50)
    default_value = models.CharField(max_length=150, blank=True)
    TYPES = (
        ('DEFAULT','Default Parameter'),
        ('URL','URL Parameter'),
        ('HEADER','Header Parameter'),
    )
    param_type = models.CharField(max_length=6, choices=TYPES, default='DEFAULT',)

    def __str__(self):
        return self.name

class Header(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=150, blank=True)
    header = models.CharField(max_length=240)
    executable = models.BooleanField()

    def __str__(self):
        return self.name


class SimpleTask(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    active = models.BooleanField()
    parameters = models.ManyToManyField(Parameter)
    project = models.ForeignKey(Project, on_delete=None)

    def __str__(self):
        return self.name


class RESTTask(SimpleTask):
    rest_url = models.CharField(max_length=255)
    METHODS = (
        ('GET','GET'),
        ('POST','POST'),
        ('PUT','PUT'),
        ('PATCH','PATCH'),
        ('DELETE','DELETE'),
    )
    rest_method = models.CharField(max_length=6, choices=METHODS, default='GET',)
    rest_headers = models.ManyToManyField(Header)
    rest_json_template = models.CharField(max_length=500, null=True, blank=True)

    def call_api(self, request):
        print "Calling % s..." % self.description
        
        json_params = {}
        url_params = {}
        header_params = {}

        for item in request.POST.items():
            for p in self.parameters.all():
                if (item[0]==p.name) and (p.param_type=='DEFAULT'):
                    json_params[item[0]] = item[1]
                elif (item[0]==p.name) and (p.param_type=='URL'):
                    url_params[item[0].replace(" ", "_")] = item[1]
                elif (item[0]==p.name) and (p.param_type=='HEADER'):
                    header_params[item[0]] = item[1]

        if self.rest_json_template:
            data_json = Template(self.rest_json_template).substitute(json_params)
        else:
            data_json = ''

        headers_dic = {"User-Agent": "script",}
        for h in self.rest_headers.all():
            headers_dic[h.name] = h.header
        headers_dic.update(header_params)
        request_url = Template(self.rest_url).substitute(url_params)

        print request_url, headers_dic, data_json
        try:
            if (self.rest_method == 'POST'):
                r = requests.post(
                    url=request_url, 
                    headers=headers_dic, 
                    data=json.dumps(data_json), 
                    verify=False)
                if r.status_code == 200:
			        print "Successfull call: [%s]" % r.content
                else:
			        print "Failure: %s" % r.content
            elif (self.rest_method == 'GET'):
                r = requests.get(
                    url=request_url, 
                    headers=headers_dic, 
                    verify=False)
                if r.status_code == 200:
			        print "Successfull call: [%s]" % r.content
                else:
			        print "Failure: %s" % r.content
            elif (self.rest_method == 'PUT'):
                r = requests.put(
                    url=request_url,
                    headers=headers_dic,
                    data=json.dumps(data_json),
                    verify=False)
                if r.status_code == 200:
			        print "Successfull call: [%s]" % r.content
                else:
			        print "Failure: %s" % r.content
            elif (self.rest_method == 'PATCH'):
                r = requests.patch(
                    url=request_url,
                    headers=headers_dic,
                    data=json.dumps(data_json),
                    verify=False)
                if r.status_code == 200:
			        print "Successfull call: [%s]" % r.content
                else:
			        print "Failure: %s" % r.content
            elif (self.rest_method == 'DELETE'):
                r = requests.delete(
                    url=request_url,
                    headers=headers_dic,
                    verify=False)
                if r.status_code == 200:
			        print "Successfull call: [%s]" % r.content
                else:
			        print "Failure: %s" % r.content

        except requests.exceptions.RequestException as e:
		    print('Request error: '+str(e))
    

class Task(SimpleTask):
    jenkins_job_name = models.CharField(max_length=240, default='POS')

    def call_api(self, request):
        result = ExecutionResult()
        form_params = request.POST
        print "Calling % s..." % self.description

        data_dic = {}
        for key, val in form_params.items():
            data_dic[key] = val 

        print data_dic
        server = jenkins.Jenkins(self.project.jenkins_url, username=self.project.jenkins_user, password=self.project.jenkins_token)
        result.jenkins_build_number = server.get_job_info(self.jenkins_job_name)['nextBuildNumber']
        server.build_job(self.jenkins_job_name, data_dic)
        
        result.is_successful = True
        result.output = "TEST"
        result.task = self
        result.user_signature = '%s %s [%s]' % (request.user.first_name, request.user.last_name, request.user.username)
        result.jenkins_job_name = self.jenkins_job_name
        result.save()


class ExecutionResult(models.Model):
    objects = models.Manager()
    task = models.ForeignKey(Task, null=True)
    is_successful = models.BooleanField()
    output = models.CharField(max_length = 500)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user_signature = models.CharField(max_length = 250, null=True)
    jenkins_job_name = models.CharField(max_length=240, default='POS', null=True)
    jenkins_build_number = models.CharField(max_length=10, default='1', null=True)

    def refresh_results(self):
        print "Getting the last data from Jenkins"
        server = jenkins.Jenkins(self.task.project.jenkins_url, username=self.task.project.jenkins_user, password=self.task.project.jenkins_token)
        sleep(5)
        return server.get_build_console_output(self.jenkins_job_name, int(self.jenkins_build_number))


