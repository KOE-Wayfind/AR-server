import os
import uuid
from flask import Flask, request, send_file
import base64
from io import BytesIO
from PIL import Image
from pathlib import Path

import my_hloc as my_hloc

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/image', methods=['POST'])
def process_image():
    # read json key "image_data"
    # without the `data:image/jpeg;base64,` prefix
    print("sampai sini")
    image_data = request.json['image_data']


    # Convert the base64-encoded image data to bytes
    image_bytes = base64.b64decode(str(image_data))
    
    # Generate a unique filename using UUID
    filename = str(uuid.uuid4()) + '.png'
    
    # Specify the temp directory path for saving the images
    temp_save_directory = 'images_temp'
    
    # Create the save directory if it doesn't exist
    os.makedirs(temp_save_directory, exist_ok=True)
    
    # Construct the full path to save the image
    temp_save_path = os.path.join(temp_save_directory, filename)
    
    img = Image.open(BytesIO(image_bytes))
    img.save(temp_save_path, 'png')

    resize_image(temp_save_path)

    return 'OK'

i = 0


@app.route('/test', methods=['POST'])
def test_endpoint():
    global i
    i =+ 1
    # result = my_hloc.check_location('night/e1-l2-conference-room-b_3.jpg')
    return str(i)

def resize_image(image_path):
    # open the image file
    image = Image.open(image_path)

    # get image dimension
    width, height = image.size

    # calculate the height of the cropped area to maintain a 3:4 aspect ratio
    cropped_height = int(width * 4 / 3)

    # define the top-left and bottom-right coordinates of the crop area
    left = 0
    top = 0
    right = width
    bottom = cropped_height

    # crop the image
    res_image = image.crop((left, top, right, bottom))

    width, height = res_image.size # new width & height value

    # resize the cropped image to fit into a 512x512 box
    base_height = 512
    wpercent = (base_height/float(height))
    wsize = int((float(width)*float(wpercent)))
    res_image = res_image.resize((wsize,base_height), Image.Resampling.LANCZOS)

    # Extract the filename from original file
    file_name = Path(image_path).stem + '.png'
    
    # Specify the temp directory path for saving the images
    save_dir = 'images'
    
    # Create the save directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Construct the full path to save the image
    temp_save_path = os.path.join(save_dir, file_name)
    
    res_image.save(temp_save_path, 'png')
    # save the resized image
    

if __name__ == '__main__':
    app.run(debug=True)
