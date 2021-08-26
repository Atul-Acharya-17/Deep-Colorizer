from PIL import Image
import numpy as np
from skimage.color import rgb2lab
import torchvision.transforms as transforms
from torch.utils.data import Dataset

class ColorDataset(Dataset):
    
    def __init__(self, path, transform=None):
        super(ColorDataset, self).__init__()
        self.path = path
        self.transform = transform
    
    def __getitem__(self, idx):
        img = Image.open(self.path[idx]).convert("RGB")
        img = self.transform(img)
        img = np.array(img)
        img_lab = rgb2lab(img).astype("float32")
        img_lab = transforms.ToTensor()(img_lab)
        L = img_lab[[0], ...] / 50. - 1. # Between -1 and 1
        ab = img_lab[[1, 2], ...] / 110. # Between -1 and 1
        
        return {'L': L, 'ab': ab}
    
    def __len__(self):
        return len(self.path)