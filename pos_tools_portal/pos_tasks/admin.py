# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Task
from .models import RESTTask
from .models import Parameter
from .models import Header
from .models import Environment

# Register your models here.
admin.site.register(Task)
admin.site.register(RESTTask)
admin.site.register(Parameter)
admin.site.register(Header)
admin.site.register(Environment)
