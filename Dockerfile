# @Project: 		Tier 2 Support Task Automation Portal
# @Version: 		0.1
# @Author:  		Oleg Snegirev <ol.snegirev@gmail.com>
# @Functionality:	Docker sandbox compilation 

FROM ubuntu:14.04
MAINTAINER Oleg Snegirev


# Install Python, MySQL and tools
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  mkdir /apps && chmod 777 /apps && \
  apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0xcbcb082a1bb943db && \
  echo "deb http://mariadb.mirror.iweb.com/repo/10.0/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/mariadb.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y byobu curl git htop man unzip vim wget libssl-dev libldap2-dev libsasl2-dev && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y mariadb-server libmariadbclient-dev python-mysqldb && \
  sed -i 's/^\(bind-address\s.*\)/# \1/' /etc/mysql/my.cnf && \
  echo "mysqld_safe &" > /tmp/config && \
  echo "mysqladmin --silent --wait=30 ping || exit 1" >> /tmp/config && \
  echo "mysql -e 'GRANT ALL PRIVILEGES ON *.* TO \"root\"@\"%\" WITH GRANT OPTION;'" >> /tmp/config && \
  bash /tmp/config && \
  rm -f /tmp/config && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*
  
#RUN mkdir /apps/ptp && mkdir /apps/ptp/tools

ADD pos_tools_portal /apps/ptp
ADD tools /apps/ptp/tools
WORKDIR /apps/ptp
EXPOSE 8000
EXPOSE 5672 
EXPOSE 3306
RUN pip install -r ./tools/requirements.txt
RUN chmod 777 ./tools/deploy_server.sh && chmod 777 ./tools/start_server.sh && ./tools/deploy_server.sh
CMD ./tools/start_server.sh