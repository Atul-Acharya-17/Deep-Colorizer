import numpy as np
import os
from skimage.color import rgb2lab, lab2rgb
import cv2
from PIL import Image

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
import torchvision.utils as vutils
import fastai
from fastai.vision.learner import create_body
from fastai.vision.models.unet import DynamicUnet

class Colorizer():
    #DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    DEVICE = "cpu"
    IMG_SIZE = 256

    INITIALIZED = False

    transform = transforms.Compose([
                transforms.Resize((IMG_SIZE, IMG_SIZE), Image.BICUBIC),
            ])
    resnet34 = fastai.vision.models.resnet34
    model = create_body(resnet34, pretrained=True, n_in=1, cut=-2)
    gen = DynamicUnet(model, 2, (IMG_SIZE, IMG_SIZE)).to(DEVICE)


    @staticmethod
    def preprocess(filename):
        img = Image.open(filename).convert("RGB")
        img = Colorizer.transform(img)
        img = np.array(img)
        img_lab = rgb2lab(img).astype("float32")
        img_lab = transforms.ToTensor()(img_lab)
        L = img_lab[[0], ...] / 50. - 1. # Between -1 and 1
        ab = img_lab[[1, 2], ...] / 110. # Between -1 and 
        return L
    
    @staticmethod
    def initialize(model_path):
        checkpoint = torch.load(model_path, map_location=Colorizer.DEVICE)
        Colorizer.gen.load_state_dict(checkpoint['state_dict'])
        Colorizer.INITIALIZED = True
    
    @staticmethod
    def colorize(filename, output_filename):
        if not Colorizer.INITIALIZED:
            Colorizer.initialize('colorizer/models/gen_state.pt')
        
        L_channel = Colorizer.preprocess(filename)
        pred = Colorizer.gen(L_channel.unsqueeze(0).to(Colorizer.DEVICE)).detach()

        L_channel = (L_channel + 1.) * 50.
        pred = pred * 110.
        pred_img = torch.cat([L_channel.unsqueeze(0), pred], dim=1).permute(0, 2, 3, 1).cpu()
        pred_img = pred_img.squeeze(0)

        pred_img = pred_img.numpy()
        pred_img = lab2rgb(pred_img)

        pred_img *= 255
        pred_img = cv2.cvtColor(pred_img,cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_filename, pred_img)