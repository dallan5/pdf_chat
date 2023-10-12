import openai
from flask import request, render_template, jsonify, views
from .utils import markdown_to_html, format_message, extract_text_from_page
from .state import get_state_manager

state_manager = get_state_manager()

from pdf_chat.utils import setup_messages, add_message_to_list

def update_state_manager_messages(state_manager):
    messages = setup_messages()
    if state_manager.source_text:
        messages = add_message_to_list("user", "Process the following text on page {} and base all subsequent responses on the facts contained within:\n{}".format(state_manager.source_page, state_manager.source_text), messages)
    messages += state_manager.conversation_messages
    state_manager.system_messages = messages

def register_message(role, content):
    state_manager.conversation_messages.append(format_message(role, content))
    update_state_manager_messages(state_manager)


class ChatView(views.MethodView):
    
    def get(self):
        return render_template("index.html", messages=state_manager.system_messages)  # Assuming you've defined 'messages' somewhere

    def post(self):
        if request.is_json:
            return self._handle_ajax_request()
        elif 'query' in request.form:
            return self._handle_form_request()

    def _handle_ajax_request(self):
        query = request.json['query']
        register_message("user", query)  # Keep this line

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=state_manager.system_messages,
                temperature=0,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            # Fetch the role and content of the response message
            role = response['choices'][0]['message']['role']
            content = markdown_to_html(response['choices'][0]['message']['content'])
            register_message(role, content)

            # Return the response to the frontend
            return jsonify({"role": role, "message": content})

        except Exception as e:
            print(f"Error: {e}")
            content = "Sorry, I couldn't process that request."
            register_message("assistant", content)
            return jsonify({"role": "assistant", "message": content})

    def _handle_form_request(self):
        query = request.form['query']
        register_message("user", query)  # Keep this line

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=state_manager.messages,
                temperature=0,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Fetch the role and content of the response message
            role = response['choices'][0]['message']['role']
            content = response['choices'][0]['message']['content']
            register_message(role, content)

        except Exception as e:
            print(f"Error: {e}")
            content = "Sorry, I couldn't process that request."
            register_message(role, content)

class MemoryView(views.MethodView):

    def post(self):
        if request.path.endswith('clear_memory'):
            return self.clear_memory()
        elif request.path.endswith('capture_text'):
            return self.capture_text()
        
    
    def capture_text(self):
        try:
            data = request.json
            page_number = data.get("page_number", 0)
            print(page_number)
            text = extract_text_from_page(state_manager.pdf_path, page_number)
            state_manager.source_page = page_number
            state_manager.source_text = text
            update_state_manager_messages(state_manager)
            return jsonify({"message": "{}".format(str(text))})
        except Exception as e:
            print(f"Capture Text Error: {e}")
            return jsonify({"error": str(e)}), 500


def initialize_routes(app):
    app.add_url_rule('/', view_func=ChatView.as_view('index'))
    app.add_url_rule('/capture_text', view_func = MemoryView.as_view("capture_text"))
