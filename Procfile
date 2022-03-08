release: python manage.py migrate
web: gunicorn  utilitario.wsgi --timeout 40 --log-file -
