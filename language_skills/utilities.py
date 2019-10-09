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
        # ت( شمارش تعداد واژههای با بسامد ١ در هر متن
        self.freq_1_count = 0
        # الف( شمارش تعداد حروف متن
        self.char_count = 0
        # ب( شمارش تعداد واژههای با تکرار )type( در هر متن
        self.type_count = 0
        # پ( شمارش تعداد واژههای بدون تکرار )token( در هر متن
        self.token_count = 0
        # ث( شمارش تعداد جملههای در هر متن
        self.sentence_count = 0
        # ج( محاسبه متوسط طول واژه در هر متن
        self.average_word_len = 0
        # چ( محاسبه متوسط طول جمله در هر متن
        self.average_sentence_len = 0
        # ح( محاسبه نسبت واژههای بدون تکرار به واژههای با تکرار در هر متن
        self.token_count_to_type_count = 0
        # خ( محاسبه نسبت واژههای با بسامد ١ به واژههای با تکرار در هر متن
        self.freq_1_count_to_type_count = 0
        # د( شمارش تعداد واژههای نقشی )مثل حرف اضافه و حرف ربط( در هر متن
        self.word_naghshi_count = 0
        # ذ( شمارش تعداد واژههای محتوایی )مثل اسم و صفت و قید و فعل( در هر متن
        self.word_mohtavai_count = 0
        # ر( محاسبه نسبت واژههای محتوایی به واژههای با تکرار در هر متن
        self.word_mohtavai_count_to_type_count = 0
        # ز( محاسبه نسبت واژههای نقشی به واژههای با تکرار در هر متن
        self.word_naghshi_count_to_type_count = 0
        self.word_naghshi_freq_1_count = 0
        # ژ( محاسبه نسبت واژههای نقشی با بسامد ١ به واژههای با تکرار در هر متن
        self.word_naghshi_freq_1_count_to_type_count = 0
        # س( محاسبه نسبت واژههای محتوایی با بسامد ١ به واژههای با تکرار در هر متن
        self.word_mohtavai_freq_1_count_to_type_count = 0
        self.word_bon_type_count = 0
        self.word_bon_token_count = 0
        # ف( محاسبه متوسط هجای واژهها در هر متن
        self.average_syllable_in_text = 0
        # ک( شمارش تعداد واژههای با تعداد هجای ١
        self.syllable_1_count = 0
        # گ( شمارش تعداد واژههای با تعداد هجای ٣ و بیشتر
        self.syllable_3_more_count = 0
        # ل( محاسبه نسبت تعداد واژههای با تعداد هجای ١ به تعداد واژههای با تکرار در هر متن
        self.syllable_1_count_to_type_count = 0
        # م( محاسبه نسبت تعداد واژههای با تعداد هجای ٣ و بیشتر به تعداد واژههای با تکرار در هر متن
        self.syllable_3_more_count_to_type_count = 0
        
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
        # self.word_bon_type_count_analyse()
        # self.word_bon_token_count_analyse()
        self.average_syllable_in_text_analyse()
        self.syllable_1_count_analyse()
        self.syllable_3_more_count_analyse()
        self.syllable_1_count_to_type_count_analyse()
        self.syllable_3_more_count_to_type_count_analyse()
    


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

    def average_syllable_in_text_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if not math.isnan(row['SentIndex']):
                result += row['SyllableNumber']
        self.average_syllable_in_text = result / self.token_count

    def syllable_1_count_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if row['SyllableNumber'] == 1:
                result += 1
        self.syllable_1_count = result


    def syllable_3_more_count_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if row['SyllableNumber'] >= 3:
                result += 1
        self.syllable_3_more_count = result

    def syllable_1_count_to_type_count_analyse(self):
        self.syllable_1_count_to_type_count = self.syllable_1_count / self.type_count
    
    def syllable_3_more_count_to_type_count_analyse(self):
        self.syllable_3_more_count_to_type_count = self.syllable_3_more_count / self.type_count


    def f1(self):
        return 206.835 - (1.015 * self.average_sentence_len) - (84.6 * self.average_syllable_in_text)

    def f2(self):
        return 3.6363 + (0.1579 * (self.syllable_3_more_count / self.token_count)) + (0.496 * self.average_sentence_len)
    
    def f3(self):
        return (4.71 * (self.char_count / self.type_count))

    def tojson(self):
        summary = {}
        
        fields = ['freq_1_count',
            'char_count',
            'token_count',
            'type_count',
            'sentence_count',
            'average_word_len',
            'average_sentence_len',
            'token_count_to_type_count',
            'freq_1_count_to_type_count',
            'word_naghshi_count',
            'word_mohtavai_count',
            'word_naghshi_count_to_type_count',
            'word_mohtavai_count_to_type_count',
            'word_naghshi_freq_1_count',
            'word_mohtavai_freq_1_count',
            'word_naghshi_freq_1_count_to_type_count',
            'word_mohtavai_freq_1_count_to_type_count',
            'word_bon_type_count',
            'word_bon_token_count',
            'average_syllable_in_text',
            'syllable_1_count',
            'syllable_3_more_count',
            'syllable_1_count_to_type_count',
            'syllable_3_more_count_to_type_count',
        ]

        for field in fields:
            summary[field] = str(self.__dict__[field])
            
        return summary

    def __str__(self):
        summary = ''
        for index, row in self.words.iterrows():
            if math.isnan(row['SentIndex']):
                summary += '\n'
                continue
            summary += (row['wordForm']) + ' '
        summary += '\n'
        
        fields = ['freq_1_count',
            'char_count',
            'token_count',
            'type_count',
            'sentence_count',
            'average_word_len',
            'average_sentence_len',
            'token_count_to_type_count',
            'freq_1_count_to_type_count',
            'word_naghshi_count',
            'word_mohtavai_count',
            'word_naghshi_count_to_type_count',
            'word_mohtavai_count_to_type_count',
            'word_naghshi_freq_1_count',
            'word_mohtavai_freq_1_count',
            'word_naghshi_freq_1_count_to_type_count',
            'word_mohtavai_freq_1_count_to_type_count',
            'word_bon_type_count',
            'word_bon_token_count',
            'average_syllable_in_text',
            'syllable_1_count',
            'syllable_3_more_count',
            'syllable_1_count_to_type_count',
            'syllable_3_more_count_to_type_count',
        ]

        for field in fields:
            summary += field + ': ' + str(self.__dict__[field]) + '\n'
            
        return summary
        

words = pd.read_csv('./sampleInputToDB.csv')
a = Analyser(words)
a.analyse()
print(a)
print(a.tojson())