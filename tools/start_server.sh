#!/bin/bash
# @Project:       Tier 2 Support Task Automation Portal
# @Version:       0.1
# @Author:        Oleg Snegirev <ol.snegirev@gmail.com>
# @Functionality: T2 Portal startup script

echo "Make sure MySQL DB is running..."
if [ ! "$(service mysql status |grep start/running)"]; then
    service mysql start
fi

echo "Starting T2 Portal..."
python manage.py runserver 0.0.0.0:8000