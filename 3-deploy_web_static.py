#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from
the contents of the web_static folder of your
AirBnB Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime
from os.path import isdir
from os.path import exists
env.hosts = ['18.233.64.33', '18.204.10.26']


def do_pack():
    """ generates a .tgz archive from the contents of the web_static """
    try:
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_name = "versions/web_static_{}.tgz".format(current_time)
        if isdir("versions") is False:
            local("mkdir versions")
        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except Exception as e:
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        file_no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run("mkdir -p {}{}/".format(path, file_no_ext))
        run("tar -xzf /tmp/{} -C {}{}/".format(file_name, path, file_no_ext))
        run("rm /tmp/{}".format(file_name))
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, file_no_ext))
        run("rm -rf {}{}/web_static".format(path, file_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(path, file_no_ext))
        return True
    except Exception as e:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive = do_pack()
    if archive is None:
        return False
    new_archive = do_deploy(archive)
    return new_archive
