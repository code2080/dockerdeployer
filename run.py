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
                        generate_django_requirements


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
        if not os.path.isdir(app_dir):
            subprocess.Popen(['git', 'clone', app["git_repo"], app_dir, '--depth=1'])


def build():
    generate_dotenv()
    generate_database_initial()
    generate_nginx_config()
    generate_docker_compose()
    generate_django_settings()
    generate_django_requirements()


def dev_up():
    os.system('docker-compose up --build')


def prod_up():
    # os.system('docker-compose -f docker-compose.yml -f docker-compose.background.yml up --build -d')
    os.system('docker-compose up --build -d')


def stop():
    os.system('docker stop dockerdeployer_webserver_1')
    os.system('docker stop dockerdeployer_database_1')
    config = get_config()
    apps = config["apps"]
    for app in apps:
        os.system('docker stop dockerdeployer_{}_1'.format(app["name"]))


def clean():
    os.system('docker rmi -f $(docker images -f dangling=true -q)')


def reset():
    os.system('docker rmi -f $(docker images -f dangling=true -q)')
    config = get_config()
    apps = config["apps"]

    os.system('docker stop dockerdeployer_webserver_1')
    os.system('docker stop dockerdeployer_database_1')
    for app in apps:
        os.system('docker stop dockerdeployer_{}_1'.format(app["name"]))

    os.system('docker rm dockerdeployer_webserver_1')
    os.system('docker rm dockerdeployer_database_1')
    for app in apps:
        os.system('docker rm dockerdeployer_{}_1'.format(app["name"]))

    os.system('docker volume rm dockerdeployer_mysql')
    os.system('docker volume rm dockerdeployer_www')


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'clone':
            clone()
        elif sys.argv[1] == 'build':
            build()
        elif sys.argv[1] == 'dev.up':
            dev_up()
        elif sys.argv[1] == 'prod.up':
            prod_up()
        elif sys.argv[1] == 'stop':
            stop()
        elif sys.argv[1] == 'clean':
            clean()
        elif sys.argv[1] == 'reset':
            reset()

if __name__ == '__main__':
    main()
