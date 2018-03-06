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

${SUDO} pip install --upgrade --force-reinstall .

clean
