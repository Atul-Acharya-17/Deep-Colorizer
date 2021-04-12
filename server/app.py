import fastai
from fastai.vision.learner import create_body
from fastai.vision.models.unet import DynamicUnet
import torch
import cv2
import numpy as np
from skimage.color import rgb2lab, lab2rgb
import torchvision.transforms as transforms
from flask import Flask, request

app = Flask(__name__)

@app.route('/predict',methods=['POST'])
def predict():
    data = request.get_json(force=True)
    print('Data:',data)
    return 'Received'