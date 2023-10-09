
import os
import openai

from flask import Flask

from pdf_chat.config import Config
from pdf_chat.routes import initialize_routes

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.config.from_object(Config)
initialize_routes(app)

if __name__ == "__main__":
    app.run(debug = True)
