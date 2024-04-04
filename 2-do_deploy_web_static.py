#!/usr/bin/python3
"""Script that generates a .tgz archive from the contents
 of the web_static folder of AirBnB Clone repo"""
from fabric.api import local, task, env, put, run  # Import the task decorator
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


def do_deploy(path):
    """ distributes an
    archive to your web servers, using the function do_deploy"""
    # Ensure path is provided
    if not path:
        return False
    else:
        # Extract the base filename without the .tgz extension
        run(f'filename=$(basename -s .tgz {path})')

        # Upload the .tgz file to /tmp directory on the remote server
        put(f'{path}', '/tmp')

        # Extract the uploaded .tgz
        # file to /data/web_static/releases/<filename> directory
        run(f'tar -xvzf /tmp/$filename.tgz -C\
            /data/web_static/releases/$filename')

        # Remove the uploaded .tgz file from /tmp directory
        run(f'rm /tmp/$filename.tgz')

        # Remove the current symlink
        run(f'rm /data/web_static/current')

        # Create a symlink to the newly deployed version
        run(f'ln -s /data/web_static/releases/$filename \
            /data/web_static/current')
