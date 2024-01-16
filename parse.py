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
        while i < self.length:
            #* word and translation
            if self.contents[i] in self.speaker_symbols: # identifies where word is in relation to speaker
                self.definition['word'] = ' '.join(self.contents[0:i])

                for j in range(i,self.length):
                    i += 1
                    self.definition['translation'] += self.contents[i]
                    #? also use join for tranlation for sleeker code?

                    if self.contents[j] in self.speaker_symbols:
                        i += j + 1
                        break
                    self.definition['translation'] += ' '
                    i += 1

            #* tabs
            if self.contents[i] in self.tabs:
                while self.contents[i] in self.tabs:
                    self.definition['tabs'].append(self.contents[i])
                    i += 1
                break

            i += 1
        return i
    
    def parseSubword(self,i)-> int:
        while self.contents[i] not in self.word_types:
            subwords = []
            subwords.append(self.contents[i])
            if self.contents[i+1] in self.word_types:
                self.definition['subword'] = " ".join(subwords)
                i += 1
                break
            i += 1
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

            #* type
            # if self.contents[i].startswith((str(self.subdefinition_number) + '.')):
            #     break          

            #* increments index at end of run NOTE: index can increment throughout code
            i += 1


parser = Parse()
parser.parseAll()
contents = parser.definition
print(contents)
