Open Water Data Platform
========================

## Environmental Variables

FLASK_CONFIG
DATABASE_URL
SECRET_KEY
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
MAIL_SERVER
MAIL_PORT
MAIL_USE_TLS
MAIL_USERNAME
MAIL_PASSWORD

Generate Flask Secret Key
>>> import os
>>> os.urandom(24)
'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

## Setting up Heroku

create Procfile

    web: gunicorn manage:app

login to heroku

    heroku login

create application

    heroku create <app_name>

add database

    heroku addons:add heroku-postgresql:dev

promote database (sets the URI to DATABASE_URL)

    heroku pg:promote HEROKU_POSTGRESQL_<COLOR>_URL

set environmental variables (see above, do all *except* DATABASE_URL)

    heroku config:set NAME=value

make sure requirements.txt exists in top level

test with foreman (first copy all environmental variables to .env file in top level)

    foreman start

upload with git

    git push heroku master

run deploy command

    heroku run python manage.py deploy

restart heroku

    heroku restart

review logs

    heroku logs