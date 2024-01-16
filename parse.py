import ast
from definition import *


class Parse():
    def __init__(self):
        # read screenshot contents to a list
        with open('raw_data/calvo.txt', 'r') as f:
            contents = f.read()
        self.contents = ast.literal_eval(contents) # a list of text top left-bottom right, separated by space
        
        # initialize definition object
        self.definition = Definition().definition
        
        # constants
        self.length = len(self.contents)
        self.speaker_symbols = ['#)','<']
        self.tabs = ['Dictionary','Conjugation','Examples','Phrases']
        self.word_types = ['TRANSITIVE','INTRANSITIVE','PRONOMINAL','REFLEXIVE','RECIPROCAL','MASCULINE','FEMININE','ADJECTIVE','PHRASE','INTERJECTION','PRONOUN','ADVERB','PREPOSITION','CONJUNCTION','ARTICLE']

        # utility for logic
        self.subdefinition_number = 1
        self.subtranslation_letter = 'a'

    def parseHeader(self,i)-> int:
        #! doesn't check for instances where speaker_symbols are transcribed differently by API
        #! list comprehension through whole contnets might be inefficient with large screenshots

        speaker_symbol_indexes = [self.contents.index(symbol) for symbol in self.speaker_symbols if symbol in self.contents]
        self.definition['word'] = ' '.join(self.contents[0:speaker_symbol_indexes[0]])
        self.definition['translation'] = ' '.join(self.contents[speaker_symbol_indexes[0]+1:speaker_symbol_indexes[1]])
        i += speaker_symbol_indexes[-1] + 1

        tabs = [tab for tab in self.tabs if tab in self.contents]
        self.definition['tabs'].append(tabs)
        i += len(tabs)

        return i
    
    def parseSubword(self,i)-> int:
        subwords = []
        while self.contents[i] not in self.word_types:
            subwords.append(self.contents[i])
            if self.contents[i+1] in self.word_types:
                self.definition['subword'].append(" ".join(subwords))
                i += 1
                break
            i += 1
        return i
    
    def parseType(self,i)-> int:
        # if self.contents[i].startswith((str(self.subdefinition_number) + '.')):
            #     break
        return i

    def parseSubdef(self,i)-> int:
        return i

    def parseSubtrans(self,i)-> int:
        return i

    def parseAll(self):
        """finds the identity of each label by finding the position of each in relation to each other """

        # ! following assumes speaker_symbols isn't encountered in an ad, etc.
        # TODO: Pop-ups before word, and 'Usage note' after translation
        #? make a global var for self.content[i]? or does the manipulation of i within code make this difficult
        
        i = 0 # global position index of contents
        i = self.parseHeader(i)
        i = self.parseSubword(i)
        while self.contents[i] != 'Copyright':
            i = self.parseType(i)
            i = self.parseSubdef(i)
            i = self.parseSubtrans(i)
            break # temporary
            
            #* increments index at end of run NOTE: index can increment throughout code
            i += 1


parser = Parse()
parser.parseAll()
contents = parser.definition
print(contents)
