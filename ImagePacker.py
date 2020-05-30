from PIL import Image
from PIL import ImageOps

class ImagePacker():
    def __init__(self, maxDim):
        self.maxDim = maxDim
        self.isFillSet = False

    def pack(self, img):
        if img.width > self.maxDim or img.height > self.maxDim:
            w = img.width
            h = img.height
            if img.width >= img.height:
                w = self.maxDim
                h = int(self.maxDim * (img.height / img.width))
            else:
                h = self.maxDim
                w = int(self.maxDim * (img.width / img.height))
            img = img.resize((w,h))
        
        delta_w = self.maxDim - img.width
        delta_h = self.maxDim - img.height
        padding = (delta_w//2, delta_h//2, delta_w-(delta_w//2), delta_h-(delta_h//2))

        fill = None
        if not self.isFillSet:
            rs = []
            gs = []
            bs = []
            i = img.convert("RGB")
            imgData = list(i.getdata())
            for pixel in imgData:
                rs.append(pixel[0])
                gs.append(pixel[1])
                bs.append(pixel[2])
            means = [0,0,0]

            means[0] = sum(rs)/len(rs)
            means[1] = sum(gs)/len(gs)
            means[2] = sum(bs)/len(bs)

            fill = int(self.rgb_to_hex((int(means[0]), int(means[1]), int(means[2]))), 0)
        else:
            fill = self.f

        return ImageOps.expand(img, padding, fill)

    def rgb_to_hex(self, rgb):
        return '0x%02x%02x%02x' % rgb

    def setFill(self, rgb):
        self.f = int(self.rgb_to_hex(rgb), 0)
        self.isFillSet = True