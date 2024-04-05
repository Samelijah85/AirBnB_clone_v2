#!/usr/bin/python3
"""
Script that generates a .tgz archive from the contents of the web_static
folder of AirBnB Clone repo
"""
from fabric.api import local
from datetime import datetime
import os.path


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
