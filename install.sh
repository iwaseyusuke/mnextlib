#!/usr/bin/env bash

SUDO=`which sudo`
${SUDO} echo '' > /dev/null

# Removes previous built files
clean ()
{
    ${SUDO} rm -rf \
        AUTHORS \
        ChangeLog \
        build/ \
        .eggs/ \
        mnextlib.egg-info/
}

clean

# Upgrade pip to the latest
${SUDO} pip install --upgrade pip

${SUDO} pip install --upgrade --force-reinstall .

clean
