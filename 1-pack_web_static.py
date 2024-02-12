#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from
the contents of the web_static folder of your
AirBnB Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime
from os.path import isdir


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
