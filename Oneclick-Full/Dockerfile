#FROM continuumio/miniconda3
FROM continuumio/anaconda3

#Expose ports
EXPOSE 3000

WORKDIR /app
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
RUN apt-get install -y exiftool php8.1 apache2 clamav clamav-daemon
COPY docker-apache.conf /etc/apache2/conf-enabled/docker-apache.conf

#Installs nano for development purposes, will be removed on final release
RUN apt-get install nano

#Exposes basic ports
EXPOSE 80



COPY phpinfo.php /var/www/html
COPY uploads.ini /etc/php/8.1/apache2/conf.d
COPY oneclickUploader /var/www/html/oneclickUploader
#Needed to be able to move the uploaded files to a uploads folder
RUN chown -R www-data:www-data /var/www/html/oneclickUploader
RUN service apache2 restart

COPY ./oneclickSIPCreator /app/oneclickSIPCreator/.

#Updates conda environment and adds needed libraries
#RUN conda update --all
RUN conda install -c conda-forge watchdog python-magic langdetect
RUN conda install -c anaconda beautifulsoup4
RUN pip install -U PyExifTool

#Runs apache and python background
#CMD apachectl -D FOREGROUND && python ./app/oneclickSIPCreator/mainapp.py
CMD apachectl -D FOREGROUND


#CMD ["python", "/app/oneclickSIPCreator/mainapp.py"]
#CMD ["bash", "/app/startup-script.sh"] 
#siksi skripti jossa on kaksi käynnistyskomentoa
