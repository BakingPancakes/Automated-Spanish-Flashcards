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
            'tabs':[['Dictionary','Examples','Phrases']],
            'subword':['calvo']
        }
        contents = self.parser.definition
        self.assertEqual(contents['word'],calvo_correct['word'])
        self.assertEqual(contents['translation'],calvo_correct['translation'])
        self.assertEqual(contents['tabs'],calvo_correct['tabs'])
        self.assertEqual(contents['subword'],calvo_correct['subword'])