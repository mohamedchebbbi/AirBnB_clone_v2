#!/usr/bin/python3
"""
    delete files on server
"""
import time
from fabric.context_managers import cd
from fabric.api import local
from fabric.api import get
from fabric.api import put
from fabric.api import reboot
from fabric.api import run
from fabric.api import sudo
from fabric.api import env
env.hosts = ['54.208.28.27', '54.157.170.238']


def do_clean(number=0):
    """
        delete all files except most recent one, first if
        delete all files except two most recent one, else
    """
    if number == 0 or number == 1:
        local('ls -t /versions | tail -n +2 | xargs rm')
        run('ls -t /data/web_static/releases | tail -n +2 | xargs rm')
    else:
        local('ls -t /versions | tail -n +3 | xargs rm')
        run('ls -t /data/web_static/releases | tail -n +2 | xargs rm')
