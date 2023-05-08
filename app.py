from flask import Flask, request, send_file
import base64
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/image', methods=['POST'])
def process_image():
    # read json key "image_data"
    # without the `data:image/jpeg;base64,` prefix
    image_data = request.json['image_data']

    # Convert the base64-encoded image data to bytes
    print(image_data)

    image_bytes = base64.b64decode(str(image_data))
    img = Image.open(BytesIO(image_bytes))
    img.save('image.jpg', 'jpeg')

    return 'OK'

if __name__ == '__main__':
    app.run()
