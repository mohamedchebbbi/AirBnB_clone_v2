#!/usr/bin/python3
"""
Fabric script based on file 1-pack_web_static.py that distributes an
archive to the web servers
"""


from fabric.api import local
from fabric.api import get
from fabric.api import put
from fabric.api import reboot
from fabric.api import run
from fabric.api import sudo
from fabric.api import env
env.hosts = ['54.208.28.27', '54.157.170.238']


def do_deploy(archive_path):
    """ deploy my archive tgz into my servers """
    try:
        put(archive_path, '/tmp/')
        c1 = 'mkdir -p /data/web_static/releases/{}/'
        run(c1.format(archive_path[9:-4]))
        c2 = 'tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
        run(c2.format(archive_path[9:], archive_path[9:-4]))
        run('rm /tmp/{}'.format(archive_path[9:]))
        c3 = 'mv /data/web_static/releases/{}/web_static/* \
              /data/web_static/releases/{}/'
        run(c3.format(archive_path[9:-4], archive_path[9:-4]))
        c4 = 'rm -rf  /data/web_static/releases/{}/web_static/'
        run(c4.format(archive_path[9:-4]))
        run('rm -rf /data/web_static/current')
        c5 = 'ln -s /data/web_static/releases/{}/ {}'
        run(c5.format(archive_path[9:-4], '/data/web_static/current'))
        return True
    except:
        return False
