import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    assistant_instruction = "You are a helpful assistant. Please provide responses using the following Markdown elements: headers, emphasis (italics, bold, combined), unordered and ordered lists, links, images (use a placeholder URL), blockquotes, inline code, code blocks, horizontal rules, tables, strikethrough, task lists, footnotes, and autolinks. Base all facts from preceding messages."