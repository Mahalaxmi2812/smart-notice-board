from flask import Flask, render_template, request, jsonify, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, storage
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Initialize Firebase Admin SDK
#cred = credentials.Certificate(r"C:/Users/Rishi/Downloads/valo123 - Copy/valo123/iot_notice_board/serviceAccountKey.json")
# automatic path
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'noticeboard12.appspot.com'
})

# Get Firestore database instance
db = firestore.client()

# Get Firebase storage bucket
bucket = storage.bucket()

# Firebase Data Model for Messages
def add_message_with_image(content, image_url=None):
    message_ref = db.collection('messages').document()
    message_data = {'content': content}
    if image_url:
        message_data['image_url'] = image_url
    message_ref.set(message_data)

def get_messages():
    return [doc.to_dict() for doc in db.collection('messages').stream()]

def delete_message_by_content(content):
    docs = db.collection('messages').where('content', '==', content).stream()
    success = False
    for doc in docs:
        doc.reference.delete()
        success = True
    return success

@app.route('/notice', methods=['GET'])
def notice():
    messages = get_messages()
    return render_template('display.html', messages=messages)

@app.route('/delete-message', methods=['POST'])
def delete_message():
    try:
        data = request.json
        message_content = data.get('message')

        if message_content and delete_message_by_content(message_content):
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Message not found or invalid request")
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify(success=False, error=str(e))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_message = request.form.get('message')
        image = request.files.get('image')

        if new_message.strip() != "":
            if image:
                # Secure the filename and generate a unique file path
                filename = secure_filename(image.filename)
                unique_filename = f"images/{uuid.uuid4()}_{filename}"
                blob = bucket.blob(unique_filename)
                blob.upload_from_file(image, content_type=image.content_type)
                blob.make_public()  
                image_url = blob.public_url
                add_message_with_image(new_message, image_url=image_url)
            else:
                add_message_with_image(new_message)

        # Redirect after POST
        return redirect(url_for('index'))
    else:
        messages = get_messages()
        return render_template('index.html', messages=messages)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
