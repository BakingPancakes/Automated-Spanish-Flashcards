import unittest
from parse import Parse

class TestParse(unittest.TestCase):

    def setUp(self):
        self.parser = Parse()

    def test_CalvoWordToSubword(self):
        self.parser.parseAll()
        calvo_correct = {
            'word':'calvo',
            'translation':'bald',
            'tabs':['Dictionary','Examples','Phrases'],
            'subword':['calvo'],
            'details':[{'subdefinitions': [{'subdefinition': '1. (without hair)', 'subtranslations': [{'subtranslation': 'a. bald', 'example': 'A los 30 ya se estaba quedando calvo, asi que decidiï¿½ raparse la cabeza. At thirty he was already going bald, so he decided to shave his head.'}]}]}]
        }
        contents = self.parser.definition
        self.assertEqual(contents['word'],calvo_correct['word'])
        self.assertEqual(contents['translation'],calvo_correct['translation'])
        self.assertEqual(contents['tabs'],calvo_correct['tabs'])
        self.assertEqual(contents['subword'],calvo_correct['subword'])
        self.assertEqual(contents['details'],calvo_correct['details'])