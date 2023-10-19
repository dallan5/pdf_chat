# PDF Chat Quickstart

This example shows you how do deploy the pdf_chat to your VPS server.

## Setup

1. Install Python 3.

2. Clone this repository.

3. Navigate into the project directory:

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip3 install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Add add the following to the newly created `.env` file.
   FLASK_APP=app
   FLASK_ENV=development
   # Once you add your API key below, make sure to not share it with anyone! The API key should remain private.
   OPENAI_API_KEY=[API key]

8. Launch the redis server

   ```bash
   $ redis-server
   ```

8. Run the app:

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)!

To get the server running, use this command:
gunicorn --config gunicorn_config.py app:app --reload --log-level=debug --error-logfile=- --access-logfile=- --capture-output
