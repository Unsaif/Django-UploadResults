# To build the docker image:
# docker build -t vmh/uploadresults .
#
# To run the docker image exposing port 8003:
# docker run --network="host" -p 8003:8003 --rm -it vmh/uploadresults
# 
# --network="host" makes the host OS ports available inside 
# the container so that MySQL can be accessed from localhost
#
# To verify operation, from host OS visit http://localhost:8003
#
# To configure Apache2 as a reverse-proxy for this server on regular web
# port use the following virtual host configuration file:
#<VirtualHost *:80>
#	ServerName api.my.domain
#	ErrorLog ${APACHE_LOG_DIR}/error.log
#	CustomLog ${APACHE_LOG_DIR}/access.log combined
#	ProxyRequests On
#	ProxyPass / http://localhost:8003/
#	ProxyPassReverse / http://localhost:8003/
#</VirtualHost>
#

FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y unzip python3-pip mysql-client libmysqlclient-dev
RUN apt-get install -y python3-dev python3-mysqldb 
RUN pip3 install pymysql django
RUN pip3 install mysqlclient==2.0.3
RUN pip3 install pandas requests
WORKDIR /uploadresults
COPY . .
CMD python3 manage.py runserver 0.0.0.0:8003
