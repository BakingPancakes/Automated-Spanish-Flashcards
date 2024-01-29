import json
from pathlib import Path
from typing import Optional, Sequence
import os

from google.api_core.client_options import ClientOptions
from google.cloud import documentai 

# add credentials to environment variable
script_directory = Path(__file__).resolve().parent.parent
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(script_directory, r'API\credentials\credentials.json')

project_id = "deductive-tempo-411820"
location = "us"
processor_id = "8db6d0408b28916b"
file_path = "/path/to/local/pdf"
mime_type = "image/jpeg"
field_mask = "text,pages" 

all_tabs = ['Dictionary','Conjugation','Examples','Phrases']

def process_document(
    file_path: str,
    field_mask: Optional[str] = None
) -> None:
    # You must set the `api_endpoint` if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # For more information: https://cloud.google.com/document-ai/docs/reference/rest/v1/ProcessOptions
    # Optional: Additional configurations for processing.
    process_options = documentai.ProcessOptions(
        # Process only specific pages
        individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
            pages=[1]
        )
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        field_mask=field_mask,
        process_options=process_options,
    )

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    document = result.document
    return format_document(document)

def print_paragraphs(
    paragraphs: Sequence[documentai.Document.Page.Paragraph], text: str
) -> None:
    for paragraph in range(len(paragraphs)):
        paragraph_text = layout_to_text(paragraphs[paragraph].layout, text)
        print(repr(paragraph_text))

def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document"s text. This function converts
    offsets to a string.
    """
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    return "".join(
        text[int(segment.start_index) : int(segment.end_index)]
        for segment in layout.text_anchor.text_segments
    )

def format_document(document: documentai.Document):

    ## uses given start_index and end_index to attempt to parse where DocumentAI believes each line begins/starts
    # output = []
    # overall_text = document.text
    # for paragraph in document.pages[0].paragraphs:
    #     try:
    #         start_index = paragraph.layout.text_anchor.text_segments[0].start_index
    #         end_index = paragraph.layout.text_anchor.text_segments[1].end_index
    #         output.append(overall_text[start_index:end_index] + f"start: {start_index}, end: {end_index}")
    #         overall_text = overall_text[end_index:]
    #     except: # first paragraph doesn't have a start_index
    #         end_index = paragraph.layout.text_anchor.text_segments[0].end_index
    #         output.append(overall_text[:end_index] + f'end: {end_index}')
    #         overall_text = overall_text[end_index:]
    # return output

    ## Using Google's version of finding paragraph divides
    # print_paragraphs(document.pages[0].paragraphs, overall_text)

    ## Find line divides in document.text via \n
    return document.text.split('\n')

def format_json(file: str) -> list:
    '''Takes json format of image and just outputs start and end index for every paragraph.'''
    with open(file) as f:
        data = json.load(f)
        output = []
        for paragraph in data['pages'][0]['paragraphs']:
            try:
                start_index = paragraph['layout']['textAnchor']['textSegments'][0]['startIndex']
                end_index = paragraph['layout']['textAnchor']['textSegments'][0]['endIndex']
                output.append(f"{start_index} : {end_index}")
            except:
                end_index = paragraph['layout']['textAnchor']['textSegments'][0]['endIndex']
                output.append(f'{end_index}')
        output.append(len(data['text']))
        return output

def get_header_word(file: str) -> str:
    '''Returns the predicted header word, ie the word requesting translation'''
    document_text = process_document(file)
    for line_index in range(len(document_text)):
        line = document_text[line_index].split(' ')

        for word in line:
            if word in all_tabs:
                return document_text[line_index-2]
    
    return "Word not found."

if __name__ == '__main__':
    # for item in (process_document('imgs/juzgar.jpg')):
    #     print(item)
    # for item in (format_json("raw_data/etiquetar.json")):
    #     print(item)
    print(get_header_word('imgs/etiquetar.jpg'))