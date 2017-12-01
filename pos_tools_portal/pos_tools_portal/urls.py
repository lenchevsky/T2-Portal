"""pos_tools_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from pos_tasks import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.allTasksIndex, name='all_index'),
    url(r'^health/', views.healthIndex, name='health_index'),
    url(r'^tsk/(?P<task_id>[0-9]+)/$', views.taskFormIndex, name='task_form'),
    url(r'^rtsk/(?P<task_id>[0-9]+)/$', views.rtaskFormIndex, name='rtask_form'),
    url(r'^history/(?P<result_id>[0-9]+)/$', views.historyIndex, name='histoty_page'),
    url(r'^tsk/(?P<task_id>[0-9]+)/result/$', views.resultIndex, name='result_form'),
    url(r'^rtsk/(?P<task_id>[0-9]+)/result/$', views.restResultIndex, name='rest_result_form'),
]
