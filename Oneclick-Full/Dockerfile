FROM continuumio/miniconda3

#Expose ports
EXPOSE 3000

WORKDIR /app
#Basic update for the system
RUN apt-get -y update 
RUN apt-get -y upgrade

#Adds required repos
#RUN apt install lsb-release ca-certificates apt-transport-https software-properties-common -y
#RUN add-apt-repository ppa:ondrej/apache2
RUN apt install apt-transport-https lsb-release ca-certificates wget -y
RUN wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg 
RUN sh -c 'echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list'

#Takes new repositories into use
RUN apt-get -y update 
RUN apt-get -y upgrade
#Installs apache and php
RUN apt-get install -y apache2 && apt-get clean
RUN apt-get install -y php8.1
#Installs nano for development purposes, will be removed on final release
RUN apt-get install nano

#Exposes basic ports
EXPOSE 80
#Runs apache
CMD apachectl -D FOREGROUND

COPY phpinfo.php /var/www/html
COPY uploads.ini /etc/php/8.1/apache2/conf.d
COPY oneclickUploader /var/www/html/oneclickUploader
#Needed to be able to move the uploaded files to a uploads folder
RUN chown -R www-data:www-data /var/www/html/oneclickUploader

#COPY . /app/.
#CMD ["python", "/app/sample.py"] #Docker sallii vain yhden käynnistyskomennon
#CMD ["bash", "/app/startup-script.sh"] 
#siksi skripti jossa on kaksi käynnistyskomentoa
