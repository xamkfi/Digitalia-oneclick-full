#FROM continuumio/miniconda3 #Was tried as a ligher alternative but caused some problems
FROM continuumio/anaconda3

#Expose ports 
#EXPOSE 8080 #does not seem affect, exposing done on startup

WORKDIR /app/oneclickSIPCreator
#Basic update for the system
RUN apt-get -y update 
RUN apt-get -y upgrade

#Adds required repos
RUN apt install apt-transport-https lsb-release ca-certificates wget -y
RUN wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg 
RUN sh -c 'echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list'

#Takes new repositories into use
RUN apt-get -y update 
RUN apt-get -y upgrade
#Installs exiftool, apache and php --> cleans unneeded
RUN apt-get install -y --fix-missing exiftool php8.1 apache2 clamav clamav-daemon default-jre-headless
COPY docker-apache.conf /etc/apache2/conf-enabled/docker-apache.conf
COPY ports.conf /etc/apache2/ports.conf

#Installs nano for development purposes, will be commented on final release
#RUN apt-get install nano

#Updates clamav disabled for development thus multiple updates during one day causes temporary ban
RUN freshclam

#Updates conda environment and adds needed libraries
RUN conda update --all

RUN conda install -c conda-forge watchdog python-magic langdetect
RUN conda install -c anaconda beautifulsoup4
RUN pip install -U PyExifTool

COPY phpinfo.php /var/www/html
COPY uploads.ini /etc/php/8.1/apache2/conf.d
COPY oneclickUploader /var/www/html/oneclickUploader
COPY ./oneclickSIPCreator/config.ini /var/www/html/oneclickUploader

#Needed to be able to move the uploaded files to a uploads folder
RUN chown -R www-data:www-data /var/www/html/oneclickUploader
RUN service apache2 restart

COPY ./oneclickSIPCreator /app/oneclickSIPCreator/.

#Runs apache and python background
#CMD apachectl -D FOREGROUND 
#CMD ["python", "-u", "/app/oneclickSIPCreator/mainapp.py"]

COPY startup-script.sh /app/oneclickSIPCreator/startup-script.sh
ENTRYPOINT ["bash","/app/oneclickSIPCreator/startup-script.sh"]
