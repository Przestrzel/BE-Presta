# Udemy2 with Prestashop

Project for Electronic bussiness - Prestashop

# How to use

After starting the server with

> docker-compose up -d

you should be able to connect to:

-   presta -> on port 80
-   phpmyadmin -> on port 8080

### Before starting to work on webshop you should

1. Check if there are changes on the repository.
2. Get up to date webshop with git pull.

#### Save your current working container as backup

1. Get the presta container id
    > docker ps -a
2. Commit docker container and
    > docker commit {presta_id} udemy2
3. Save file (remember to be in repo directory and to name it properly)
    > docker save udemy2 > udemy2-backup.gz
4. If necessery load file
    > docker load < udemy2-backup.gz

### Every change of the site should be pushed to the github repository.

1. Do the dump of the website.

    - go to /admindev
    - then zaawansowane/baza danych
    - kopia zapasowa DB
    - Download to the dbdump folder.

2. Commit and push the changes to the repository.

### Loading the files of presta to the repository

1. Get the presta container id
    > docker ps -a
2. Copy files from container
    > docker cp {presta_id}:/var/www/html ./udemy2dump
3. Copy files from /udemy2dump to /webshop

# Useful commands

Remove and/or stop your containers

> docker-compose down

Stop the container2. Get up to date webshop.

> docker-compose stop

# Bug fixes

### If there's no tables on udemy2 db (check on phpmyadmin)

1. Extract dbdump and add these commands on the start of the file.

    > DROP DATABASE IF EXISTS udemy2; <br />
    > CREATE DATABASE udemy2; <br />
    > USE udemy2; <br />

2. Delete cache and var/cache folders from webshop.

3. Rerun the prestashop.

### If something is old or not loaded

1. Delete cache and var/cache folders from webshop.

2. Rerun the prestashop.

### If you have got no permission

1. Go to presta container with command

    - docker container exec -it CONTAINER_ID /bin/bash
    - or with docker desktop.

2. Run the followin command
    - chmod -R 777 ./

### Links/Images do not work

1. Go to /admindev

2. Go to Preferencje/Ruch and toggle przyjazny adres URL.

3. If everything works now, do again the 2th step.
