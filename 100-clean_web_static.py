from fabric.api import *
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = 'path_to_your_ssh_key'

def do_clean(number=0):
    """ Delete out-of-date archives """

    number = int(number)

    if number == 0:
        number = 1

    # Local cleanup in versions folder
    archives = sorted(os.listdir("versions"))
    archives_to_keep = archives[-number:]

    with lcd("versions"):
        for archive in archives:
            if archive not in archives_to_keep:
                local("rm ./{}".format(archive))

    # Remote cleanup in /data/web_static/releases
    releases = run("ls -tr /data/web_static/releases").split()
    releases = [r for r in releases if "web_static_" in r]
    releases_to_keep = releases[-number:]

    with cd("/data/web_static/releases"):
        for release in releases:
            if release not in releases_to_keep:
                run("rm -rf ./{}".format(release))

