Docker deployer for Django application, maybe static site or nodejs

# REQUIREMENTS

- Docker & Docker compose

`https://docs.docker.com/install/linux/docker-ce/ubuntu/
https://docs.docker.com/compose/install/`

- Python 3.x & Pip3

- Git

# SETUP

## Prepare for run.py

- Create your own python3 virtualenv then activate it

- On `dode` directory

`pip install -r requirements.txt`

## 1. Clone repos

`python run.py clone`

## 2. Build configs

`python run.py build`

## 3. Build and Run containers

- `python run.py dev.up` (foreground with logs)

- `python run.py prod.up`

# ROADMAP

- Work with private repos
- CI/CD
- SSL with letencrypt
- Support Redis, memcached, Elasticsearch...

