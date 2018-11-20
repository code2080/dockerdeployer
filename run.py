#!/usr/bin/python
import os
import sys
import json
import subprocess

from generators import generate_dotenv, \
                        generate_database_initial, \
                        generate_nginx_config, \
                        generate_docker_compose, \
                        generate_django_settings, \
                        generate_requirements


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')


def get_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.loads(f.read())


def clone():
    config = get_config()
    apps = config["apps"]
    for app in apps:
        app_dir = os.path.join(PARENT_DIR, app["name"])
        subprocess.Popen(['git', 'clone', app["git_repo"], app_dir, '--depth=1'])


def build():
    generate_dotenv()
    generate_database_initial()
    generate_nginx_config()
    generate_docker_compose()
    generate_django_settings()
    generate_requirements()


def up():
    # os.system('docker-compose -f docker-compose.yml -f docker-compose.background.yml up --build -d')
    os.system('docker-compose up --build')


def clean():
    os.system('docker rmi -f $(docker images -f dangling=true -q)')


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'clone':
            clone()
        elif sys.argv[1] == 'build':
            build()
        elif sys.argv[1] == 'up':
            up()
        elif sys.argv[1] == 'clean':
            clean()

if __name__ == '__main__':
    main()
