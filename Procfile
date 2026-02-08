web: daphne -b 0.0.0.0 -p $PORT secureHome.asgi:application 
worker: celery -A secureHome worker --loglevel=info