import ast
from collections import deque
import string

from definition import Definition
from API.ImageToText import ImageToText


class Parse():
    def __init__(self,file_name):
        # read screenshot contents to a list
        itt = ImageToText()
        self.contents = itt.get_image_dataAPI(file_name)
        
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
        
        self.type_indexes = deque()
        [self.type_indexes.append(self.contents.index(type)) for type in self.word_types if type in self.contents]

        numbered_item = 1
        self.numbered_item_indexes = deque()
        for word in self.contents:
            if word == str(numbered_item) + '.':
                self.numbered_item_indexes.append(self.contents.index(word))
                numbered_item += 1

        lettered_item = 'a'
        self.lettered_item_indexes = deque()
        for word in self.contents:
            if word == str(lettered_item) + '.':
                self.lettered_item_indexes.append(self.contents.index(word))
                lettered_item = chr(ord(lettered_item) + 1)

    def parseHeader(self)-> int:
        #! Doesn't check for instances where speaker_symbols are transcribed differently
        #!    by API (besides '#)' and '<'), or if speaker symbols are encountered above word
        #!    (ad, search bar, etc.) since parsing begins at index 0
        #! Doesn't ensure ending keyword is always last thing encountered

        self.definition['word'] = ' '.join(self.contents[0:self.speaker_symbol_indexes[0]])
        try:
            self.definition['translation'] = ' '.join(self.contents[self.speaker_symbol_indexes[0]+1:self.speaker_symbol_indexes[1]])
        except:
            self.definition['translation'] = ' '.join(self.contents[self.speaker_symbol_indexes:self.tabs.index(self.tabs[0])])

        self.definition['tabs'] = self.tabs
    
    def parseSubword(self)-> int:
        #* Scan backwards from type_indexes[i] until 1) Encounters an element from 'tabs'
        #*                                           2) Ecounters a word ending in punctuation
        subwords = []
        #! no more type_indexes -> no other sections, t.f. exit
        try:
            type_index = self.type_indexes[0] # will be accessed again in parseType
            curr_index = type_index - 1
        except: # no more sections (under a type) to parse
            return
        
        while curr_index > 0:
            word = self.contents[curr_index]
            if (word in self.all_tabs) or (word in self.punctuation): # more concise if change while conditon to this?
                self.definition['subword'].append(' '.join(subwords))
                break
            subwords.insert(0,word)
            curr_index -= 1

        match self.parseType(' '.join(subwords)):
            case 'reached end':
                return
            case 'found subword':
                self.parseSubword()

    def parseType(self,subword)-> int:
        #* From type_indexes until next item in numbered_item_indexes
        #! no other numbered_items -> SS is cutoff, t.f. exit
        try:
            type_index = self.type_indexes.popleft()
            number_index = self.numbered_item_indexes[0]
        except:
            return 'reached end'
        self.definition['type'].append(' '.join(self.contents[type_index:number_index]))

        subdefinition_index = 0
        type_index = 0
        match self.parseSubdef(type_index,subdefinition_index):
            case 'reached end':
                return 'reached end'
            case 'found subword': # exit to parse subword to label new subword
                return 'found subword'
            case 'found new type': # exit to parseType and copy last subword
                self.parseType(subword)

    def parseSubdef(self,type_index,subdefinition_index)-> int:
        #* From numbered[i] until next item in lettered_item_indexes
        #! need to check for empty lettered_items_indexes?
        number_index = self.numbered_item_indexes.popleft()
        lettered_index = self.lettered_item_indexes[0] # will be accessed again in parseSubtrans

        new_subdefinition = {'subdefinitions':[
            {'subdefinition':'1. (subdefinition)','subtranslations':[
                {'subtranslation':'a. subtranslation','example':'...'}
            ]} 
        ]}
        new_subdefinition['subdefinitions'][subdefinition_index]['subdefinition'] = ' '.join(self.contents[number_index:lettered_index])

        self.definition['details'].append(new_subdefinition)
        subtranslation_index = 0
        match self.parseSubtrans(type_index,subdefinition_index, subtranslation_index):
            case 'reached end':
                return 'reached end'
            case 'found subword': # exit to parse subword to label new subword
                return 'found subword'
            case 'found numbered_item': # exit to parseSubdef to label new subdefinition
                self.parseSubdef(type_index + 1,subdefinition_index + 1)
            case 'found new type': # exit to parseType and copy last subword
                return 'found new type'

    def parseSubtrans(self,type_index,subdefinition_index, subtranslation_index)-> int:
        #* From lettered_item_indexes until word starting in capital letter
        lettered_index = self.lettered_item_indexes.popleft()
        curr_index = lettered_index
        subtrans = []
        while curr_index < self.length: #! terminates when reaches end of data, but doesn't add all to definition
            word = self.contents[curr_index]
            if word[0] not in string.ascii_letters: # filters out punctuation in first index
                word = word[0:-1]
            if word[0].isupper():
                self.definition['details'][type_index]['subdefinitions'][subdefinition_index]['subtranslations'][subtranslation_index]['subtranslation'] = ' '.join(subtrans)
                break
            subtrans.append(self.contents[curr_index])
            curr_index += 1

        match self.parseExample(type_index,subdefinition_index,subtranslation_index,curr_index):
            case 'reached end':
                return 'reached end'
            
            case 'found lettered_item':
                self.parseSubtrans(type_index,subdefinition_index,subtranslation_index + 1)
            
            case 'found subword': # exit to parse subword to label new subword
                return 'found subword'
            
            case 'found numbered_item': # exit to parseSubdef to label new subdefinition
                return 'found numbered_item'
            
            case 'found new type': # exit to parseType and copy last subword
                return 'found new type'
    
    def parseExample(self,type_index,subdefinition_index,subtranslation_index,curr_index):
        #* Example: From last stop (first word starting in capital letter) - Need to create conditional in case begins with punctuation
        #*          To next letter item, a lowercase letter following a period (subword), next number, word type
        #? conditions could alternatively be met by comparing the order of each index (only applicable to letter item, next number, next type) wouldn't apply to lowercase letter after a period?
        example = []
        while curr_index < self.length:
            word = self.contents[curr_index]      
            if word == '-':
                curr_index += 1
                continue
            if word in self.ending_keyphrases or curr_index+1 == self.length:
                self.definition['details'][type_index]['subdefinitions'][subdefinition_index]['subtranslations'][subtranslation_index]['example'] = ' '.join(example)
                return 'reached end'                
            # True = parse for a subtranslation again
            #! need to check if lettered_item_index is empty
            if len(self.lettered_item_indexes) != 0 and curr_index == self.contents[self.lettered_item_indexes[0]]: #! remove item instead?
                self.definition['details'][type_index]['subdefinitions'][subdefinition_index]['subtranslations'][subtranslation_index]['example'] = ' '.join(example)
                return 'found lettered_item'

            # True = exit to parseSubword to label new subword
            if self.contents[curr_index].endswith('.') and self.contents[curr_index + 1][0].islower():
                self.definition['details'][type_index]['subdefinitions'][subdefinition_index]['subtranslations'][subtranslation_index]['example'] = ' '.join(example)
                return 'found subword'
            
            # True = exit to parseSubdef to label new subdefinition
            if len(self.lettered_item_indexes) != 0 and curr_index == self.contents[self.numbered_item_indexes[0]]: #! remove item instead?
                self.definition['details'][type_index]['subdefinitions'][subdefinition_index]['subtranslations'][subtranslation_index]['example'] = ' '.join(example)
                return 'found numbered_item'
            
            # True = exit to parseType and copy last subword 
            if self.contents[curr_index] in self.word_types:
                self.definition['details'][subdefinition_index]['subdefinitions'][subtranslation_index]['example'] = ' '.join(example)
                return 'found new type'
            
            example.append(word)
            curr_index += 1

    def parseAll(self):
        """Finds the identity of each label by 
            finding the position of each in relation to each other.
            Returns the labeled definition information."""

        # TODO: Pop-ups before word, and 'Usage note' after translation
        self.parseHeader()
        self.parseSubword()

if __name__ == '__main__':
    parserCalvo = Parse('imgs/calvo.png')
    # print(parserCalvo.contents)
    parserCalvo.parseAll()
    print(parserCalvo.definition)