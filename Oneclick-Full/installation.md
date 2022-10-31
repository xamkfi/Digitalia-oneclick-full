# Installation instructions
These instructions are created for, and tested on Ubuntu 20.04 server. Other Ubuntu / Debian versions might also work

## prequisites
- Installed Ubuntu server 20.04 with cli / ssh access
- Installed Docker (developed on 20.10.18)

## Installation procedure
1. Clone the repository https://gitlab.com/jaaskela79/oneclick-full
2. Open config.ini file inside oneclickSIPCreator folder and modify if needed, see the file for more instructions
    - **ip** and **port** to match your host ip and the port you wish to expose
    - **sipcreator** which is the name that will appear in the created SIP package
    - **detectlanguage** Detects the uploaded content language, either True of False 
    - **dovirusscan** Check the uploaded content for viruses, either True of False
    - **metadata** If you know that the to be uploaded content includes metadata inside xml files, name the files here and the content of those files will be checked if possible
3. Open the ports.conf file inside Oneclick-Full directory and modify the port to be the same than inside the config.ini file
4. Open the uploads.ini file and modify if needed. This can be used to change the upload file sizes and execution times.
4. Run the following commands inside Oneclick-Full directory

`docker build -t oneclick` 
- Builds and names the result as oneclick
    
`docker run -v /etc/localtime:/etc/localtime:ro -h somename.somedomain.net -d -p 8080:8080 oneclick` 
- Runs the compiled oneclick container, -v syncronizes the host machine time with the docker, -h gets rid of apache common name warning, -d run as deatached and -p exposes port 8080 to host

`docker ps`
- Check that the docker is actually running, output should be something similar to: *b1e03a8739a4   oneclick   "bash /app/oneclickS…"   59 minutes ago   Up 59 minutes   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   boring_chandrasekhar*

5. When the docker is up and running, fire up your browser and enter http://yourip:yourport/oneclickUploader/uploader-main.php 
    - in my development machine the full path is http://10.25.36.72:8080/oneclickUploader/uploader-main.php
