{% for app in apps %}
CREATE DATABASE IF NOT EXISTS `{{ app.database_name }}`;
{% endfor %}

CREATE USER '{{ user }}'@'localhost' IDENTIFIED BY '{{ password }}';
GRANT ALL ON *.* TO 'root'@'%';