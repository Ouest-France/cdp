#!/bin/sh

## Do whatever you need with env vars here ...
if [ `grep -P '(\t| )docker( |\t|$)' /etc/hosts | wc -l` == 1 ]; then
  export DOCKER_HOST="tcp://docker:2375"
fi
echo 'DOCKER_HOST: '.$DOCKER_HOST

# Hand off to the CMD
exec "$@"
