#!/bin/sh

## Do whatever you need with env vars here ...
if [ `grep -P '(\t| )docker( |\t|$)' /etc/hosts | wc -l` -eq 1 ]; then
  export DOCKER_HOST="tcp://docker:2375";
else
  export DOCKER_HOST="tcp://localhost:2375";
fi

# Hand off to the CMD
exec "$@"
