#!/bin/bash
# @Project:       Tier 2 Support Task Automation Portal
# @Version:       0.1
# @Author:        Oleg Snegirev <ol.snegirev@gmail.com>
# @Functionality: T2 Portal deployment script

echo "Make sure MySQL DB is running..."
if [ ! "$(service mysql status |grep start/running)"]; then
    service mysql start
fi

echo "Deploying PTP..."
python manage.py makemigrations --noinput    # Fetch DB changes
python manage.py migrate                     # Apply database migrations
python manage.py collectstatic --noinput     # Collect static files
python manage.py check
echo "Deployed"