import ast
from definition import *


class Parse():
    def __init__(self):
        with open('raw_data/calvo.txt', 'r') as f:
            contents = f.read()
        self.contents = ast.literal_eval(contents) # a list of text top left-bottom right, separated by space
        self.definition = Definition().definition
        
        # constants
        self.length = len(self.contents)
        self.speaker_symbols = ['#)','<']
        self.tabs = ['Dictionary','Conjugation','Examples','Phrases']

        # utility for logic


    def parse(self):
        # ! following assumes speaker_symbols isn't encountered in an ad, etc.
        # TODO: Pop-ups before word, and 'Usage note' after translation
        #? make a global var for self.content[i]? or does the manipulation of i within code make this difficult
        i = 0 # global position, can't use i if in for loop
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
                continue

            #* tabs
            if self.contents[i] in self.tabs:
                self.definition['tabs'].append(self.contents[i])
                break

            i += 1


parser = Parse()
parser.parse()
contents = parser.definition
print(contents)
