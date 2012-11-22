#!/bin/bash
set -e
LOGFILE=$VIRTUAL_ENV/var/log/gunicorn/thingstream.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=6
# user/group to run as
USER=garnold
GROUP=garnold
cd $VIRTUAL_ENV/thingstream
source $VIRTUAL_ENV/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec $VIRTUAL_ENV/bin/gunicorn_django -w $NUM_WORKERS \
  -k gevent --user=$USER --group=$GROUP --log-level=info \
  --log-file=$LOGFILE 2>>$LOGFILE
