from PIL import Image
from pathlib import Path

def toJPEG(file_path):
    '''Converts png to jpeg. Throws an error if not png'''
    #TODO: reject files that aren't image extensions?
    path_obj = Path(file_path)

    if (path_obj.suffix != '.png'):
        raise ValueError('Invalid file extension. Please only provide files with .png') # rejects files that are already .jpg
    
    im = Image.open(file_path)
    rgb_im = im.convert('RGB')
    rgb_im.save(path_obj.with_suffix('.jpg'))

if __name__ == '__main__':
    toJPEG('imgs/desahogarse.png')