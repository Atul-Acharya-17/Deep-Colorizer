import torch
import torch.nn as nn
import fastai
from fastai.vision.learner import create_body
from fastai.vision.models.unet import DynamicUnet


def create_generator(back_bone=fastai.vision.models.resnet34, IMG_SIZE=256):
    resnet34 = back_bone
    model = create_body(resnet34, pretrained=True, n_in=1, cut=-2)
    gen = DynamicUnet(model, 2, (IMG_SIZE, IMG_SIZE))#.to(device)

    return gen


class UNet(nn.Module):

    def __init__(self):
        super(UNet, self).__init__()
        
        self.max_pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        
        self.contract_1 = nn.Sequential(  
            nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 64, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2, inplace=True)
        )
        
        self.contract_2 = nn.Sequential(  
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(128, 128, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True)
        )
        
        self.contract_3 = nn.Sequential(  
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(256, 256, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True)
        )
        
        self.bottle_neck = nn.Sequential(  
            nn.Conv2d(256, 512, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(512, 512, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(512, 256, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True)
        )
        
        self.expand_1 = nn.Sequential(
            nn.Conv2d(512, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 128, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True)
        )
        
        self.expand_2 = nn.Sequential(
            nn.Conv2d(256, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 64, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )
        self.expand_3 = nn.Sequential(
            nn.Conv2d(128, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 32, kernel_size=1, stride=1, padding=0),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True)
        )
        
        self.final_layer = nn.Sequential(
            nn.Conv2d(32, 2, kernel_size=1, stride=1, padding=0),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        x0 = self.contract_1(x)
        x1 = self.max_pool(x0)
        x2 = self.contract_2(x1)
        x3 = self.max_pool(x2)
        x4 = self.contract_3(x3)
        x5 = self.max_pool(x4)
        x6 = self.bottle_neck(x5)
        
        x7 = self.upsample(x6)
        x7 = torch.cat([x7, x4], axis=1)
        x8 = self.expand_1(x7)
        
        x9 = self.upsample(x8)
        x9 = torch.cat([x9, x2], axis=1)
        x10 = self.expand_2(x9)
        
        x11 = self.upsample(x10)
        x11 = torch.cat([x11, x0], axis=1)
        x12 = self.expand_3(x11)
        
        output = self.final_layer(x12)
        
        return output