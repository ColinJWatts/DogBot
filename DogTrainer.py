from DataManager import DataManager
from BinaryClassifierCNN import BinaryImageClassifier
from BinaryClassifierCNN import ImgDataSet
import torch
import torchvision.transforms as transforms
import torch.optim as optim
import torch.nn as nn
import torch.utils.data as data
import numpy as np
from PIL import Image
import random

NUMEPOCH = 15
BATCHSIZE = 20

class DogTrainer():
    # initiallize DogTrainer with the size images will be compressed to and an array of integers 
    # corresponding to image ids from the DataManager
    def __init__(self, imgSize, trainingImgIds):
        self.imgSize = imgSize
        self.mgr = DataManager(imgSize=imgSize)
        self.model = BinaryImageClassifier(self.imgSize)
        self.model.train()
        self.trans = transforms.ToTensor()
        self.getNormParameters(trainingImgIds)

        optimizer = optim.Adam(self.model.parameters())
        optimizer.zero_grad()

        criteria = nn.BCELoss()
        loader = data.DataLoader(ImgDataSet(trainingImgIds, self.mgr, self.normalizeImg), batch_size=BATCHSIZE, shuffle=True)

        for epoch in range(NUMEPOCH):
            print(f"Epoch: {epoch}")

            for i, (images, labels) in enumerate(loader):
                target = []
                for l in labels:
                    if l == "dog":
                        target.append(1)
                    else:
                        target.append(0)
                outputs = self.model(images)
                loss = criteria(outputs, torch.Tensor(target).unsqueeze(1))

                # Backprop and perform Adam optimisation
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        self.model.eval()

    def getNormParameters(self, imgIds):
        rs = []
        gs = []
        bs = []
        for id in imgIds:
            img = self.mgr.loadImageByDataId(id).convert("RGB")
            imgData = list(img.getdata())
            for pixel in imgData:
                rs.append(pixel[0])
                gs.append(pixel[1])
                bs.append(pixel[2])
        self.means = [0,0,0]
        self.stds = [0,0,0]

        self.means[0] = sum(rs)/len(rs)
        self.means[1] = sum(gs)/len(gs)
        self.means[2] = sum(bs)/len(bs)
        self.stds[0] = np.std(rs)
        self.stds[1] = np.std(gs)
        self.stds[2] = np.std(bs)
        self.mgr.packer.setFill((int(self.means[0]), int(self.means[1]), int(self.means[2])))
        print((self.means, self.stds))

    def normalizeImg(self, img):
        imgData = list(img.getdata())
        newImg = [[[]], [[]], [[]]]
        w = 0
        h = 0
        for pixel in imgData:
            newImg[0][h].append((pixel[0] - self.means[0])/self.stds[0])
            newImg[1][h].append((pixel[1] - self.means[1])/self.stds[1])
            newImg[2][h].append((pixel[2] - self.means[2])/self.stds[2])
            w = (w + 1) % self.imgSize
            if w == 0:
                h += 1
                if h != self.imgSize:
                    newImg[0].append([])
                    newImg[1].append([])
                    newImg[2].append([])

        tensor = torch.Tensor(newImg)
        return tensor

    def getPredictionOnImgId(self, id):
        img = self.mgr.loadImageByDataId(id).convert("RGB")
        temp = self.normalizeImg(img)
        return self.model(temp.unsqueeze(0))

    def getPredictionOnImg(self, img):
        img = img.convert("RGB")
        temp = self.normalizeImg(img)
        return self.model(temp.unsqueeze(0))
    
    def evaluate(self, testImgsIds):
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        for id in testImgsIds:
            label = self.getLabel(id)[0].item()
            prediction = self.getPredictionOnImgId(id)
            if prediction[0].item() > 0.5:
                if label == 1:
                    tp += 1
                if label == 0:
                    fn += 1
            if prediction[0].item() < 0.5:
                if label == 1:
                    fp += 1
                if label == 0:
                    tn += 1

        return tp, tn, fp, fn

    def getLabel(self, id): 
        l = self.mgr.getLabelFromId(id)
        label = 0
        if l == "dog":
            label = 1
        target = torch.Tensor([label])
        return target.view(-1,1)