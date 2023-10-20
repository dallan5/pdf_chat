import os
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
    text = ""
    print("PAGE NUMBER", page_number)
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        if reader.is_encrypted:
            reader.decrypt('')
        
        if page_number <= len(reader.pages):
            page = reader.pages[page_number-1]
            text = page.extract_text()
        else:
            raise Exception(f"Page {page_number} not found in the document.PDF file: {pdf_path}")
    return text

def clear_messages(messages):
    # Remove single message
    if not messages:
        return []

    #Always remove the index 2, since 0 and 1 are assistant instructions followed by text. Keep the rest
    return [item for i, item in enumerate(messages) if i != 2]

def clear_directory(directory_path):
    for filename in os.listdir(directory_path):  # List all files and directories in the specified directory
        file_path = os.path.join(directory_path, filename)  # Join the directory path and filename to get the full path
        if os.path.isfile(file_path):  # Check if the path is a file (not a directory)
            print("DELETE:", file_path)
            os.unlink(file_path)


def create_uploads_folder(uploads_dir):
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)