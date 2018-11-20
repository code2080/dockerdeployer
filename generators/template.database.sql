{% for app in apps %}
CREATE DATABASE IF NOT EXISTS `{{ app.database_name }}`;
{% endfor %}