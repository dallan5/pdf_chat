import os
import redis
from datetime import timedelta

class Config:
    DEBUG = True
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    UPLOAD_FOLDER = "/tmp/pdf_uploads"
    assistant_instruction = "You are a helpful assistant. Please provide responses using the following Markdown elements: headers, emphasis (italics, bold, combined), unordered and ordered lists, links, images (use a placeholder URL), blockquotes, inline code, code blocks, horizontal rules, tables, strikethrough, task lists, footnotes, and autolinks. Base all facts from preceding messages."
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 Megabytes

    # Configure Redis for session management
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False

    # SESSION_USE_SIGNER = True #TODO: Look into this later
    SESSION_KEY_PREFIX = 'chatbot:'
    SESSION_REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)