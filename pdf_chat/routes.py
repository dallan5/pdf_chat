import openai
import json
from flask import request, render_template, jsonify, views, session
from .utils import markdown_to_html, format_message, extract_text_from_page, clear_messages
from .session import get_session_data, set_session_data, update_session_messages

from pdf_chat.utils import setup_messages, add_message_to_list

def register_message(role, content):
    
    conversation_messages = get_session_data("conversation_messages", [])
    conversation_messages.append(format_message(role, content))
    set_session_data("conversation_messages", conversation_messages)
    update_session_messages()

class ChatView(views.MethodView):
    
    def get(self):
        # Set default values if nothing provided
        if 'conversation_messages' not in session:
            setup_messages()
        if "source_page" not in session:
            set_session_data("source_page", 0)
        if "source_text" not in session:
            set_session_data("source_text", "")
        if "pdf_path" not in session:
            set_session_data("pdf_path", "static/pdf/book.pdf")
        if "system_messages" not in session:
            set_session_data("system_messages", [])

        return render_template("index.html", messages=get_session_data("conversation_messages", []))

    def post(self):
        if request.is_json:
            return self._handle_ajax_request()
        #elif 'query' in request.form:
        #    return self._handle_form_request()

    def _handle_ajax_request(self):
        query = request.json['query']
        register_message("user", query)  # Keep this line
        # Flag to control the while loop
        retry_request = True
        # Counter to keep track of the number of attempts
        attempt_counter = 0
        # Maximum number of attempts
        max_attempts = 2

        content = ""
        role = "assistant"
        while retry_request and attempt_counter < max_attempts:
            attempt_counter += 1  # Increment the counter at the beginning of each loop iteration

            try:
                # Your OpenAI API request
                print("sending request")
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=get_session_data("system_messages", []),
                    temperature=0,
                    max_tokens=1024,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                print("response")
                # If the request is successful, the following lines will execute,
                # and the loop will exit by setting retry_request to False
                role = response['choices'][0]['message']['role']
                content = markdown_to_html(response['choices'][0]['message']['content'])
                register_message(role, content)
                retry_request = False  # Set the flag to false to exit the loop

            except openai.error.RateLimitError as e:
                print(f"OpenAI API request exceeded rate limit: {e}")
                # Optionally, you may want to break out of the loop or handle this error differently

            except openai.error.OpenAIError as e:
                # Assuming the token error is of type OpenAIError, adjust if necessary
                print(f"Token error: {e}. Clearing messages and retrying...")
                set_session_data("system_messages", clear_messages(get_session_data("system_messages", [])))

            except Exception as e:
                print(f"Error: {e}")
                content = "Sorry, I couldn't process that request."
                register_message("assistant", content)
                retry_request = False  # Set the flag to false to exit the loop

        # Check if the loop exited due to reaching the maximum number of attempts
        if attempt_counter >= max_attempts:
            content = "Sorry, I couldn't process that request after multiple attempts."
            register_message("assistant", content)

        # Return the response to the frontend
        # This is placed outside the loop to ensure it's executed once the loop exits
        return jsonify({"role": role, "message": content})

class MemoryView(views.MethodView):

    def post(self):
        if request.path.endswith('clear_session'):
            return self.clear_session()
        elif request.path.endswith('capture_text'):
            return self.capture_text()
    
    def capture_text(self):
        try:
            data = request.json
            page_number = data.get("page_number", 0)
            text = extract_text_from_page(get_session_data("pdf_path"), page_number)#TODO: update this

            set_session_data("source_page", page_number)
            set_session_data("source_text", text)
            update_session_messages()

            return jsonify({"message": "{}".format(str(text))})
        
        except Exception as e:
            print(f"Capture Text Error: {e}")
            return jsonify({"error": str(e)}), 500
        
    def clear_session(self):
        print("SESSION CLEARED")
        session.clear()
        return '', 200

def initialize_routes(app):
    app.add_url_rule('/', view_func=ChatView.as_view('index'))
    app.add_url_rule('/capture_text', view_func = MemoryView.as_view("capture_text"))
