from os import listdir
from os.path import isfile, join, isdir
from PIL import Image

rawPath = "C:\\Users\\colin\\Documents\\PersonalProjects\\AnimalImages\\raw-img\\"

class Librarian():
    def __init__(self):
        self.folders  = [f for f in listdir(rawPath) if isdir(join(rawPath, f))]
        self.files = dict()
        for folder in self.folders:
            self.files[folder] = [f for f in listdir(f"{rawPath}{folder}\\") if isfile(join(f"{rawPath}{folder}\\", f))]

    def loadFileDirAndName(self, dir, fileName):
        if not dir in self.folders:
            print(f"Error: {dir} was not found in folders")
            return None
        if not fileName in self.files[dir]:
            print(f"Error: {fileName} was not found")
            return None

        return Image.open(f"./raw-img/{dir}/{fileName}")

    
