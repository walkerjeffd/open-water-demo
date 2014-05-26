Open Water Data Platform
========================

This repo contains files for the Open Water Data Platform (which may be renamed at some point in the future). This is part of the Public Lab's [Open Water](http://publiclab.org/wiki/open-water) and [Riffle](http://publiclab.org/wiki/riffle) Projects.

## Overview

This application runs on flask and is configured for deployment to Heroku. Data files are stored on Amazon S3.

## Environmental Variables

Sensitive configuration settings must be set as environmental variables. These include:

FLASK_CONFIG: Config class, e.g. development, production, heroku. see config.py
DATABASE_URL: URI to database for SQLAlchemy
SECRET_KEY: Flask secret key
AWS_ACCESS_KEY_ID: Amazon AWS Access Key
AWS_SECRET_ACCESS_KEY: Amazon AWS Secret Key
S3_BUCKET: AWS S3 bucket name
MAIL_SERVER: SMTP server name
MAIL_PORT: SMTP port name
MAIL_USE_TLS: SMTP TLS option (True/False)
MAIL_USERNAME: SMTP username
MAIL_PASSWORD: SMTP password

## Development Server

To run a local web server:

    python manage.py runserver -d -r

To access the shell with bindings for app, db, and various Models

    python manage.py shell

To initialize the database

    python manage.py deploy

## Setting up Heroku

make sure Procfile contains this line:

    web: gunicorn manage:app

login to heroku, enter username and password

    heroku login

create application where <app_name> is the name of the heroku application (e.g. open-water-demo)

    heroku create <app_name>

add PostgreSQL database addon

    heroku addons:add heroku-postgresql:dev

promote PostgreSQL database (sets the URI to DATABASE_URL), note replace <COLOR>

    heroku pg:promote HEROKU_POSTGRESQL_<COLOR>_URL

set environmental variables on heroku (see above, do all *except* DATABASE_URL)

    heroku config:set NAME=value

make sure requirements.txt exists in top level, which Heroku uses to install dependencies

push to Heroku using git

    git push heroku master

run deploy command

    heroku run python manage.py deploy

restart heroku

    heroku restart

review logs

    heroku logs