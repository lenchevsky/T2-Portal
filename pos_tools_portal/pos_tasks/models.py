# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests, os
import json
import ssl
import jenkins
import hipchat_v2
from django.db import models
from subprocess import Popen, PIPE
from time import sleep
from string import Template
from django.conf import settings
import logging

log = logging.getLogger(__name__)

# Create your models here.
class Environment(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50)
    jenkins_url = models.URLField(max_length=250)
    jenkins_user = models.CharField(max_length=50)
    jenkins_token = models.CharField(max_length=50)

    hipchat_url = models.URLField(max_length=250)
    hipchat_token = models.CharField(max_length=250)
    hipchat_room = models.IntegerField()

    snow_url = models.URLField(max_length=250)
    snow_user = models.CharField(max_length=50)
    snow_token = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Environment"
        verbose_name_plural = "Environments"



class Parameter(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50)
    default_value = models.CharField(max_length=150, blank=True)
    TYPES = (
        ('DEFAULT','Default Parameter'),
        ('URL','URL Parameter'),
        ('HEADER','Header Parameter'),
    )
    param_type = models.CharField(max_length=20, choices=TYPES, default='DEFAULT',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task Parameter"
        verbose_name_plural = "Task Parameters"


class Header(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=150, blank=True)
    header = models.CharField(max_length=240)
    executable = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task Header"
        verbose_name_plural = "Task Headers"


class SimpleTask(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    active = models.BooleanField()
    parameters = models.ManyToManyField(Parameter)
    environment = models.ForeignKey(Environment, on_delete=None)

    def notify_hipchat(self, text, text_type):
        ssl._create_default_https_context = ssl._create_unverified_context
        # Post a message to a HipChat room
        hipchat_server = self.environment.hipchat_url
        hipchat_room_id = self.environment.hipchat_room
        hipchat_token = self.environment.hipchat_token
        hipchat = hipchat_v2.HipChat(url=hipchat_server)
        hipchat.message_room(
  			room_id=hipchat_room_id,
  			message=text,
  			color=text_type,
  			token=hipchat_token,
  			notify=True)

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

        # Start building ExecutionResult object
        result = ExecutionResult()
        result.task = self
        result.user_signature = '%s %s [%s]' % (request.user.first_name, request.user.last_name, request.user.username)
        
        # Logging
        log.info("Calling % s..." % self.description)
        
        # Parsing task paramerets
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
                elif (item[0]=='snow_number'):
                    result.snow_number = item[1]

        if self.rest_json_template:
            data_json = Template(self.rest_json_template).substitute(json_params)
        else:
            data_json = ''

        headers_dic = {"User-Agent": "script",}
        for h in self.rest_headers.all():
            headers_dic[h.name] = h.header
        headers_dic.update(header_params)
        request_url = Template(self.rest_url).substitute(url_params)

        log.debug(request_url, headers_dic, data_json)

        try:
            if (self.rest_method == 'POST'):
                r = requests.post(
                    url=request_url, 
                    headers=headers_dic, 
                    data=json.dumps(data_json), 
                    verify=False)
                if r.status_code == 200:
                    log.info("Successfull call: [%s]" % r.content)
                    result.is_successful = True
                    result.output = str(r.content)
                else:
                    log.warning("Failure: %s" % r.content)
                    result.is_successful = False
                    result.output = str(r.content)
            elif (self.rest_method == 'GET'):
                r = requests.get(
                    url=request_url, 
                    headers=headers_dic, 
                    verify=False)
                if r.status_code == 200:
                    log.info("Successfull call: [%s]" % r.content)
                    result.is_successful = True
                    result.output = str(r.content)
                else:
                    log.warning("Failure: %s" % r.content)
                    result.is_successful = False
                    result.output = str(r.content)
            elif (self.rest_method == 'PUT'):
                r = requests.put(
                    url=request_url,
                    headers=headers_dic,
                    data=json.dumps(data_json),
                    verify=False)
                if r.status_code == 200:
                    log.info("Successfull call: [%s]" % r.content)
                    result.is_successful = True
                    result.output = str(r.content)
                else:
                    log.warning("Failure: %s" % r.content)
                    result.is_successful = False
                    result.output = str(r.content)
            elif (self.rest_method == 'PATCH'):
                r = requests.patch(
                    url=request_url,
                    headers=headers_dic,
                    data=json.dumps(data_json),
                    verify=False)
                if r.status_code == 200:
                    log.info("Successfull call: [%s]" % r.content)
                    result.is_successful = True
                    result.output = str(r.content)
                else:
                    log.warning("Failure: %s" % r.content)
                    result.is_successful = False
                    result.output = str(r.content)
            elif (self.rest_method == 'DELETE'):
                r = requests.delete(
                    url=request_url,
                    headers=headers_dic,
                    verify=False)
                if r.status_code == 200:
                    log.info("Successfull call: [%s]" % r.content)
                    result.is_successful = True
                    result.output = str(r.content)
                else:
                    log.warning("Failure: %s" % r.content)
                    result.is_successful = False
                    result.output = str(r.content)

        except requests.exceptions.RequestException as e:
            log.error('Request error: '+str(e))
            result.is_successful = False
            result.output = str(e)
        
        result.save()

        # Broadcasting to HipChat
        host = ''
        for env in settings.ENVIRONMENTS:
            if env['default']:
                host = env['url']
        self.notify_hipchat(("%s is executing task '% s' at %s/history/%s/..." % (request.user.get_full_name(),self.name,host,result.id)),('green' if result.is_successful else 'yellow'))


    class Meta:
        verbose_name = "REST Task"
        verbose_name_plural = "REST Tasks"
    

class Task(SimpleTask):
    jenkins_job_name = models.CharField(max_length=240, default='POS')

    def call_api(self, request):

        # Start building ExecutionResult object
        result = ExecutionResult()
        result.task = self
        result.user_signature = '%s %s [%s]' % (request.user.first_name, request.user.last_name, request.user.username)
        result.jenkins_job_name = self.jenkins_job_name

        # Logging
        log.info("Calling % s..." % self.description)
        
        # Parsing task paramerets
        data_dic = {}
        form_params = request.POST
        for key, val in form_params.items():
            data_dic[key] = val 
        log.debug("Task parameters are %s" % data_dic)
        result.snow_number = data_dic['snow_number']

        # Run Jenkins Job and save buid number
        server = jenkins.Jenkins(self.environment.jenkins_url, username=self.environment.jenkins_user, password=self.environment.jenkins_token)
        result.jenkins_build_number = server.get_job_info(self.jenkins_job_name)['nextBuildNumber']
        server.build_job(self.jenkins_job_name, data_dic)    
    
        # Try to get first results
        try:    
            # Wait 10 seconds so the build may start
            sleep(10)
            build_info = server.get_build_info(result.jenkins_job_name, int(result.jenkins_build_number))
        
            result.is_successful = (True if build_info['building']=='True' else (True if build_info['result']=='SUCCESS' else False))
            result.output = ("Job is building..." if build_info['building']=='True' else server.get_build_console_output(self.jenkins_job_name, int(result.jenkins_build_number)))
        except Exception:
            result.is_successful = False
            result.output = "Jenkins job has not been started"
            log.warning("Jenkins job has not been started")
            pass

        result.save()

        # Broadcasting to HipChat
        host = ''
        for env in settings.ENVIRONMENTS:
            if env['default']:
                host = env['url']
        self.notify_hipchat(("%s is executing task '% s' at %s/history/%s/..." % (request.user.get_full_name(),self.name,host,result.id)),('green' if result.is_successful else 'yellow'))

    class Meta:
        verbose_name = "Jenkins Task"
        verbose_name_plural = "Jenkins Tasks"


class ExecutionResult(models.Model):
    objects = models.Manager()
    task = models.ForeignKey(SimpleTask, null=True)
    is_successful = models.BooleanField()
    output = models.CharField(max_length = 500, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user_signature = models.CharField(max_length = 250, default= 'System')
    jenkins_job_name = models.CharField(max_length=240, default='None', null=True)
    jenkins_build_number = models.CharField(max_length=10, default='0', null=True)
    snow_number = models.CharField(max_length=50, null=True)

    def get_previous(self):
        return self.get_previous_by_date().id

    def refresh_results(self):
        log.info("Getting the last data from Jenkins")
        server = jenkins.Jenkins(self.task.environment.jenkins_url, username=self.task.environment.jenkins_user, password=self.task.environment.jenkins_token)
        build_info = server.get_build_info(self.jenkins_job_name, int(self.jenkins_build_number))
        self.is_successful = (True if build_info['result']=='SUCCESS' else False)
        self.output = server.get_build_console_output(self.jenkins_job_name, int(self.jenkins_build_number))


