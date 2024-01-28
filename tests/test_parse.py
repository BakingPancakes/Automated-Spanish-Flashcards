import unittest
import os, sys
from pathlib import Path

module_path = os.path.join(Path(__file__).resolve().parent.parent)
sys.path.append(module_path)
from parse import Parse

from API.CloudVisionAPI import detect_text
from API.DocumentAI import process_document_sample

class TestParse(unittest.TestCase):

    def setUp(self):
        self.parserNinja = Parse('imgs/calvo.png',APINinja=True)
        self.parserVision = Parse('imgs/etiquetar.png',CloudVisionAPI=True)
        self.parserDocument = Parse('imgs/etiquetar.png',DocumentAI=True)

    def test_CalvoWordToSubwordNinja(self):
        self.parserNinja.parseAll()
        calvo_correct = {
            'word':'calvo',
            'translation':'bald',
            'tabs':['Dictionary','Examples','Phrases'],
            'subword':['calvo'],
            'details':[
                {'subdefinitions':
                 [{'subdefinition': '1. (without hair)', 'subtranslations': 
                   [{'subtranslation': 'a. bald', 'example': 'A los 30 ya se estaba quedando calvo, así que decidió raparse la cabeza. At thirty he was already going bald, so he decided to shave his head.'}]
                 }]
                }]
        }
        contents = self.parserNinja.definition
        self.assertEqual(contents['word'],calvo_correct['word'])
        self.assertEqual(contents['translation'],calvo_correct['translation'])
        self.assertEqual(contents['tabs'],calvo_correct['tabs'])
        self.assertEqual(contents['subword'],calvo_correct['subword'])
        #! detials will always fail because APINinja transcribes special characters incorrectly
        self.assertEqual(contents['details'],calvo_correct['details'])

    def test_CloudVisionVSDocumentAI(self):
        for i in range(len(self.parserVision.contents)):
            self.assertEqual(self.parserDocument.contents[i],self.parserVision.contents[i])