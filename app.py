import os
import openai
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
messages = list()
text = ""

def add_message(role, content):
    global messages
    _dict = {}
    _dict["role"] = role
    _dict["content"] = content
    messages.append(_dict)

add_message("system", "You are a helpful assistant.")

@app.route("/", methods=["GET", "POST"])
def index():
    global messages

    if request.method == "POST":
        if request.is_json:
            # Handle the AJAX request here
            query = request.json['query']
            add_message("user", query)  # Keep this line

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
                add_message(role, content)

                # Return the response to the frontend
                return jsonify({"role": role, "message": content})

            except Exception as e:
                print(f"Error: {e}")
                content = "Sorry, I couldn't process that request."
                add_message("assistant", content)
                return jsonify({"role": "assistant", "message": content})

        # This part will handle non-ajax POST requests
        elif 'query' in request.form:
            query = request.form['query']
            add_message("user", query)  # Keep this line

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
                add_message(role, content)

            except Exception as e:
                print(f"Error: {e}")
                content = "Sorry, I couldn't process that request."
                add_message("assistant", content)


    return render_template("index.html", messages=messages)

@app.route("/add_text_to_memory", methods=["POST"])
def add_text_to_memory():
    global text
    if request.method == "POST":
        data = request.json
        if data.get("text", "") not in text:
            text += data.get("text", "")
        return jsonify({"message": "Text saved to memory."})
    return jsonify({"message": "Invalid request."})

