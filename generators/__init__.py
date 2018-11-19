import os
import json
from jinja2 import Environment, FileSystemLoader


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
CONFIG_FILE = os.path.join(PARENT_DIR, 'config.json')
DOTENV_FILE = os.path.join(PARENT_DIR, '.env')

ROOT_DIRECTORY = '/www/'
STATIC_DIRECTORY_NAME = 'static'
MEDIA_DIRECTORY_NAME = 'media'


def get_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.loads(f.read())


def generate_dotenv():
    config = get_config()
    vars = [
        ("ROOT_DIRECTORY", ROOT_DIRECTORY),
        ("STATIC_DIRECTORY_NAME", STATIC_DIRECTORY_NAME),
        ("MEDIA_DIRECTORY_NAME", MEDIA_DIRECTORY_NAME),
        # ("MYSQL_VERSION", config["mysql"]["version"]),
        # ("GUNICORN_VERSION", config["django"]["gunicorn_version"]),
        ("DJANGO_ADMIN_USERNAME", config["django"]["djang_admin"]["username"]),
        ("DJANGO_ADMIN_PASSWORD", config["django"]["djang_admin"]["password"]),
        ("DJANGO_ADMIN_EMAIL", config["django"]["djang_admin"]["email"]),
    ]
    with open(DOTENV_FILE, 'w') as f:
        for var in vars:
            f.write("{}={}\n".format(var[0], var[1]))


def generate_database_initial():
    config = get_config()
    env = Environment(loader=FileSystemLoader(BASE_DIR))
    template = env.get_template('template.database.sql')

    MYSQL_INIT_DIR = os.path.join(PARENT_DIR, 'mysql_init')
    if not os.path.isdir(MYSQL_INIT_DIR):
        os.mkdir(MYSQL_INIT_DIR)

    with open(os.path.join(MYSQL_INIT_DIR, '01-databases.sql'), 'w') as f:
        f.write(template.render(
            user=config["mysql"]["user"],
            password=config["mysql"]["password"],
            apps=config["apps"]))


def generate_nginx_config():
    config = get_config()
    env = Environment(loader=FileSystemLoader(BASE_DIR))
    template = env.get_template('template.nginx.conf')

    with open(os.path.join(PARENT_DIR, 'nginx', 'config', 'conf.d', 'default.conf'), 'w') as f:
        f.write(template.render(
            root_directory=ROOT_DIRECTORY,
            apps=config["apps"]))


def generate_docker_compose():
    config = get_config()
    env = Environment(loader=FileSystemLoader(BASE_DIR))
    template = env.get_template('template.docker-compose.yml')

    with open(os.path.join(PARENT_DIR, 'docker-compose.yml'), 'w') as f:
        f.write(template.render(
            root_directory=ROOT_DIRECTORY,
            mysql_version=config["mysql"]["version"],
            gunicorn_version=config["django"]["gunicorn_version"],
            apps=config["apps"]))
