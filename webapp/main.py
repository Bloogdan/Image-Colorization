from flask import Flask, request, render_template, make_response, jsonify, redirect, url_for
from google.cloud import datastore
from image_handler import handle_image
from datetime import datetime
import os
import uuid

    
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'image-colorization-280016-c617dae15ba5.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/load')
def load():
    if request.args:
        cursor = request.args.get('c')
        if cursor == 'start':
            cursor = None
        elif cursor == 'end':
            return make_response(jsonify('finished', []), 200)
        else:
            cursor = bytes(cursor, 'utf-8')

        datastore_client = datastore.Client()
        query = datastore_client.query(kind='image')
        query.order = ['-created_at']
        query_iter = query.fetch(start_cursor=cursor, limit=24)
        images = list(next(query_iter.pages))
        next_cursor = query_iter.next_page_token

        if next_cursor == None:
            return make_response(jsonify('end', images), 200)
        else:
            return make_response(jsonify(next_cursor.decode('utf-8'), images), 200)


@app.route('/about')
def about():
    return render_template('about.html')

    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for file in dict(request.files).values():
            if file.filename == '':
                return 'No selected file.', 400
        
            if file and allowed_file(file.filename):
                datastore_client = datastore.Client()
                entity_id = uuid.uuid4().hex
                entity_key = datastore_client.key('image', entity_id)
                entity_image = datastore.Entity(key=entity_key)

                image_path = handle_image(file, entity_id)

                entity_image['path'] = image_path
                entity_image['created_at'] = datetime.now()
        
                datastore_client.put(entity_image)
            
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
