import numpy as np
from PIL import Image
import os

# PyTorch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
from torchvision.models import mobilenet_v2

# Pytorch Lightning
import pytorch_lightning as pl
from pytorch_lightning.metrics import functional as FM

class PreTrained_Model(pl.LightningModule):
    def __init__(self):
        super().__init__()
        pretrained_model = mobilenet_v2(pretrained = True)
        for param in pretrained_model.parameters():
            param.requires_grad = False
        
        # MobileNet V2
        num_ftrs = pretrained_model.classifier[1].in_features
        pretrained_model.classifier = nn.Sequential(
            nn.Linear(num_ftrs, 512, bias = True),
            nn.ReLU(inplace = True),
            nn.Dropout(p = 0.5, inplace = False),
            nn.Linear(in_features = 512, out_features = 64, bias = True),
            nn.ReLU(inplace = True),
            nn.Dropout(p = 0.5, inplace = False),
            nn.Linear(in_features = 64, out_features = 20, bias = True),
        )
        
        self.model = pretrained_model
        self.softmax = nn.Softmax(dim = 1)
        self.train_acc = pl.metrics.Accuracy()
        self.val_acc = pl.metrics.Accuracy()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch['image'], batch['targets']
        outputs = self.model(x)
        loss = F.cross_entropy(outputs, torch.max(y.long(), 1)[1])
        acc = self.train_acc(self.softmax(outputs), y)
        self.log('train_loss', loss, prog_bar = True)
        self.log('train_acc', acc, prog_bar = True)
        return loss
    
    def validation_step(self, batch, batch_idx):
        x, y = batch['image'], batch['targets']
        outputs = self.model(x)
        loss = F.cross_entropy(outputs, torch.max(y.long(), 1)[1])
        acc = self.val_acc(self.softmax(outputs), y)
        self.log('val_loss', loss, prog_bar = True, on_epoch = True)
        self.log('val_acc', acc, prog_bar = True, on_epoch = True)

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr = 0.0005)
        return optimizer

def load_img(img_path):
    img = np.asarray(Image.open(img_path).resize((224, 224)))
    assert(img.dtype == 'uint8')
    img = img / 255
    img = np.divide(np.subtract(img, np.asarray([0.485, 0.456, 0.406])), np.asarray([0.229, 0.224, 0.225]))
    img = np.expand_dims(img, axis = 0)
    img = np.rollaxis(img, axis = 3, start = 1)
    img = torch.tensor(img).type(torch.double)
    return img

def predict_food(img_path):
    targets = [
        'Paniyaram', 'Dhokla', None, 'Upma',
        'Dosa', 'Poori Bhaji', 'Gulab Jamun', 'Naan',
        None, 'Medu Vada', 'Bisi Bele Bath',
        'Tandoori Chicken', 'Chicken Biryani', 'Ven Pongal',
        None, 'Idli', 'Samosa', 'Dudhi Halwa', None,
        'Chapathi'
    ]

    model = PreTrained_Model()
    model = PreTrained_Model.load_from_checkpoint(os.path.join('./utils/', 'mobilenet.ckpt'))
    model.double()
    model.freeze()

    test_X = load_img(img_path)
    pred = nn.Softmax(dim = 1)(model(test_X)).cpu().numpy()
    return targets[np.argmax(pred)]