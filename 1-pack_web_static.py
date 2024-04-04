#!/usr/bin/python3
"""Script that generates a .tgz archive from the contents
 of the web_static folder of AirBnB Clone repo"""
from fabric.api import local, task, env  # Import the task decorator
from datetime import datetime

env.hosts = ['ubuntu@34.204.81.253', 'ubuntu@52.87.154.218']


def do_pack():
    """generates a .tgz archive from th"""
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(date)
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.succes:
        print("web_static packed: {}".format(archive_path))
        return archive_path
    return None
