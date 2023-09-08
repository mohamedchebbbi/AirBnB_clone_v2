#!/usr/bin/python3
"""
Fabric script based on file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
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
import os.path
# do_pack = __import__('1-pack_web_static').do_pack
# do_deploy = __import__('2-do_deploy_web_static').do_deploy
env.hosts = ['54.208.28.27', '54.157.170.238']


def do_pack():
    """ pack my static"""
    try:
        if not os.path.exists('versions'):
            l = local("mkdir -p versions")
        n = "versions/web_static_{}.tgz".\
            format(time.strftime("%Y%m%d%H%M%S", time.gmtime()))
        o = local("tar -cvzf {} web_static".format(n))
        # x = local("mv {} versions".format(n))
        # p = local("pwd {}".format(n))
        # return 'versions/{}'.format(n)
        return n
    except:
        return None


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


path = do_pack()


def deploy():
    """ pack and deploy """
    if path:
        return do_deploy(path)
    else:
        return False
