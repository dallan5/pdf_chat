# OpenAI API Quickstart - Python example app


To get the server running, use this command:
gunicorn --config gunicorn_config.py app:app --reload --log-level=debug --error-logfile=- --access-logfile=- --capture-output
