#!/usr/bin/python3
"""Script that generates a .tgz archive from the contents
 of the web_static folder of AirBnB Clone repo"""
from fabric.api import local, task, env, put, run  # Import the task decorator
from datetime import datetime
import os

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


def do_deploy(archive_path):
    """
    Distributes an archive to web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        True if all operations have been done correctly, otherwise False.
    """
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

        result = run(f'mkdir -p /data/web_static/releases/{filename}')
        if result.failed:
            return False
        # Upload the .tgz file to /tmp directory on the remote server
        result = put(f'{archive_path}', '/tmp')
        if result.failed:
            return False

        # Extract the uploaded .tgz file to
        # /data/web_static/releases/<filename> directory
        result = run(f'tar -xzf /tmp/{filename}.tgz -C \
                     /data/web_static/releases/{filename}')
        if result.failed:
            return False

        # Remove the uploaded .tgz file from /tmp directory
        result = run(f'mv  /data/web_static/releases/{filename}/web_static/* \
                      /data/web_static/releases/{filename}/')
        result = run(f'rm /tmp/{filename}.tgz')
        result = run(f'rm -rf \
            /data/web_static/releases/{filename}/web_static/')
        if result.failed:
            return False

        # Remove the current symlink
        result = run(f'rm -rf /data/web_static/current')
        if result.failed:
            return False

        # Create a symlink to the newly deployed version
        result = run(f'ln -s /data/web_static/releases/{filename}\
    /data/web_static/current')
        if result.failed:
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
