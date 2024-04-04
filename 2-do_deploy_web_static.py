#!/usr/bin/python3
"""Script that generates a .tgz archive from the contents
 of the web_static folder of AirBnB Clone repo"""
from fabric.api import local, task, env, put, run  # Import the task decorator
from datetime import datetime
import os

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


def do_deploy(archive_path):
    """ distributes an
    archive to your web servers, using the function do_deploy"""
    # Ensure path is provided
    if not archive_path:
        return False
    else:
        # Extract the base filename without the .tgz extension
        base_name = os.path.basename(archive_path)
        # Split the base name into root and extension (e.g.,
        # 'web_static_20240404115939', '.tgz')
        filename, _ = os.path.splitext(base_name)
        # result = run(f'filename=$(basename -s .tgz {archive_path})')
        # if result.failed:
        #     return False

        # Upload the .tgz file to /tmp directory on the remote server
        result = put(f'{archive_path}', '/tmp')
        if result.failed:
            return False

        # Extract the uploaded .tgz file to
        # /data/web_static/releases/<filename> directory
        result = run(f'tar -xvzf /tmp/{filename}.tgz -C \
                     /data/web_static/releases/$filename')
        if result.failed:
            return False

        # Remove the uploaded .tgz file from /tmp directory
        result = run(f'rm /tmp/{filename}.tgz')
        if result.failed:
            return False

        # Remove the current symlink
        result = run(f'rm /data/web_static/current')
        if result.failed:
            return False
        run(f'echo {filename}')

        # Create a symlink to the newly deployed version
        result = run(f'ln -s /data/web_static/releases/{filename}\
    /data/web_static/current')
        if result.failed:
            return False

        return True
