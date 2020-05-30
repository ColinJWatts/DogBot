import numpy as np 
import torch
import torch.nn as nn
import torch.nn.functional as F

class BinaryImageClassifier(nn.Module):
    def __init__(self, imgSize):
        super(BinaryImageClassifier, self).__init__()

        temp = float(imgSize)
        while temp > 1:
            temp = temp / 2
        if temp < 1:
            print("IMG SIZE NOT A POWER OF 2")

        self.imgSize = imgSize
        #Input channels = 3, output channels = 16
        self.numOutputChannels = 32
        self.conv1 = torch.nn.Conv2d(3, self.numOutputChannels, kernel_size=5, stride=1, padding=2)
        self.pool = torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        
        #4608 input features, 64 output features (see sizing flow below)
        self.fc1 = torch.nn.Linear(self.numOutputChannels * int(imgSize/2) * int(imgSize/2), 64)
        
        #64 input features, 10 output features for our 10 defined classes
        self.fc2 = torch.nn.Linear(64, 1)
        
    def forward(self, x):
        #Computes the activation of the first convolution
        #Size changes from (3, 32, 32) to (18, 32, 32)
        x = F.relu(self.conv1(x))
        
        #Size changes from (18, 32, 32) to (18, 16, 16)
        x = self.pool(x)
        
        #Reshape data to input to the input layer of the neural net
        #Size changes from (18, 16, 16) to (1, 4608)
        #Recall that the -1 infers this dimension from the other given dimension
        x = x.view(-1, self.numOutputChannels * int(self.imgSize/2) * int(self.imgSize/2))
        
        #Computes the activation of the first fully connected layer
        #Size changes from (1, 4608) to (1, 64)
        x = F.relu(self.fc1(x))
        
        #Computes the second fully connected layer (activation applied later)
        #Size changes from (1, 64) to (1, 10)
        x = torch.sigmoid(self.fc2(x))
        return(x)

class ImgDataSet(torch.utils.data.Dataset):
    def __init__(self, ids, dataManager, normalize):
        self.ids = ids
        self.mngr = dataManager
        self.normalize = normalize

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, idx):
        label = self.mngr.getLabelFromId(self.ids[idx])
        img = self.normalize(self.mngr.loadImageByDataId(self.ids[idx]).convert('RGB'))
        return img, label