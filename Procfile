web: gunicorn wger.wsgi --log-file -
release: invoke create-settings --settings-path ./settings.py --database-type postgresql
release: invoke bootstrap-wger --settings-path ./settings.py --no-start-server