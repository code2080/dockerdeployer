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
                        generate_django_requirements, \
                        generate_nodejs_package


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
            subprocess.Popen(['git', 'clone', app["git_repo"], app_dir, app["name"], '--depth=1'])


def build():
    generate_dotenv()
    generate_database_initial()
    generate_nginx_config()
    generate_docker_compose()
    generate_django_settings()
    generate_django_requirements()
    generate_nodejs_package()


def dev_up():
    os.system('docker-compose up --build')


def prod_up():
    # os.system('docker-compose -f docker-compose.yml -f docker-compose.background.yml up --build -d')
    os.system('docker-compose up --build -d')


def stop():
    os.system('docker stop dode_webserver')
    os.system('docker stop dode_database')
    config = get_config()
    apps = config["apps"]
    for app in apps:
        os.system('docker stop dode_{}'.format(app["name"]))


def clean():
    os.system('docker rmi -f $(docker images -f dangling=true -q)')


def clear():
    config = get_config()
    apps = config["apps"]

    # Stop containers
    os.system('docker stop dode_webserver')
    os.system('docker stop dode_database')
    for app in apps:
        os.system('docker stop dode_{}'.format(app["name"]))

    # Remove containers
    os.system('docker rm dode_webserver')
    os.system('docker rm dode_database')
    for app in apps:
        os.system('docker rm dode_{}'.format(app["name"]))

    # Remove images
    os.system('docker rmi -f $(docker images -f dangling=true -q)')

    
def reset():
    config = get_config()
    apps = config["apps"]

    # Stop containers
    os.system('docker stop dode_webserver')
    os.system('docker stop dode_database')
    for app in apps:
        os.system('docker stop dode_{}'.format(app["name"]))

    # Remove containers
    os.system('docker rm dode_webserver')
    os.system('docker rm dode_database')
    for app in apps:
        os.system('docker rm dode_{}'.format(app["name"]))

    # Remove volumes
    os.system('docker volume rm dode_mysql')
    servers = {}
    for app in config["apps"]:
        servers[app["server"]] = servers.get(app["server"], []) + [app]
    for server in servers:
        os.system('docker volume rm dode_root_directory_{}'.format(server.replace(".", "_").replace(":", "_")))

    # Remove images
    os.system('docker rmi -f $(docker images -f dangling=true -q)')
    for app in apps:
        os.system('docker rmi dode_{}'.format(app["name"]))


def restart(app_name):
    os.system('docker restart dode_{}'.format(app_name))


def backup(app_name):
    MYSQL_INIT_DIR = os.path.join(BASE_DIR, 'backups')
    if not os.path.isdir(MYSQL_INIT_DIR):
        os.mkdir(MYSQL_INIT_DIR)

    config = get_config()
    apps = config["apps"]
    app = None
    for a in apps:
        if a["name"] == app_name:
            app = a
    if app:
        os.system('docker exec dode_database /usr/bin/mysqldump -u {} --password={} {} > backup/{}_backup.sql'.format(config["mysql"]["user"], config["mysql"]["password"], app["database_name"], app["name"]))


def restore(app_name, backup_path):
    config = get_config()
    apps = config["apps"]
    app = None
    for a in apps:
        if a["name"] == app_name:
            app = a
    if app:
        os.system('cat {} | docker exec -i dode_database /usr/bin/mysql -u {} --password={} {}'.format(backup_path, config["mysql"]["user"], config["mysql"]["password"], app["database_name"]))


def main():
    if len(sys.argv) >= 2:
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
        elif sys.argv[1] == 'clear':
            clear()
        elif sys.argv[1] == 'reset':
            reset()
        elif sys.argv[1] == 'restart':
            restart(sys.argv[2])
        elif sys.argv[1] == 'backup':
            backup(sys.argv[2])
        elif sys.argv[1] == 'restore':
            restore(sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()
