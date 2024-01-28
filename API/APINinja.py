import requests

def get_image_dataAPI(self,file_name):
    api_url = 'https://api.api-ninjas.com/v1/imagetotext'
    image_file_descriptor = open(file_name, 'rb')
    files = {'image': image_file_descriptor}
    headers = {'X-API-KEY':'Wgq1BYJ0gltIrxZaAOYODA==muNLBCWatY5uTAQD'}
    r = requests.post(api_url, files=files,headers=headers)
    extracted_text = []
    for n in r.json():
        extracted_text.append(n.get('text'))
    return extracted_text

if __name__ == '__main__':
    print(get_image_dataAPI('imgs/juzgar.png'))

