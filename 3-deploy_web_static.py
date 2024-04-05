#!/usr/bin/python3
"""
Script that generates a .tgz archive from the contents
of the web_static folder of AirBnB Clone repo
"""
from fabric.api import local, env, put, run
from datetime import datetime
import os.path

env.hosts = ['ubuntu@54.88.80.89', 'ubuntu@54.160.119.162']


def do_pack():
    """
    Creates a tgz archive from the contents of web_static.

    Returns:
        Archive path, otherwise None
    """
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(date)
    print("Packing web_static to {}".format(archive_path))
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(archive_path)).failed is True:
        return None
    print("web_static packed: {} -> {}Bytes".format(
        archive_path,
        os.path.getsize(archive_path)
        )
    )
    return archive_path


def do_deploy(archive_path):
    """
    Distributes an archive to web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        True if all operations have been done correctly, otherwise False.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    print('New version deployed!')
    return True


def deploy():
    """
    Create and distribute an archive to web servers.

    Returns:
        False if no archive has been created, otherwise the return value
        of do_deploy.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
