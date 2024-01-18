import ast
from definition import *


class Parse():
    def __init__(self):
        # read screenshot contents to a list
        #! this should be moved to future main.py function instead of initialized here
        with open('raw_data/calvo.txt', 'r') as f:
            contents = f.read()
        self.contents = ast.literal_eval(contents) # a list of text top left-bottom right, separated by space
        
        # initialize definition object
        self.definition = Definition().definition
        
        # constants
        self.length = len(self.contents) #? necessary?
        self.speaker_symbols = ['#)','<']
        self.tabs = ['Dictionary','Conjugation','Examples','Phrases']
        self.word_types = ['TRANSITIVE','INTRANSITIVE','PRONOMINAL','REFLEXIVE','RECIPROCAL','MASCULINE','FEMININE','ADJECTIVE','PHRASE','INTERJECTION','PRONOUN','ADVERB','PREPOSITION','CONJUNCTION','ARTICLE']
        #! keyphrases don't consider what emojis were transcribed to
        self.ending_keyphrases = ['Try Premium','Unlock Premium','Get Ahead With Premium','Copyright']

        # find indexes of anchor-points (iterates total of 5 times + calls for index(word))
        #! should limit symbol + tabs to only scan within first ~20 words
        self.speaker_symbol_indexes = [self.contents.index(symbol) for symbol in self.speaker_symbols if symbol in self.contents]
        self.tabs = [tab for tab in self.tabs if tab in self.contents] # doesn't need to find indexes
        self.word_type_indexes = [self.contents.index(type) for type in self.word_types if type in self.contents]
        
        numbered_item = 1
        numbered_item_indexes = []
        for word in self.contents:
            if word == str(numbered_item) + '.':
                numbered_item_indexes.append(self.contents.index(word))
                numbered_item += 1
        self.numbered_item_indexes = numbered_item_indexes

        lettered_item = 'a'
        lettered_item_indexes = []
        for word in self.contents:
            if word == str(lettered_item) + '.':
                lettered_item_indexes.append(self.contents.index(word))
                lettered_item = chr(ord(lettered_item) + 1)
        self.lettered_item_indexes = lettered_item_indexes

    def parseHeader(self,i)-> int:
        #! Doesn't check for instances where speaker_symbols are transcribed differently
        #!    by API (besides '#)' and '<'), or if speaker symbols are encountered above word
        #!    (ad, search bar, etc.) since parsing begins at index 0
        #! Doesn't ensure ending keyword is always last thing encountered

        self.definition['word'] = ' '.join(self.contents[0:self.speaker_symbol_indexes[0]])
        self.definition['translation'] = ' '.join(self.contents[self.speaker_symbol_indexes[0]+1:self.speaker_symbol_indexes[1]])
        i += self.speaker_symbol_indexes[-1] + 1

        self.definition['tabs'].append(self.tabs)
        i += len(self.tabs)

        return i
    
    def parseSubword(self,i)-> int:
        subwords = []
        while self.contents[i] not in self.word_types: # as long as word isn't a word type, ex. MASCULINE
            subwords.append(self.contents[i])          # add term as part of subword
            if self.contents[i+1] in self.word_types:  # check if next word is word type
                self.definition['subword'].append(" ".join(subwords)) # if a word type, add subwords, exit loop
                i += 1
                break
            i += 1
        return i
    
    def parseType(self,i)-> int:
        if self.contents[i].startswith((str(self.numbered_item_indexes[0]) + '.')):
            pass
        return i

    def parseSubdef(self,i)-> int:
        return i

    def parseSubtrans(self,i)-> int:
        return i
    
    def checkEndingKeyword(self,i):
        pass # should check if position is one of ending_keyphrases

    def parseAll(self):
        """Finds the identity of each label by 
            finding the position of each in relation to each other."""

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
