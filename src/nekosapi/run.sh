python manage.py collectstatic --no-input
python manage.py migrate
uvicorn nekosapi.asgi:application --host 0.0.0.0 --port 8000 --workers $(API_WORKERS)
