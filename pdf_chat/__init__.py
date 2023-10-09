from flask import Flask
from .config import Config
from .routes import initialize_routes

app = Flask(__name__)
app.config.from_object(Config)
initialize_routes(app)
