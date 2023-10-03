import os
import openai
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
messages = list()

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
    global uploaded_file_path  # Make sure to access the global variable
    upload_confirmation = None  # Variable to store the upload confirmation message

    if request.method == "POST":
        if 'query' in request.form:
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


    return render_template("index.html", messages=messages, upload_confirmation=upload_confirmation)
