import os
import time
import MySQLdb

connected = False

while not connected:
    try:
        db = MySQLdb.connect(host="database", user=os.environ['MYSQL_USER'], passwd=os.environ['MYSQL_ROOT_PASSWORD'])
        cursor = db.cursor()
        sql = """
{% for app in apps %}
    {% if app.type == "django" %}
        CREATE DATABASE IF NOT EXISTS `{{ app.database_name }}`;
    {% endif %}
{% endfor %}
"""
        cursor.execute(sql)
    except MySQLdb._exceptions.OperationalError:
        print("Mysql is unavailable. Sleeping in 1s...")
        time.sleep(0.5)
    else:
        connected = True
        cursor.close()
        print("Mysql is up. Waiting for Mysql service restart in 3s...")
        time.sleep(3)
        print("Excuting command...")
