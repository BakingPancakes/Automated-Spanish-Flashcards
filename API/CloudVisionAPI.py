import os
from pathlib import Path
import sys
from google.cloud import vision

script_directory = Path(__file__).resolve().parent.parent

module_path = os.path.join(script_directory, 'helpers')
sys.path.append(module_path)

from toJPEG import toJPEG

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(script_directory, r'API\credentials\credentials.json')

def detect_text(path)-> list:
    """Detects text in the file."""

    path_obj = Path(path)

    # convert to jpg if png
    if (path_obj.suffix == '.png'):
        toJPEG(path)
        path_obj.with_suffix('.jpg')

    client = vision.ImageAnnotatorClient()

    # read file contents
    with open(str(path_obj), "rb") as image_file:
        content = image_file.read()

    # create vision.Image obj and call Cloud API
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    output_data = ((texts[0].description).split('\n'))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    return output_data

if __name__ == '__main__':


    print(detect_text('imgs/desahogarse.png'))
    #example response:
    # Texts:
    #     "juzgar
    #     to judge
    #     Dictionary Conjugation
    #     juzgar
    #     TRANSITIVE VERB
    #     1. (legal)
    #     Examples
    #     Phrases
    #     a. to judge
    #     El juez que juzgó el caso absolvió a los acusados. - The
    #     judge who judged the case acquitted the accused.
    #     b. to try
    #     No te pueden juzgar dos veces por el mismo delito. -
    #     They cannot try you twice for the same offense."
    #     bounds: (36,25),(1029,25),(1029,821),(36,821)