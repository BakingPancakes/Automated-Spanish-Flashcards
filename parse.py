import ast
from queue import Queue
import string

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
        self.punctuation = string.punctuation.replace("()","")
        self.speaker_symbols = ['#)','<']
        self.all_tabs = ['Dictionary','Conjugation','Examples','Phrases']
        self.word_types = ['TRANSITIVE','INTRANSITIVE','PRONOMINAL','REFLEXIVE','RECIPROCAL','MASCULINE','FEMININE','ADJECTIVE','PHRASE','INTERJECTION','PRONOUN','ADVERB','PREPOSITION','CONJUNCTION','ARTICLE']
        #! keyphrases don't consider what emojis were transcribed to (random symbols or the emoji itself)
        self.ending_keyphrases = ['Try Premium','Unlock Premium','Get Ahead With Premium','Copyright']

        # store indexes of anchor-points (iterates total of 5 times + calls for index(word))
        #! should limit symbol + tabs to only scan within first ~20 words
        self.speaker_symbol_indexes = [self.contents.index(symbol) for symbol in self.speaker_symbols if symbol in self.contents]
        self.tabs = [tab for tab in self.all_tabs if tab in self.contents] # doesn't need to find indexes
        self.type_indexes = Queue()
        [self.type_indexes.put(self.contents.index(type)) for type in self.word_types if type in self.contents]

        numbered_item = 1
        self.numbered_item_indexes = Queue()
        for word in self.contents:
            if word == str(numbered_item) + '.':
                self.numbered_item_indexes.put(self.contents.index(word))
                numbered_item += 1

        lettered_item = 'a'
        self.lettered_item_indexes = Queue()
        for word in self.contents:
            if word == str(lettered_item) + '.':
                self.lettered_item_indexes.put(self.contents.index(word))
                lettered_item = chr(ord(lettered_item) + 1)

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
        #* Scan backwards from type_indexes[i] until 1) Encounters an element from 'tabs'
        #*                                           2) Ecounters a word ending in punctuation
        subwords = []
        type_index = self.type_indexes.get(False) # will be accessed again in parseType
        curr_index = type_index - 1
        while curr_index > 0:
            word = self.contents[curr_index]
            if (word in self.all_tabs) or (word in self.punctuation): # more concise if change while conditon to this?
                self.definition['subword'].append(' '.join(subwords))
                break
            subwords.insert(0,word)
            curr_index -= 1

    def parseType(self,i)-> int:
        #* From type_indexes until next item in numbered_item_indexes
        type_index = self.type_indexes.get()
        number_index = self.numbered_item_indexes.get(False) # will be accessed again in parseSubdef
        self.definition['type'].append(self.contents[type_index+1:number_index])
        return i

    def parseSubdef(self,i)-> int:
        #* From numbered[i] until next item in lettered_item_indexes
        number_index = self.numbered_item_indexes.get()
        lettered_index = self.lettered_item_indexes.get(False) # will be accessed again in parseSubtrans
        new_subdefinition = {'subdefinitions':[
            {'subdefinition':'1. (subdefinition)','subtranslations':[
                {'subtranslation':'a. subtranslation','example':'...'}
            ]} 
        ]}
        subdefinition_index = 0
        #! need a method of keeping track of subdefinition indexes between adding subtranslations
        new_subdefinition['subdefinitions'][subdefinition_index]['subdefinition'] = self.contents[number_index:lettered_index]

        self.definition['details'].append(new_subdefinition)
        # some conditional that ends when parsesubtrans says so
        self.parseSubtrans(0,subdefinition_index)
        return i

    def parseSubtrans(self,i,subdefinition_index)-> int:
        #* From lettered_item_indexes until word starting in capital letter
        lettered_index = self.lettered_item_indexes.get()
        curr_index = lettered_index
        subtrans = []
        subtranslation_index = 0 #! increments if there are more subtranslations
        while curr_index < self.length: #! terminates when reaches end of data, but doesn't add all to definition
            word = self.contents[curr_index]
            for item in self.punctuation:
                if item in word:
                    word.replace(item,'')
            if word[0].isupper():
                self.definition['details'][subdefinition_index]['subdefinitions'][subtranslation_index]['subtranslation'] = ' '.join(subtrans)
                break
            subtrans.append(self.contents[curr_index])
            curr_index += 1

        match self.parseExample(curr_index):
            case 'found lettered_item':
                self.parseSubtrans(0, subtranslation_index + 1)
            
            case 'found subword': # exit to parse subword to label new subword
                return 'found subword' #! parseSubtrans call needs to check for this and parse subword again
            
            case 'found numbered_item': # exit to parseSubdef to label new subdefinition
                return 'found numbered_item'
            
            case 'found word_type': # exit to parseType and copy last subword
                return 'found word_type'

        return i
    
    def parseExample(self,curr_index):
        #* Example: From last stop (first word starting in capital letter) - Need to create conditional in case begins with punctuation
        #*          To next letter item, a lowercase letter following a period (subword), next number, word type
        #? conditions could alternatively be met by comparing the order of each index (only applicable to letter item, next number, next type) wouldn't apply to lowercase letter after a period?
        while curr_index < self.length:
            word = self.contents[curr_index]            
            # True = parse for a subtranslation again
            if curr_index == self.contents[self.lettered_item_indexes.get(False)]:
                return 'found lettered_item'
            
            # True = exit to parseSubword to label new subword
            if self.contents[curr_index].endswith('.') and self.contents[curr_index][0].islower():
                return 'found subword'
            
            # True = exit to parseSubdef to label new subdefinition
            if curr_index == self.contents[self.numbered_item_indexes.get(False)]:
                return 'found numbered_item'
            
            # True = exit to parseType and copy last subword 
            if self.contents[curr_index] in self.word_types:
                return 'found word_type'
            curr_index += 1
    
    def checkEndingKeyword(self,i):
        # should check if position is one of ending_keyphrases
        pass 

    def parseAll(self):
        """Finds the identity of each label by 
            finding the position of each in relation to each other."""

        # TODO: Pop-ups before word, and 'Usage note' after translation
        #? make a global var for self.content[i]? or does the manipulation of i within code make this difficult
        
        i = 0 # global position index of contents
        i = self.parseHeader(i)
        i = self.parseSubword(i)
        wontRunYet = False
        if wontRunYet:
            while self.contents[i] != 'Copyright':
                i = self.parseType(i)
                i = self.parseSubdef(i)
                i = self.parseSubtrans(i)
                break # temporary
                
                #* increments index at end of run NOTE: index can increment throughout code
                i += 1

parser = Parse()
parser.parseAll()
print(parser.definition)