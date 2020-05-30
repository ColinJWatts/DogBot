from DogTrainer import DogTrainer
from DataManager import DataManager
import random
from PIL import Image
from ImagePacker import ImagePacker

class DogModel():
    def __init__(self, imgSize=128):
        self.imgSize = imgSize
        trained = False

        manager = DataManager(imgSize)
        dogSet = manager.getNRandomIdFromClass("dog", 1500)
        otherSet = manager.getNRandomIdFromClass("notdog", 300)
        otherSet = otherSet + manager.getNRandomIdFromClass("sheep", 100)
        otherSet = otherSet + manager.getNRandomIdFromClass("cow", 100)
        otherSet = otherSet + manager.getNRandomIdFromClass("cat", 100)
        otherSet = otherSet + manager.getNRandomIdFromClass("butterfly", 100)
        otherSet = otherSet + manager.getNRandomIdFromClass("chicken", 100)
        otherSet = otherSet + manager.getNRandomIdFromClass("elephant", 100)
        otherSet = otherSet + manager.getNRandomIdFromClass("horse", 100)
        otherSet = otherSet + manager.getNRandomIdFromClass("squirrel", 100)
        otherSet = otherSet + manager.getNRandomIdFromClass("spider", 100)

        trainingSet = dogSet + otherSet

        while not trained:
            random.shuffle(trainingSet)

            model = DogTrainer(imgSize, trainingSet)

            dogTestSet = manager.getNRandomIdFromClass("dog", 1500)
            otherTestSet = manager.getNRandomIdFromClass("notdog", 300)
            otherTestSet = otherTestSet + manager.getNRandomIdFromClass("sheep", 100)
            otherTestSet = otherTestSet + manager.getNRandomIdFromClass("cow", 100)
            otherTestSet = otherTestSet + manager.getNRandomIdFromClass("cat", 100)
            otherTestSet = otherTestSet + manager.getNRandomIdFromClass("butterfly", 100)
            otherTestSet = otherTestSet + manager.getNRandomIdFromClass("chicken", 100)
            otherTestSet = otherTestSet + manager.getNRandomIdFromClass("elephant", 100)
            otherTestSet = otherTestSet + manager.getNRandomIdFromClass("horse", 100)
            otherTestSet = otherTestSet + manager.getNRandomIdFromClass("squirrel", 100)
            otherTestSet = otherTestSet + manager.getNRandomIdFromClass("spider", 100)

            testSet = dogTestSet + otherTestSet

            tp, tn, fp, fn = model.evaluate(testSet)
            trained = True
            print(f"Accuracy: {int(10000 * (tp + tn)/(tp+ tn+ fp+ fn))/100}%")
            if (tp + tn)/(tp+ tn+ fp+ fn) < 0.7:
                print("fuck")
                trained = False

        self.model = model

    def isDog(self, filename):
        img = Image.open(f"./collectedImages/{filename}")
        packer = ImagePacker(self.imgSize)
        pred = self.model.getPredictionOnImg(packer.pack(img))

        if pred[0].item() >= 0.5:
            return True
        return False