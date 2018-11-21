Docker deployer for Django application

# INSTALLATION

0. Prepare

**Install Docker & Docker compose;**

`https://docs.docker.com/install/linux/docker-ce/ubuntu/
https://docs.docker.com/compose/install/`

**Install python requirements:**

`pip install -r requirements.txt`

1. Clone repos

`python run.py clone`

2. Build .env, nginx default.conf

`python run.py build`

3. Run docker

`python run.py up`

# ROADMAP

- Restart commands
- Django app envvar
- Improve nginx configuration
- Support Go & JS applications
- Import export database
- CI/CD
- Model abtract layer for Go & Django app
- SSL with letencrypt
- Support Redis, memcached, Elasticsearch...