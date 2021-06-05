import fastai
from fastai.vision.learner import create_body
from fastai.vision.models.unet import DynamicUnet
import torch
import cv2
import numpy as np
from skimage.color import rgb2lab, lab2rgb
import torchvision.transforms as transforms
from flask import Flask, request, send_file, session
from flask_cors import CORS #comment this on deployment
from werkzeug.utils import secure_filename
from colorizer.colorizer import Colorizer
from flask.helpers import make_response

app = Flask(__name__)

CORS(app) #comment this on deployment


@app.route('/colorize',methods=['POST'])
def colorize():
    image = request.files['image'] 
    filename = secure_filename("image.png")
    destination="/".join(["colorizer", filename])
    image.save(destination)
    Colorizer.colorize(destination, destination)
    response = make_response(send_file(destination,mimetype='image/gif'))
    return send_file(destination,mimetype='image/gif')

if __name__ == '__main__':
    Colorizer.initialize('colorizer/models/gen_state.pt')
    app.run(debug=True)

#CORS(app, expose_headers='Authorization')