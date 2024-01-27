from PIL import Image
import os, sys

def toJPEG(fileName):
    '''Ommit the file type (for example .png)'''
    im = Image.open(fileName + '.png')
    rgb_im = im.convert('RGB')
    # rgb_im = Image.new('RGB', im.size, (255,255,255))
    rgb_im.save(fileName + '.jpg')

if __name__ == '__main__':
    toJPEG('imgs/calvo')