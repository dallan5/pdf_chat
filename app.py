import os
import openai
from flask import Flask, request, render_template, jsonify, render_template_string
from flaskext.markdown import Markdown
import tiktoken
import markdown
app = Flask(__name__)
Markdown(app)
openai.api_key = os.getenv("OPENAI_API_KEY")

assistant_instruction = "You are a helpful tutor. Please provide a response using the following Markdown elements: headers, emphasis (italics, bold, combined), unordered and ordered lists, links, images (use a placeholder URL), blockquotes, inline code, code blocks, horizontal rules, tables, strikethrough, task lists, footnotes, and autolinks."


source_text = ""
conversation_messages = list()
system_messages = list()

def markdown_to_html(content):
    return markdown.markdown(content)

def format_message(role, content):
    _dict = {}
    _dict["role"] = role
    _dict["content"] = content
    return _dict

def set_source_text(string):
    global source_text
    source_text = f"Read this:{string}"
    update_messages()

def add_message(role, content, messages=None):
    if messages is None:
        messages = []

    _message = format_message(role, content)
    messages.append(_message)
    return messages

def get_tokens(text, encoding_name = "cl100k_base"):
    #TODO: I can get the amount of tokens directly from the reponse message
    encoding = tiktoken.get_encoding(encoding_name)
    token_count = len(encoding.encode(str(text)))
    return token_count

def get_message_tokens(messages):
    tokens = 0
    for message in messages:
        tokens += get_tokens(message.get("content", ""))
    return tokens

def setup_messages():
    messages = list()
    messages = add_message("assistant", assistant_instruction, messages)
    return messages if messages else []

def recursive_clear_messages(messages):
    # Remove messages intil tokens are less than 4990
    if not messages:
        return []

    tokens = get_message_tokens(messages)
    if tokens > 4990:
        #Always remove the index 2, since 0 and 1 are assistant instructions followed by text. Keep the rest
        messages = [item for i, item in enumerate(messages) if i != 2]
        return recursive_clear_messages(messages)
    else:
        return messages

def register_message(role, content):
    global conversation_messages
    conversation_messages.append(format_message(role, content))
    update_messages()

def set_system_messages(messages):
    global system_messages
    system_messages = messages
    print("SYSTEM MESSAGE SET")
    print(messages)
    print('-----------------')

def update_messages():
    # First add system instructions for assistant
    messages = setup_messages()
    # Then add source text, which is the base for assistant knowledge
    if source_text:
        messages = add_message("user", source_text, messages)
    #Add conversational messages
    print(conversation_messages)
    print(messages)
    messages += conversation_messages
    set_system_messages(messages)

messages = setup_messages()

@app.route("/", methods=["GET", "POST"])
def index():
    global messages

    if request.method == "POST":
        if request.is_json:
            # Handle the AJAX request here
            query = request.json['query']
            register_message("user", query)  # Keep this line

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=system_messages,
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

        # This part will handle non-ajax POST requests
        elif 'query' in request.form:
            query = request.form['query']
            register_message("user", query)  # Keep this line

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
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
                register_message("assistant", content)


    return render_template("index.html", messages=messages)

@app.route("/add_text_to_memory", methods=["POST"])
def add_text_to_memory():
    text = str()
    if request.method == "POST":
        data = request.json
        if data.get("text", "") not in text:
            text += data.get("text", "")
        set_source_text(text)
        return jsonify({"message": "Text saved to memory."})
    return jsonify({"message": "Invalid request."})


@app.route("/clear_memory", methods=["POST"])
def clear_memory():
    set_source_text("")
    return jsonify({"message": "Memory cleared"})
