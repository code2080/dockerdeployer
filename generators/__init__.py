import os
import json
from shutil import copyfile
from jinja2 import Environment, FileSystemLoader


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
CONFIG_FILE = os.path.join(PARENT_DIR, 'config.json')
DOTENV_FILE = os.path.join(PARENT_DIR, '.env')

def get_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.loads(f.read())


def generate_dotenv():
    config = get_config()
    vars = [
        ("MYSQL_USER", config["mysql"]["user"]),
        ("MYSQL_ROOT_PASSWORD", config["mysql"]["password"]),
        ("DJANGO_ADMIN_USERNAME", config["django"]["djang_admin"]["username"]),
        ("DJANGO_ADMIN_PASSWORD", config["django"]["djang_admin"]["password"]),
        ("DJANGO_ADMIN_EMAIL", config["django"]["djang_admin"]["email"]),
        ("PYTHONPATH", "/settings/"),
    ]
    with open(DOTENV_FILE, 'w') as f:
        for var in vars:
            f.write("{}={}\n".format(var[0], var[1]))


def generate_database_initial():
    config = get_config()
    env = Environment(loader=FileSystemLoader(BASE_DIR))
    template = env.get_template('template.init_database.py')

    MYSQL_INIT_DIR = os.path.join(PARENT_DIR, 'django')
    if not os.path.isdir(MYSQL_INIT_DIR):
        os.mkdir(MYSQL_INIT_DIR)

    with open(os.path.join(MYSQL_INIT_DIR, 'init_database.py'), 'w') as f:
        f.write(template.render(apps=config["apps"]))


def generate_nginx_config():
    config = get_config()
    env = Environment(loader=FileSystemLoader(BASE_DIR))
    template = env.get_template('template.nginx.conf')

    servers = {}
    for app in config["apps"]:
        servers[app["server"]] = servers.get(app["server"], []) + [app]

    with open(os.path.join(PARENT_DIR, 'nginx', 'config', 'conf.d', 'default.conf'), 'w') as f:
        f.write(template.render(
            servers=servers,
            customize_nginx=config["customize_nginx"]))


def generate_docker_compose():
    config = get_config()
    env = Environment(loader=FileSystemLoader(BASE_DIR))
    template = env.get_template('template.docker-compose.yml')

    servers = {}
    ports = []
    for app in config["apps"]:
        servers[app["server"]] = servers.get(app["server"], []) + [app]
        ports.append(app["server"].split(":")[1])
    ports = list(set(ports))

    with open(os.path.join(PARENT_DIR, 'docker-compose.yml'), 'w') as f:
        f.write(template.render(
            mysql_version=config["mysql"]["version"],
            gunicorn_version=config["django"]["gunicorn_version"],
            apps=config["apps"],
            servers=servers,
            ports=ports))


def generate_django_settings():
    config = get_config()
    env = Environment(loader=FileSystemLoader(BASE_DIR))
    template = env.get_template('template.settings.py')

    apps = config["apps"]
    for app in apps:
        if app["type"] == "django":
            with open(os.path.join(PARENT_DIR, 'django', 'settings_{}.py'.format(app["name"])), 'w') as f:
                f.write(template.render(
                    app_name=app["name"],
                    db_name=app["database_name"],
                    db_usr=config["mysql"]["user"],
                    db_pwd=config["mysql"]["password"],
                    host=app["server"].split(":")[0],
                    settings=app["settings"]))


def generate_django_requirements():
    config = get_config()
    env = Environment(loader=FileSystemLoader(BASE_DIR))
    template = env.get_template('template.requirements.txt')

    apps = config["apps"]
    for app in apps:
        if app["type"] == "django":
            with open(os.path.join(os.path.dirname(PARENT_DIR), app["name"], 'requirements.txt'), 'r') as f_in:
                with open(os.path.join(PARENT_DIR, 'django', 'requirements_{}.txt'.format(app["name"])), 'w') as f_out:
                    f_out.write(template.render(requirements=f_in.read()))


def generate_nodejs_package():
    config = get_config()

    apps = config["apps"]
    for app in apps:
        if app["type"] == "nodejs":
            copyfile(
                os.path.join(os.path.dirname(PARENT_DIR), app["name"], 'package.json'),
                os.path.join(PARENT_DIR, 'nodejs', 'package_{}.json'.format(app["name"]))
            )
