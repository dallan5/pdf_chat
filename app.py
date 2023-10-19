import os
import logging
from dotenv import load_dotenv
import openai
import secrets
import redis

from flask import Flask, session
from flask_session import Session

from pdf_chat.config import Config
from pdf_chat.routes import initialize_routes




# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
openai.api_key = os.getenv("OPENAI_API_KEY")

app.config.from_object(Config)
# Initialize session handling
Session(app)
initialize_routes(app)

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

first_request_done = False
#Clear the session and DB when starting the server
@app.before_request
def handle_before_request():
    global first_request_done
    if not first_request_done:
        redis_client.flushdb()
        session.clear()
        first_request_done = True

if __name__ == "__main__":
    app.run(debug=True)
