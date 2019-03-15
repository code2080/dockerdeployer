{% for app in apps %}
    {% if app.type == "django" %}
        CREATE DATABASE IF NOT EXISTS `{{ app.database_name }}`;
    {% endif %}
{% endfor %}