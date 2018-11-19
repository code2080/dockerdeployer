import time
from django.db import connections
from django.db.utils import OperationalError

connected = False

while not connected:
    try:
        c = connections['default'].cursor()
    except OperationalError:
        print("Mysql is unavailable. Sleeping in 1s...")
        time.sleep(0.5)
    else:
        connected = True
        c.close()
        print("Mysql is up. Waiting for Mysql service restart in 3s...")
        time.sleep(3)
        print("Excuting command...")