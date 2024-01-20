import requests

class ImageToText():
    def __init__(self,):
        pass

    def get_image_dataAPI(self,file_name):
        api_url = 'https://api.api-ninjas.com/v1/imagetotext'
        image_file_descriptor = open(file_name, 'rb')
        files = {'image': image_file_descriptor}
        headers = {'X-API-KEY':'Wgq1BYJ0gltIrxZaAOYODA==muNLBCWatY5uTAQD'}
        r = requests.post(api_url, files=files,headers=headers)
        extracted_text = []
        for n in r.json(): # since r provides extra junk, this takes out only the text
            extracted_text.append(n.get('text'))
        return extracted_text

if __name__ == '__main__':
    imagetotext = ImageToText()
    print(imagetotext.get_image_dataAPI('imgs/nalgada.png'))

