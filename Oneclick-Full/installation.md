# Installation instructions
These instructions are created for, and tested on Ubuntu 20.04 server. Other Ubuntu / Debian versions might also work

## prequisites
- Installed Ubuntu server 20.04 with cli / ssh access
- Installed Docker (developed on 20.10.18)
    - [Installing Docker on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

## Installation procedure
1. Clone the repository https://gitlab.com/jaaskela79/oneclick-full
2. Open config.ini file inside oneclickSIPCreator folder and modify it to match your environment, more details inside the file
    - **ip** and **port**: Match your host ip and the port you are going to use
    - **sipcreator**: the name that will appear in the created SIP package metadata
    - **detectlanguage**: Detects the uploaded content language, (True or False)
    - **dovirusscan**: Check the uploaded content for viruses before processing, (True or False)
    - **metadata**: If you know that the to be uploaded content includes metadata inside xml files, name these files here and those will be separated into a specific original metadata folder inside the created SIP package.
3. Open the ports.conf file inside Oneclick-Full directory and modify the port to be the same as in the config.ini file
4. Open the uploads.ini file and modify if needed. This can be used to change the upload limitis and execution times. Also any other container php settings can be altered via this file. You just have to know what to add.
4. Run the following commands inside Oneclick-Full directory

`docker build -t oneclick` 
- Builds and names the resulting container as oneclick
- Note that the first build takes minutes to complete
    
`docker run -v /etc/localtime:/etc/localtime:ro -h somename.somedomain.net -d -p 8080:8080 oneclick` 
- Runs the compiled oneclick container 
    - -v syncronizes the host machine time with the docker (if this is not defined the creation time in SIP:s   will be wrong), 
    - -h gets rid of apache common name warning (can safely be omitted), 
    - -d runs in deatached mode and 
    - -p exposes container port 8080 to host port 8080

`docker ps`
- Check that the docker is actually running, output should be something similar than 
    - *b1e03a8739a4   oneclick   "bash /app/oneclickS…"   59 minutes ago   Up 59 minutes   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   boring_chandrasekhar*

5. When the docker is up and running, fire up your browser and enter http://yourip:yourport/oneclickUploader/uploader-main.php 
    - in my development machine the full path is http://10.25.36.72:8080/oneclickUploader/uploader-main.php which obviously doesn't work for you thus being developed inside a vpn network
6. Upload things to be added into a SIP package. For more information related to this, see the tutorial video
