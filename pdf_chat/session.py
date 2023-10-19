import json
from flask import session
from .utils import add_message_to_list, setup_messages

def get_session_data(key, default_value = None):
    if key not in session:
        return default_value
    return json.loads(session.get(key, default_value))

def set_session_data(key, value):
    session[key] = json.dumps(value)

def update_session_messages():
    message = """Process the following text on page {} 
            and base all subsequent responses on the 
            facts contained within:\n{}"""
    
    messages = setup_messages()
    source_text = get_session_data("source_text", "")
    source_page = get_session_data("source_page", 0)
    conversation_messages = get_session_data("conversation_messages", [])

    if source_text and source_page:
        messages = add_message_to_list(
            "user", 
            message.format(
                source_page, 
                source_text,
                ), 
            messages
            )

    messages += conversation_messages
    print('-------------------')
    print(messages)
    print('-------------------')
    set_session_data("system_messages", messages)