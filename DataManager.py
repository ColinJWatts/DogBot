from Librarian import Librarian
from ImagePacker import ImagePacker
import random

lib = Librarian()

class DataManager():
    def __init__(self, imgSize=300):
        s = 0
        for folder in lib.folders:
            s += len(lib.files[folder])
        self.numDataPoint = s
        self.packer = ImagePacker(imgSize)
        self.numClasses = len(lib.folders)
        return
    
    def loadImageByDataId(self, id):
        if id >= self.numDataPoint:
            return None

        s = 0
        keys = lib.folders
        i = 0
        while s <= id:
            s += len(lib.files[keys[i]])
            i += 1
        i = i - 1
        s = s - len(lib.files[keys[i]])
        idx = id - s
        return self.packer.pack(lib.loadFileDirAndName(keys[i], lib.files[keys[i]][idx]))

    def getLabelFromId(self, id):
        s = 0
        for folder in lib.folders:
            s += len(lib.files[folder])
            if s > id:
                return folder
        return None

    def getRandomIdUniformAcrossData(self):
        return random.randint(0, self.numDataPoint-1)

    def getNRandomIdUniformAcrossData(self, n):
        ids = []
        while len(ids) < n:
            r = self.getRandomIdUniformAcrossData()
            if not r in ids:
                ids.append(r)
        return ids

    def getRandomIdUniformAcrossClasses(self):
        c = random.randint(0, self.numClasses-1)
        r = random.randint(0, len(lib.files[lib.folders[c]]) - 1)

        s = 0
        adding = True
        for folder in lib.folders:
            if folder == lib.folders[c]:
                adding = False
            if adding:
                s += len(lib.files[folder])

        return s + r

    def getNRandomIdUniformAcrossClasses(self, n):
        ids = []
        while len(ids) < n:
            r = self.getRandomIdUniformAcrossClasses()
            if not r in ids:
                ids.append(r)
        return ids

    def getRandomIdFromClass(self, folder):
        r = random.randint(0, len(lib.files[folder]) - 1)
        s = 0
        adding = True
        for f in lib.folders:
            if f == folder:
                adding = False
            if adding:
                s += len(lib.files[f])

        return s + r
    
    def getNRandomIdFromClass(self, folder, n):
        ids = []
        while len(ids) < n:
            r = self.getRandomIdFromClass(folder)
            if not r in ids:
                ids.append(r)
        return ids

    def getFileNameFromId(self, id):
        if id >= self.numDataPoint:
            return None

        s = 0
        keys = lib.folders
        i = 0
        while s <= id:
            s += len(lib.files[keys[i]])
            i += 1
        i = i - 1
        s = s - len(lib.files[keys[i]])
        idx = id - s
        return lib.files[keys[i]][idx]