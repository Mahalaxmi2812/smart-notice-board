# app.py
from flask import Flask, render_template,request,jsonify

app = Flask(__name__)

messages = []
@app.route('/')
def index():
    print("Accessed the home route")
    return render_template('index.html', messages=messages)

@app.route('/update-messages', methods=['POST'])
def update_messages():
    global messages

    try:
        data = request.json
        new_message = data.get('message')
        num_messages = int(data.get('num-messages'))

        if new_message.strip() != "":
            messages.append(new_message)

        messages = messages[:num_messages]

        print(f"Received new message: {new_message}")
        print(f"Updated messages: {messages}")

        return jsonify(success=True, messages=messages)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify(success=False, error=str(e))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)





