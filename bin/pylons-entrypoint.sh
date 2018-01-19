#!/bin/sh
set -e


# wait for servers to come up
# /opt/ckan/wait-for-it.sh  :5432 -t 20
#/opt/ckan/wait-for-it.sh  redis:6379 -t 40

# wait a bit more
sleep 5

# Install pylons
cd /usr/lib/pylons/default/src/pylons
pylons-pip install -q -e .

# run migrations and initialize database
. /usr/lib/pylons/default/bin/activate
elx-migration -c pylons/conf/production.ini upgrade head

exec "$@"
