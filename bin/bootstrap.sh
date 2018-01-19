#!/bin/sh

abort() {
    echo >&2 "Aborted! An error occured. Exiting...\n"
}

trap 'abort' 0

set -eu

# define envvars
export VBOX_IPADDRESS="${VBOX_IPADDRESS}"
export VBOX_HOST_PORT="${VBOX_HOST_PORT}"


# process template files  to do env-var substitutions
cat ./bin/vagrantfile.rb.tmpl | envsubst > ./vagrantfile


trap : 0

echo >&2 "Done!"
