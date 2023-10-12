from pdf_chat.config import Config
import markdown
import PyPDF2

def format_message(role, content):
    return {
        "role": role,
        "content": content
    }

def markdown_to_html(content):
    return markdown.markdown(content)

def format_message(role, content):
    _dict = {}
    _dict["role"] = role
    _dict["content"] = content
    return _dict

def setup_messages():
    messages = list()
    messages = add_message_to_list("assistant", Config.assistant_instruction, messages)
    return messages if messages else []

def add_message_to_list(role, content, messages=None):
    if messages is None:
        messages = []
    _message = format_message(role, content)
    messages.append(_message)
    return messages

def extract_text_from_page(pdf_path, page_number):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        if reader.is_encrypted:
            reader.decrypt('')
        
        if page_number < len(reader.pages):
            page = reader.pages[page_number]
            return page.extract_text()
        else:
            return f"Page {page_number} not found in the document."
