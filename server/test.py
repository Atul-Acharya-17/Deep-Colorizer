import numpy as np
import pandas as pd
import os
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
from skimage.color import rgb2lab, lab2rgb
import cv2
from PIL import Image
from pathlib import Path
import glob

import torch
import torch.nn as nn

import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as dset
import torch.optim as optim
import torchvision.utils as vutils
import numpy as np
from torch.utils.data import DataLoader, Dataset
import fastai
from fastai.vision.learner import create_body
from fastai.vision.models.unet import DynamicUnet

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
DEVICE = "cpu"

BATCH_SIZE = 16
IMG_SIZE = 256

transform = transforms.Compose([
                transforms.Resize((IMG_SIZE, IMG_SIZE), Image.BICUBIC),
            ])

path = "b.jpeg"

img = Image.open(path).convert("RGB")
img = transform(img)
img = np.array(img)
img_lab = rgb2lab(img).astype("float32")
img_lab = transforms.ToTensor()(img_lab)
L = img_lab[[0], ...] / 50. - 1. # Between -1 and 1
ab = img_lab[[1, 2], ...] / 110. # Between -1 and 


resnet34 = fastai.vision.models.resnet34
model = create_body(resnet34, pretrained=True, n_in=1, cut=-2)
gen = DynamicUnet(model, 2, (IMG_SIZE, IMG_SIZE)).to(DEVICE)

checkpoint = torch.load("models/gen_state.pt", map_location=DEVICE)
gen.load_state_dict(checkpoint['state_dict'])

pred = gen(L.unsqueeze(0).to(DEVICE)).detach()

L = (L + 1.) * 50.
pred = pred * 110.

print(L.shape)
print(pred.shape)

pred_img = torch.cat([L.unsqueeze(0), pred], dim=1).permute(0, 2, 3, 1).cpu()



print(pred_img.squeeze(0).shape)

pred_img = pred_img.squeeze(0)

pred_img = pred_img.numpy()

pred_img = lab2rgb(pred_img)

pred_img *= 255
#pred_img = np.int64(pred_img)
pred_img = cv2.cvtColor(pred_img,cv2.COLOR_RGB2BGR)

cv2.imwrite(path, pred_img)

