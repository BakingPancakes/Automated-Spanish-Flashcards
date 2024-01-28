from typing import Optional, Sequence
import os

from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

# add credentials to environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'C:\Users\zavie\VS_Code_Files\QuirkyProjects\SpanishFlashcards\API\credentials.json'

project_id = "deductive-tempo-411820"
location = "us" # Format is "us" or "eu"
processor_id = "8db6d0408b28916b" # Create processor before running sample
file_path = "/path/to/local/pdf"
mime_type = "image/jpeg" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
field_mask = "text,pages"  # Optional. The fields to return in the Document object. others include entities
processor_version_id = "YOUR_PROCESSOR_VERSION_ID" # Optional. Processor version to use

#TODO: remove parts that probably don't need, like processor_version_id and field_mask
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

    output = []
    overall_text = document.text
    print_paragraphs(document.pages[0].paragraphs, overall_text)

    #     return "".join(
    #     overall_text[int(segment.start_index) : int(segment.end_index)]
    #     for segment in layout.text_anchor.text_segments
    # )

        # try:
        #     start_index = paragraph.layout.text_anchor.text_segments[0].start_index
        #     end_index = paragraph.layout.text_anchor.text_segments[1].end_index
        #     output.append(overall_text[start_index:end_index])
        #     overall_text = overall_text[end_index:]
        # except: # first paragraph doesn't have a start_index
        #     end_index = paragraph.layout.text_anchor.text_segments[0].end_index
        #     output.append(overall_text[:end_index])
        #     overall_text = overall_text[end_index:]

    # return the recognition output from the processor
    # return document.pages
    # return document.text.split('\n')

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



if __name__ == '__main__':
    print(process_document('imgs/etiquetar.jpg'))
    # for item in (process_document('imgs/etiquetar.jpg')):
    #     print(item)