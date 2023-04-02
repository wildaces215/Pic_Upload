from flask import Flask, render_template, request,redirect,url_for
from PIL import Image
from PIL.ExifTags import TAGS
from urllib.parse import quote,unquote
import json

app = Flask(__name__)
#Main route
@app.route('/')
def index():
    return render_template('index.html', message='Hello, world!')
@app.route('/upload',methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    image =Image.open(file)
    info_dict = {
    "Filename": filename,
    "Image Size": image.size,
    "Image Height": image.height,
    "Image Width": image.width,
    "Image Format": image.format,
    "Image Mode": image.mode,
    "Image is Animated": getattr(image, "is_animated", False),
    "Frames in Image": getattr(image, "n_frames", 1)
    }
    encoded_data = quote(json.dumps(info_dict))
    return redirect(url_for('display',info_dict=encoded_data))
    
@app.route('/display')
def display():
    encoded_data = request.args.get('info_dict')
    data = json.loads(unquote(encoded_data))
    return render_template('display.html',name = data['Filename'],size = data['Image Size'],height = data['Image Height'],width = data['Image Width'],format = data['Image Format'],mode = data['Image Mode'],animated = data['Image is Animated'],frames = data['Frames in Image'])
app.run(debug=True)