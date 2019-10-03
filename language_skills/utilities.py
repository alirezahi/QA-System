import pandas as pd
import math

posTypeDict = {
    'naghshi': ['Jr-'],
    'mohtavai': ['Nasp---', 'Ncsp--z'],
    'bon': ['Vpykshs----']
}

class Analyser():
    def __init__(self, words):
        self.words = words
        self.freq_dict = 0
        self.freq_1_count = 0
        self.char_count = 0
        self.type_count = 0
        self.token_count = 0
        self.sentence_count = 0
        self.average_word_len = 0
        self.average_sentence_len = 0
        self.token_count_to_type_count = 0
        self.freq_1_count_to_type_count = 0
        self.word_naghshi_count = 0
        self.word_mohtavai_count = 0
        self.word_naghshi_count_to_type_count = 0
        self.word_mohtavai_count_to_type_count = 0
        self.word_naghshi_freq_1_count = 0
        self.word_naghshi_freq_1_count_to_type_count = 0
        self.word_bon_type_count = 0
        self.word_bon_token_count = 0
        self.average_syllable_in_text = 0
        self.average_syllable_in_text = 0
    
    def analyse(self):
        self.freq_analyse()
        self.freq_1_analyse()
        self.char_count_analyse()
        self.type_count_analyse()
        self.token_count_analyse()
        self.sentence_count_analyse()
        self.average_word_len_analyse()
        self.average_sentence_len_analyse()
        self.token_count_to_type_count_analyse()
        self.freq_1_count_to_type_count_analyse()
        for posType in ['naghshi', 'mohtavai']:
            self.word_pos_count_analyse(posType)
            self.word_pos_count_to_type_count_analyse(posType)
            self.word_pos_freq_1_count_analyse(posType)
            self.word_pos_freq_1_count_to_type_count_analyse(posType)
        self.word_bon_type_count_analyse()
        self.word_bon_token_count_analyse()
    
    

    def freq_analyse(self):
        freq_dict = {}
        for index, row in self.words.iterrows():
            if not math.isnan(row['SentIndex']):
                word = row['wordForm']
                if word in freq_dict:
                    freq_dict[word] = freq_dict[word]+1
                else:
                    freq_dict[word] = 1
        self.freq_dict = freq_dict

    def freq_1_analyse(self):
        self.freq_1_count = sum(value == 1 for value in self.freq_dict.values())
        
    def type_count_analyse(self):
        self.type_count = len(self.freq_dict)

    def token_count_analyse(self):
        self.token_count = sum(self.freq_dict.values())

    def char_count_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if not math.isnan(row['SentIndex']):
                result += row['WordCharacter']
        self.char_count = result

    def sentence_count_analyse(self):
        self.sentence_count = self.words['SentIndex'].max()

    def average_word_len_analyse(self):
        self.average_word_len = self.char_count / self.token_count

    def average_sentence_len_analyse(self):
        self.average_sentence_len = self.char_count / self.sentence_count

    def token_count_to_type_count_analyse(self):
        self.token_count_to_type_count = self.token_count / self.type_count

    def freq_1_count_to_type_count_analyse(self):
        self.freq_1_count_to_type_count = self.freq_1_count / self.type_count

        
    def word_pos_count_analyse(self, posType):
        count = 0
        for index, row in self.words.iterrows():
            if row['POS'] in posTypeDict[posType]:
                count += 1
        self.__dict__['word_'+posType+'_count'] = count

    def word_pos_count_to_type_count_analyse(self, posType):
        self.__dict__['word_'+posType+'_count_to_type_count'] = self.__dict__['word_'+posType+'_count'] / self.type_count
    
    def word_pos_freq_1_count_analyse(self, posType):
        count = 0
        for index, row in self.words.iterrows():
            if row['POS'] in posTypeDict[posType] and self.freq_dict[row['wordForm']] == 1:
                count += 1
        self.__dict__['word_' + posType+ '_freq_1_count'] = count
        
    def word_pos_freq_1_count_to_type_count_analyse(self, posType):
        self.__dict__['word_'+posType+'_freq_1_count_to_type_count'] = self.__dict__['word_'+posType+'_freq_1_count'] / self.type_count
    
    def word_bon_type_count_analyse(self):
        words = set()
        for index, row in self.words.iterrows():
            if row['POS'] in posTypeDict['bon']:
                words.add(row['wordForm'])
        self.word_bon_type_count = len(words)

    def word_bon_token_count_analyse(self):
        count = 0
        for index, row in self.words.iterrows():
            if row['POS'] in posTypeDict['bon']:
                print(row['POS'], posTypeDict['bon'])
                count += 1
        self.word_bon_token_count = count

    def __str__(self):
        summary = ''
        for index, row in self.words.iterrows():
            if math.isnan(row['SentIndex']):
                summary += '\n'
                continue
            summary += (row['wordForm']) + ' '
        summary += '\n'
        summary += 'freq_1_count: ' + str(self.freq_1_count) + '\n'
        summary += 'char_count: ' + str(self.char_count) + '\n'
        summary += 'token_count: ' + str(self.token_count) + '\n'
        summary += 'type_count: ' + str(self.type_count) + '\n'
        summary += 'sentence_count: ' + str(self.sentence_count) + '\n'
        summary += 'average_word_len: ' + str(self.average_word_len) + '\n'
        summary += 'average_sentence_len: ' + str(self.average_sentence_len) + '\n'
        summary += 'token_count_to_type_count: ' + str(self.token_count_to_type_count) + '\n'
        summary += 'freq_1_count_to_type_count: ' + str(self.freq_1_count_to_type_count) + '\n'
        summary += 'word_naghshi_count: ' + str(self.word_naghshi_count) + '\n'
        summary += 'word_mohtavai_count: ' + str(self.word_mohtavai_count) + '\n'
        summary += 'word_naghshi_count_to_type_count: ' + str(self.word_naghshi_count_to_type_count) + '\n'
        summary += 'word_mohtavai_count_to_type_count: ' + str(self.word_mohtavai_count_to_type_count) + '\n'
        summary += 'word_naghshi_freq_1_count: ' + str(self.word_naghshi_freq_1_count) + '\n'
        summary += 'word_mohtavai_freq_1_count: ' + str(self.word_mohtavai_freq_1_count) + '\n'
        summary += 'word_naghshi_freq_1_count_to_type_count: ' + str(self.word_naghshi_freq_1_count_to_type_count) + '\n'
        summary += 'word_mohtavai_freq_1_count_to_type_count: ' + str(self.word_mohtavai_freq_1_count_to_type_count) + '\n'
        summary += 'word_bon_type_count: ' + str(self.word_bon_type_count) + '\n'
        summary += 'word_bon_token_count: ' + str(self.word_bon_token_count) + '\n'
        return summary
        

words = pd.read_csv('./sampleInputToDB.csv')
a = Analyser(words)
a.analyse()
print(a)