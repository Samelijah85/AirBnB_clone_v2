#!/usr/bin/python3
"""Script that generates a .tgz archive from the contents
 of the web_static folder of AirBnB Clone repo"""
from fabric.api import local, task, env  # Import the task decorator
from datetime import datetime

env.hosts = ['ubuntu@54.88.80.89', 'ubuntu@54.160.119.162']


def do_pack():
    """
    Creates a tgz archive from the contents of web_static.

    Returns:
        Archive path, otherwise None
    """
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(date)
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.succes:
        print("web_static packed: {}".format(archive_path))
        return archive_path
    return None
