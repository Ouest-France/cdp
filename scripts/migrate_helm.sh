#/bin/bash

NAMESPACE=
RELEASE=
usage() { echo "Usage: $0 -n <namespace> -r <release>" 1>&2; exit 4; }

while getopts "n:r:" option; do
    case "${option}" in
        n)
            NAMESPACE=${OPTARG};;
        r)
            RELEASE=${OPTARG};;
        *)
            usage
            ;;
    esac
done

if [ "$RELEASE" == "" -o "$NAMESPACE" == "" ]; then
   usage
fi

RELEASEV2=$(helm2 --tiller-namespace ${NAMESPACE} list -q "^${RELEASE}$")
if [ ! $? -eq 0 ]; then
   echo "Erreur dans la migration de la release ${RELEASE}"
   exit 2
fi
if [ "$RELEASEV2" != "" ]; then

   # Migration release
   helm3 2to3 convert -t ${NAMESPACE} ${RELEASE}
   if [ ! $? -eq 0 ]; then
      echo "Erreur dans la migration de la release ${RELEASE}"
      exit 2
   fi
  
   RELEASEV3=$(helm3 list -qn ${NAMESPACE} -f "^${RELEASE}$")
   if [  ! $? -eq 0 -o "$RELEASEV3" == "" ]; then
      echo "Erreur dans la migration de la release ${RELEASE}"
      exit 3
   fi
   echo "Release $2 migree en Helm3"
   exit 1
fi
