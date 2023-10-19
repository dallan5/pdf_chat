from flask import Flask, session
from flask_session import Session
import json

app = Flask(__name__)
# Check Configuration section for more details
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

@app.route('/set/')
def set():
    value = [{"role" : "system", "content" : "you're an assistant"}, {"role" : "user", "content" : "give me a list of bullet points"}]
    session['system_messages'] = json.dumps(value)
    return 'ok'

@app.route('/get/')
def get():
    print(session)
    a = json.loads(session.get('system_messages', 'not set'))
    print(type(a))
    return a

if __name__ == "__main__":
    app.run(debug=True)
