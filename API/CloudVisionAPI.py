import os
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'C:\Users\zavie\VS_Code_Files\QuirkyProjects\SpanishFlashcards\API\deductive-tempo-411820-e309e4ebb1cb.json'

def detect_text(path):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")

    for text in texts:
        print(f'\n"{text.description}"')

        vertices = [
            f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        ]

        print("bounds: {}".format(",".join(vertices)))

    

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

if __name__ == '__main__':
    detect_text('imgs/juzgar.jpg')
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