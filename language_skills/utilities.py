import pdb
import pandas as pd
import math
import subprocess
import sys
import networkx as nx
from scipy import spatial
from language_skills.models import *

posTypeDict = {
    'naghshi': ['f'],
    'mohtavai': ['c'],
    'bon': ['Vpykshs----']
}

fields = ['freq_1_count',
        'char_count',
        'token_count',
        'type_count',
        'sentence_count',
        'average_word_len',
        'average_sentence_len',
        'type_count_to_token_count',
        'freq_1_count_to_token_count',
        'word_naghshi_count',
        'word_mohtavai_count',
        'word_naghshi_count_to_token_count',
        'word_mohtavai_count_to_token_count',
        'word_naghshi_freq_1_count',
        'word_mohtavai_freq_1_count',
        'word_naghshi_freq_1_count_to_token_count',
        'word_mohtavai_freq_1_count_to_token_count',
        'word_bon_type_count',
        'word_bon_type_count_to_type_count',
        'word_bon_type_count_to_token_count',
        'word_bon_freq_1',
        'word_bon_freq_1_to_token_count',
        'ravabet_dastori_dar_tajziye_vabastegi_type_count',
        'grehaye_sakhtari_dar_tajzie_sazei_token_count',
        'average_syllable_in_text',
        'syllable_1_count',
        'syllable_3_more_count',
        'syllable_1_count_to_token_count',
        'syllable_3_more_count_to_token_count',
        'f1',
        'f2',
        'f3',
        'syllable_2_count',
        'syllable_2_count_ratio_to_token_count',
        'cvcc_count',
        'cvc_count',
        'cv_count',
        'cvcc_to_count_all_syllable_ratio',
        'cvc_to_count_all_syllable_ratio',
        'cv_to_count_all_syllable_ratio',
        'count_all_syllable',
        'naghshi_to_mohtavai_ratio',
        'mohtavai_to_naghshi_ratio',
        'f4',
        'f5',
        'f6',
        'f7',
        'syllable_1_count_in_150_word',
        'syllable_3_above_in_100_word',
        'count_type_in_100_word',
        'bigram_freq_1_above',
        'bigram_freq_1',
        'bigram_freq_1_to_above_1_ratio',
        'trigram_freq_1_above',
        'trigram_freq_1',
        'trigram_freq_1_to_above_1_ratio',
        'pos_bigram_freq_1_above',
        'pos_bigram_freq_1',
        'pos_bigram_freq_1_to_above_1_ratio',
        'pos_trigram_freq_1_above',
        'pos_trigram_freq_1',
        'pos_trigram_freq_1_to_above_1_ratio',
        'name_entity_count',
        'name_entity_to_token_ratio',
        'count_clauses_dependency',
        'clause_dependency_total_dependency'
]

alpha = {'freq_1_count': 128, 'char_count': 2403, 'token_count': 776, 'type_count': 223, 'sentence_count': 90, 'average_word_len': 3.481012658227848, 'average_sentence_len': 10.846153846153847, 'type_count_to_token_count': 0.6111111111111112, 'freq_1_count_to_token_count': 0.765625, 'word_naghshi_count': 348, 'word_mohtavai_count': 428, 'word_naghshi_count_to_token_count': 1.5605381165919283, 'word_mohtavai_count_to_token_count': 1.9192825112107623, 'word_naghshi_freq_1_count': 9, 'word_mohtavai_freq_1_count': 124, 'word_naghshi_freq_1_count_to_token_count': 0.21212121212121213, 'word_mohtavai_freq_1_count_to_token_count': 0.71875, 'word_bon_type_count': 183, 'word_bon_token_count': 776, 'word_bon_type_count_to_type_count': 0.96875, 'word_bon_type_count_to_type_count': 3.4798206278026904, 'word_bon_freq_1_to_token_count': 94, 'ravabet_dastori_dar_tajziye_vabastegi_type_count': 33, 'grehaye_sakhtari_dar_tajzie_sazei_token_count': 1512, 'average_syllable_in_text': 1.8987341772151898, 'syllable_1_count': 425, 'syllable_3_more_count': 152, 'syllable_1_count_to_token_count': 1.905829596412556, 'syllable_3_more_count_to_token_count': 0.6816143497757847, 'f1': 56.13859908361974, 'f2': 9.060786633933443, 'f3': 30.5628350772297}

def save_text(text, fileName):
    f = open("../codes-data-folders/data/persian-archieve/new/fileName.txt","w+")
    f.write(text)
    f.close()


def run_perl():
    perl_script = subprocess.Popen(
        ["perl", "../codes-data-folders/0-persian-commands-pipeline.pl", "externalFile"],
        stdout=sys.stdout
    )
    perl_script.communicate()

class Analyser():
    def __init__(self, words):
        self.words = words
        self.freq_dict = 0
        self.freq_dict_bon = 0
        self.freq_dict_dep = 0
        self.freq_dict_pos = 0
        
        self.bigrams = {}
        self.pos_bigrams = {}
        self.trigrams = {}
        self.pos_trigrams = {}

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
        self.type_count_to_token_count = 0
        # خ( محاسبه نسبت واژههای با بسامد ١ به واژههای با تکرار در هر متن
        self.freq_1_count_to_token_count = 0
        # د( شمارش تعداد واژههای نقشی )مثل حرف اضافه و حرف ربط( در هر متن
        self.word_naghshi_count = 0
        # ذ( شمارش تعداد واژههای محتوایی )مثل اسم و صفت و قید و فعل( در هر متن
        self.word_mohtavai_count = 0
        # ر( محاسبه نسبت واژههای محتوایی به واژههای با تکرار در هر متن
        self.word_mohtavai_count_to_token_count = 0
        # ز( محاسبه نسبت واژههای نقشی به واژههای با تکرار در هر متن
        self.word_naghshi_count_to_token_count = 0
        self.word_naghshi_freq_1_count = 0
        # ژ( محاسبه نسبت واژههای نقشی با بسامد ١ به واژههای با تکرار در هر متن
        self.word_naghshi_freq_1_count_to_token_count = 0
        # س( محاسبه نسبت واژههای محتوایی با بسامد ١ به واژههای با تکرار در هر متن
        self.word_mohtavai_freq_1_count_to_token_count = 0
        self.word_bon_type_count = 0
        self.word_bon_token_count = 0
        self.word_bon_type_count_to_type_count = 0
        self.word_bon_type_count_to_token_count = 0
        self.word_bon_freq_1 = 0
        self.word_bon_freq_1_to_token_count = 0
        self.ravabet_dastori_dar_tajziye_vabastegi_type_count = 0
        self.grehaye_sakhtari_dar_tajzie_sazei_token_count = 0
        # ف( محاسبه متوسط هجای واژهها در هر متن
        self.average_syllable_in_text = 0
        # ک( شمارش تعداد واژههای با تعداد هجای ١
        self.syllable_1_count = 0
        # گ( شمارش تعداد واژههای با تعداد هجای ٣ و بیشتر
        self.syllable_3_more_count = 0
        # ل( محاسبه نسبت تعداد واژههای با تعداد هجای ١ به تعداد واژههای با تکرار در هر متن
        self.syllable_1_count_to_token_count = 0
        # م( محاسبه نسبت تعداد واژههای با تعداد هجای ٣ و بیشتر به تعداد واژههای با تکرار در هر متن
        self.syllable_3_more_count_to_token_count = 0
        self.f1 = 0
        self.f2 = 0
        self.f3 = 0

        self.syllable_2_count = 0   # 45
        self.syllable_2_count_ratio_to_token_count = 0 # 46
        self.cvcc_count = 0 # 47
        self.cvc_count = 0  # 48
        self.cv_count = 0  # 40
        self.cvcc_to_count_all_syllable_ratio = 0 # 50
        self.cvc_to_count_all_syllable_ratio = 0  # 51
        self.cv_to_count_all_syllable_ratio = 0  # 52
        self.count_all_syllable = 0 # 53
        self.naghshi_to_mohtavai_ratio = 0  # 54
        self.mohtavai_to_naghshi_ratio = 0  # 55
        self.f4 = 0 # 56
        self.f5 = 0 # 57
        self.f6 = 0 # 58
        self.f7 = 0 # 59
        self.syllable_1_count_in_150_word = 0 # 60
        self.syllable_3_above_in_100_word = 0 # 61
        self.count_type_in_100_word = 0  # 62
        self.bigram_freq_1_above = 0    # 63
        self.bigram_freq_1 = 0  # 64
        self.bigram_freq_1_to_above_1_ratio = 0 # 65
        self.trigram_freq_1_above = 0  # 66
        self.trigram_freq_1 = 0  # 67
        self.trigram_freq_1_to_above_1_ratio = 0  # 68
        self.pos_bigram_freq_1_above = 0 # 69
        self.pos_bigram_freq_1 = 0  # 70
        self.pos_bigram_freq_1_to_above_1_ratio = 0  # 71
        self.pos_trigram_freq_1_above = 0  # 72
        self.pos_trigram_freq_1 = 0  # 73
        self.pos_trigram_freq_1_to_above_1_ratio = 0  # 74
        self.name_entity_count = 0 # 75
        self.name_entity_to_token_ratio = 0 # 76
        self.count_clauses_dependency = 0 # 77
        self.clause_dependency_total_dependency = 0 #78

        
    def analyse(self):
        self.freq_analyse()
        self.freq_1_analyse()
        self.char_count_analyse()
        self.type_count_analyse()
        self.token_count_analyse()
        self.sentence_count_analyse()
        self.average_word_len_analyse()
        self.average_sentence_len_analyse()
        self.type_count_to_token_count_analyse()
        self.freq_1_count_to_token_count_analyse()
        for posType in ['naghshi', 'mohtavai']:
            self.word_pos_count_analyse(posType)
            self.word_pos_count_to_token_count_analyse(posType)
            self.word_pos_freq_1_count_analyse(posType)
            self.word_pos_freq_1_count_to_token_count_analyse(posType)
        self.word_bon_type_count_analyse()
        self.word_bon_token_count_analyse()
        self.word_bon_type_count_to_type_count_analyse()
        self.word_bon_type_count_to_token_count_analyse()
        self.word_bon_freq_1_analyse()
        self.word_bon_freq_1_to_token_count_analyse()
        self.grehaye_sakhtari_dar_tajzie_sazei_token_count_analyse()
        self.ravabet_dastori_dar_tajziye_vabastegi_type_count_analyse()
        self.average_syllable_in_text_analyse()
        self.syllable_1_count_analyse()
        self.syllable_3_more_count_analyse()
        self.syllable_1_count_to_token_count_analyse()
        self.syllable_3_more_count_to_token_count_analyse()
        self.f1_analyse()
        self.f2_analyse()
        self.f3_analyse()
        self.syllable_2_count_analyse()
        self.syllable_2_count_ratio_to_token_count_analyse()
        self.cvcc_count_analyse()
        self.cvc_count_analyse()
        self.cv_count_analyse()
        self.count_all_syllable_analyse()
        self.cvcc_to_count_all_syllable_ratio_analyse()
        self.cvc_to_count_all_syllable_ratio_analyse()
        self.cv_to_count_all_syllable_ratio_analyse()
        self.naghshi_to_mohtavai_ratio_analyse()
        self.mohtavai_to_naghshi_ratio_analyse()
        self.f4_analyse()
        self.f5_analyse()
        self.f6_analyse()
        self.f7_analyse()
        self.syllable_1_count_in_150_word_analyse()
        self.syllable_3_above_in_100_word_analyse()
        self.count_type_in_100_word_analyse()
        self.bigram_freq_1_analyse()
        self.bigram_freq_1_above_analyse()
        self.bigram_freq_1_to_above_1_ratio_analyse()
        self.trigram_freq_1_analyse()
        self.trigram_freq_1_above_analyse()
        self.trigram_freq_1_to_above_1_ratio_analyse()
        self.pos_bigram_freq_1_analyse()
        self.pos_bigram_freq_1_above_analyse()
        self.pos_bigram_freq_1_to_above_1_ratio_analyse()
        self.pos_trigram_freq_1_analyse()
        self.pos_trigram_freq_1_above_analyse()
        self.pos_trigram_freq_1_to_above_1_ratio_analyse()
        self.count_clauses_dependency_analyse()
        self.name_entity_count_analysis()
        self.name_entity_to_token_ratio_analyse()
        self.clause_dependency_total_dependency_analyse()
    def freq_analyse(self):
        freq_dict = {}
        freq_dict_bon = {}
        freq_dict_dep = {}
        freq_dict_pos = {}
        for index, row in self.words.iterrows():
            if not math.isnan(float(row['q'])):
                word = row['wordForm']
                if word in freq_dict:
                    freq_dict[word] = freq_dict[word]+1
                else:
                    freq_dict[word] = 1
                bon = row['Lemma']
                if bon in freq_dict_bon:
                    freq_dict_bon[bon] = freq_dict_bon[bon]+1
                else:
                    freq_dict_bon[bon] = 1
                dep = row['DepType']
                if dep in freq_dict_dep:
                    freq_dict_dep[dep] = freq_dict_dep[dep]+1
                else:
                    freq_dict_dep[dep] = 1
                pos = row['POS']
                if pos in freq_dict_pos:
                    freq_dict_pos[pos] = freq_dict_pos[pos]+1
                else:
                    freq_dict_pos[pos] = 1
        self.freq_dict = freq_dict
        self.freq_dict_bon = freq_dict_bon
        self.freq_dict_dep = freq_dict_dep
        self.freq_dict_pos = freq_dict_pos

    def freq_1_analyse(self):
        self.freq_1_count = sum(value == 1 for value in self.freq_dict.values())
        
    def type_count_analyse(self):
        self.type_count = len(self.freq_dict)

    def token_count_analyse(self):
        self.token_count = sum(self.freq_dict.values())

    def char_count_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if not math.isnan(float(row['q'])):
                result += row['WordCharacter'] if not math.isnan(row['WordCharacter']) else 0
        self.char_count = result

    def sentence_count_analyse(self):
        self.sentence_count = int(self.words['q'].map(lambda x: int(x)).max())

    def average_word_len_analyse(self):
        self.average_word_len = self.char_count / self.token_count if self.token_count != 0 else 0

    def average_sentence_len_analyse(self):
        self.average_sentence_len = self.token_count / int(self.sentence_count)

    def type_count_to_token_count_analyse(self):
        self.type_count_to_token_count = self.type_count / self.token_count

    def freq_1_count_to_token_count_analyse(self):
        self.freq_1_count_to_token_count = self.freq_1_count / self.token_count
   
    def word_pos_count_analyse(self, posType):
        count = 0
        for index, row in self.words.iterrows():
            try:
                if row['POS type (functional/content)'] in posTypeDict[posType]:
                    count += 1
            except:
                pass
        self.__dict__['word_'+posType+'_count'] = count

    def word_pos_count_to_token_count_analyse(self, posType):
        self.__dict__['word_'+posType+'_count_to_token_count'] = self.__dict__['word_'+posType+'_count'] / self.token_count
    
    def word_pos_freq_1_count_analyse(self, posType):
        count = 0
        for index, row in self.words.iterrows():
            if row['POS type (functional/content)'] in posTypeDict[posType] and self.freq_dict_pos[row['POS']] == 1:
                count += 1
        self.__dict__['word_' + posType+ '_freq_1_count'] = count
        
    def word_pos_freq_1_count_to_token_count_analyse(self, posType):
        self.__dict__['word_'+posType+'_freq_1_count_to_token_count'] = self.__dict__['word_'+posType+'_freq_1_count'] / self.token_count
    
    def word_bon_type_count_analyse(self):
        self.word_bon_type_count = len(self.freq_dict_bon)

    def word_bon_token_count_analyse(self):
        self.word_bon_token_count = sum(self.freq_dict.values())

    def word_bon_type_count_to_type_count_analyse(self):
        self.word_bon_type_count_to_type_count = self.word_bon_type_count / self.type_count

    def word_bon_type_count_to_token_count_analyse(self):
        self.word_bon_type_count_to_token_count = self.word_bon_type_count / self.token_count

    def word_bon_freq_1_analyse(self):
        self.word_bon_freq_1 = sum(value == 1 for value in self.freq_dict_bon.values())
    
    def word_bon_freq_1_to_token_count_analyse(self):
        self.word_bon_freq_1_to_token_count = self.word_bon_freq_1/self.token_count if self.token_count else 0

    def ravabet_dastori_dar_tajziye_vabastegi_type_count_analyse(self):
        self.ravabet_dastori_dar_tajziye_vabastegi_type_count = len(self.freq_dict_dep)

    def grehaye_sakhtari_dar_tajzie_sazei_token_count_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if not math.isnan(float(row['q'])):
                result += row['ConstituencyNumberOfNodes'] if not math.isnan(row['ConstituencyNumberOfNodes']) else 0
        self.grehaye_sakhtari_dar_tajzie_sazei_token_count = result

    def average_syllable_in_text_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if not math.isnan(float(row['q'])):
                try:
                    if isinstance(row['SyllableNumber'], str) and row['SyllableNumber'].isdigit():
                        result += int(row['SyllableNumber'])
                    elif not math.isnan(row['SyllableNumber']) :
                        result += row['SyllableNumber']
                except:
                    pass
        self.average_syllable_in_text = result / self.token_count

    def syllable_1_count_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if row['SyllableNumber'] in ['1',1]:
                result += 1
        self.syllable_1_count = result

    def syllable_3_more_count_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            try: #TODO: correct here
                if int(row['SyllableNumber']) >= 3:
                    result += 1
            except:
                pass
        self.syllable_3_more_count = result

    def syllable_1_count_to_token_count_analyse(self):
        self.syllable_1_count_to_token_count = self.syllable_1_count / self.token_count
    
    def syllable_3_more_count_to_token_count_analyse(self):
        self.syllable_3_more_count_to_token_count = self.syllable_3_more_count / self.token_count

    def f1_analyse(self):
        self.f1 = 206.835 - (1.015 * self.average_sentence_len) - (84.6 * self.average_syllable_in_text)

    def f2_analyse(self):
        self.f2 = 3.6363 + (0.1579 * (self.syllable_3_more_count)) + (0.496 * self.average_sentence_len)
    
    def f3_analyse(self):
        self.f3 = (4.71 * (self.char_count / int(self.token_count))) + (0.5 * (self.token_count / int(self.sentence_count))) - 21.43

    def tolist(self):
        summary = []

        list_fields = []
        for field in fields:
            category_id = '1'
            if Config.objects.filter(name='analysis_category_id', active=True).exists():
                category_id = Config.objects.filter(name='analysis_category_id', active=True).last()
                # f = {
                #     '1':[
                #         'average_sentence_len',
                #         'sentence_count',
                #     ],
                #     '2': [
                #         'average_syllable_in_text',
                #         'syllable_1_count',
                #         'syllable_3_more_count',
                #         'syllable_1_count_to_token_count',
                #         'syllable_3_more_count_to_token_count',
                #     ],
                #     '3':
                # }

        for field in list_fields:
            summary.append(self.__dict__[field])
            
        return summary

    def tojson(self):
        summary = {}

        for field in fields:
            summary[field] = str(self.__dict__[field])
            
        return summary

    def __str__(self):
        summary = ''
        for index, row in self.words.iterrows():
            if math.isnan(int(row['q'])):
                summary += '\n'
                continue
            summary += (row['wordForm']) + ' '
        summary += '\n'

        for field in fields:
            summary += field + ': ' + str(self.__dict__[field]) + '\n'
            
        return summary
    
    def get_difficulty_level(self):
        features = []
        for field in fields:
            features.append(min(self.__dict__[field] / alpha.get(field, 1), 1))
        print('injaaaaa', features)
        result = spatial.distance.cosine(features, [1]*len(features))
        if result > 0.7: return 'A'
        if result > 0.3: return 'B'
        return 'C'
    #   added features

    def get_phonem_pattern_count(self, pattern):
        count = 0
        for index, row in self.words.iterrows():
            try:
                count += int(row[pattern])
            except:
                pass
        return count

    def get_phonem_count_to_all_patern(self, pattern):
        count = 0
        all_count = 0
        for index, row in self.words.iterrows():
            try:
                try:
                    count += int(row[pattern])
                except:
                    pass
            except:
                pass
        return count/self.count_all_syllable if self.count_all_syllable else 0

    def syllable_2_count_analyse(self):
        count = 0
        for index, row in self.words.iterrows():
            if row['SyllableNumber'] in ['2',2]:
                count += 1
        self.syllable_2_count = count
    
    def syllable_2_count_ratio_to_token_count_analyse(self):
        self.syllable_2_count_ratio_to_token_count = self.syllable_2_count/ self.token_count if self.token_count else 0

    def count_all_syllable_analyse(self):
        count = 0
        for index, row in self.words.iterrows():
            try:
                count += int(row['SyllableNumber'])
            except:
                pass
        self.count_all_syllable = count

    def cv_count_analyse(self):
        self.cv_count =  self.get_phonem_pattern_count('CV Count')

    def cvc_count_analyse(self):
        self.cvc_count = self.get_phonem_pattern_count('CVC Count')

    def cvcc_count_analyse(self):
        self.cvcc_count = self.get_phonem_pattern_count('CVCC Count')

    def cv_to_count_all_syllable_ratio_analyse(self):
        self.cv_to_count_all_syllable_ratio = self.get_phonem_count_to_all_patern('CV Count')

    def cvc_to_count_all_syllable_ratio_analyse(self):
        self.cvc_to_count_all_syllable_ratio = self.get_phonem_count_to_all_patern('CVC Count')

    def cvcc_to_count_all_syllable_ratio_analyse(self):
        self.cvcc_to_count_all_syllable_ratio = self.get_phonem_count_to_all_patern('CVCC Count')

    def get_pos_type_count(self, posType):
        count = 0
        for index, row in self.words.iterrows():
            try:
                if row['POS type (functional/content)'] in posType:
                    count += 1
            except:
                pass
        return count

    def naghshi_to_mohtavai_ratio_analyse(self):
        mohtavai_count = self.get_pos_type_count(posTypeDict['mohtavai'])
        self.naghshi_to_mohtavai_ratio = self.get_pos_type_count(posTypeDict['naghshi'])/mohtavai_count if mohtavai_count else 0

    def mohtavai_to_naghshi_ratio_analyse(self):
        naghshi_count = self.get_pos_type_count(posTypeDict['naghshi'])
        self.mohtavai_to_naghshi_ratio = self.get_pos_type_count(posTypeDict['mohtavai'])/naghshi_count if naghshi_count else 0

    def syllable_1_count_in_150_word_analyse(self):
        count = 0
        for index, row in self.words.iterrows():
            if row['SyllableNumber'] in ['1',1]:
                count += 1
            if index >= 150:
                break
        self.syllable_1_count_in_150_word = count

    def syllable_3_above_in_100_word_analyse(self):
        count = 0
        for index, row in self.words.iterrows():
            try:
                if int(row['SyllableNumber']) >= 3:
                    count += 1
            except:
                pass
            if index >= 100:
                break
        self.syllable_3_above_in_100_word = count

    def count_type_in_100_word_analyse(self):
        words = []
        for index, row in self.words.iterrows():
            if index < 100:
                if not math.isnan(float(row['q'])):
                    words.append(row['wordForm'])
            else:
                break
        self.count_type_in_100_word = len(set(words))

    def bigram_freq_1_above_analyse(self):
        words = []
        for index, row in self.words.iterrows():
            if not math.isnan(float(row['q'])):
                words.append(row['wordForm'])

        self.bigram_freq_1_above = sum(value != 1 for value in self.bigrams.values())
        return self.bigram_freq_1_above

    def bigram_freq_1_analyse(self):
        words = []
        for index, row in self.words.iterrows():
            if not math.isnan(float(row['q'])):
                words.append(row['wordForm'])


        for i in range(0,len(words)-1):
            text = words[i] + ' ' + words[i+1]
            self.bigrams[text] = self.bigrams.get(text,0)+1

        self.bigram_freq_1 = sum(value == 1 for value in self.bigrams.values())
        return self.bigram_freq_1

    def bigram_freq_1_to_above_1_ratio_analyse(self):
        self.bigram_freq_1_to_above_1_ratio = self.bigram_freq_1 / (self.bigram_freq_1_above or 1)

    def trigram_freq_1_analyse(self):
        words = []
        for index, row in self.words.iterrows():
                if not math.isnan(float(row['q'])):
                    words.append(row['wordForm'])
        trigrams = {}

        for i in range(0, len(words) - 2):
            text = words[i] + ' ' + words[i + 1] + ' ' + words[i + 2]
            trigrams[text] = trigrams.get(text, 0) + 1

        self.trigrams = trigrams
        
        self.trigram_freq_1 = sum(value == 1 for value in self.trigrams.values())
        return self.trigram_freq_1

    def trigram_freq_1_above_analyse(self):

        self.trigram_freq_1_above = sum(value != 1 for value in self.trigrams.values())
        return self.trigram_freq_1_above

    def trigram_freq_1_to_above_1_ratio_analyse(self):
        self.trigram_freq_1_to_above_1_ratio = self.trigram_freq_1 / (self.trigram_freq_1_above or 1)

    def pos_bigram_freq_1_analyse(self):
        words = []
        for index, row in self.words.iterrows():
            if not str(row['POS']) == 'nan':
                words.append(row['POS'])
            
        pos_bigrams = {}

        for i in range(0, len(words) - 1):
            text = words[i] + ' ' + words[i + 1]
            pos_bigrams[text] = pos_bigrams.get(text, 0) + 1
        
        self.pos_bigrams = pos_bigrams
        
        self.pos_bigram_freq_1 = sum(value == 1 for value in self.pos_bigrams.values())
        return self.pos_bigram_freq_1

    def pos_bigram_freq_1_above_analyse(self):

        self.pos_bigram_freq_1_above = sum(value != 1 for value in self.pos_bigrams.values())
        return self.pos_bigram_freq_1_above


    def pos_bigram_freq_1_to_above_1_ratio_analyse(self):
        self.pos_bigram_freq_1_to_above_1_ratio = self.pos_bigram_freq_1_analyse()/(self.pos_bigram_freq_1_above_analyse() or 1)

    def pos_trigram_freq_1_analyse(self):
        words = []
        for index, row in self.words.iterrows():
            if not str(row['POS']) == 'nan':
                words.append(row['POS'])
        pos_trigrams = {}

        for i in range(0, len(words) - 2):
            text = words[i] + ' ' + words[i + 1] + ' ' + words[i + 2]
            pos_trigrams[text] = pos_trigrams.get(text, 0) + 1
        
        self.pos_trigrams = pos_trigrams

        self.pos_trigram_freq_1 = sum(value == 1 for value in self.pos_trigrams.values())
        return self.pos_trigram_freq_1

    def pos_trigram_freq_1_above_analyse(self):
        self.pos_trigram_freq_1_above = sum(value != 1 for value in self.pos_trigrams.values())
        return self.pos_trigram_freq_1_above

    def pos_trigram_freq_1_to_above_1_ratio_analyse(self):
        self.pos_trigram_freq_1_to_above_1_ratio = self.pos_trigram_freq_1 / (self.pos_trigram_freq_1_above or 1)

    def f4_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if index < 100:
                try:
                    if row['SyllableNumber'] >= 3:
                        result += 1
                except:
                    pass
            else:
                break
        y = result
        x = self.average_sentence_len
        self.f4 = 0.4 * (x + y)

    def f5_analyse(self):
        y = self.sentence_count
        x = self.syllable_3_more_count
        self.f5 = 3.1291 + 3 + math.sqrt(x * (30/y))

    def f6_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if index < 150:
                if row['SyllableNumber'] == 1:
                    result += 1
            else:
                break
        x = result
        self.f6 = 20 - (x / 10)

    def f7_analyse(self):
        x = self.average_sentence_len
        y = self.average_syllable_in_text
        self.f7 = (0.39 * x) + (11.8 * y) - 15.59



    def get_vacancy_questions(self):
        result = []
        for i in range(1, int(self.sentence_count) + 1):
            sentence_words = self.words[self.words.q == i]
            
            sentence_analyser = Analyser(sentence_words)
            sentence_analyser.analyse()

            G = nx.DiGraph()
            for index, row in sentence_words.iterrows():
                if not math.isnan(int(row['q'])):
                    if not math.isnan(row['DepRelation']) and int(row['DepRelation']) != 0:
                        G.add_edge(int(row['WordIndex']), int(row['DepRelation']))
            pr = nx.pagerank(G, alpha=0.9)
            # import pdb;pdb.set_trace()
            if len(pr) != 0:
                keyword_index = max(pr.keys(), key = lambda x: pr[x])
                
                processed_words = []
                for index, row in sentence_words.iterrows():
                    if not math.isnan(int(row['q'])):
                        processed_words.append({'word': row['wordForm'], 'is_vacancy': row['WordIndex']
                                                == keyword_index, 'DepType': row['DepType'], 'POSType': row['POS']})
                
                result.append({'level': sentence_analyser.get_difficulty_level(), 'words': processed_words})
        return result

    def name_entity_count_analysis(self):
        result = 0
        for index, row in self.words.iterrows():
            try:
                if row['POS'] and row['POS'].startswith('N') and (row['POS'][5] == '-'):
                    result += 1
            except:
                pass

        self.name_entity_count = result

    def name_entity_to_token_ratio_analyse(self):
        self.name_entity_to_token_ratio = self.name_entity_count/self.token_count

    def count_clause_dependency_tree_analyse(self):
        result = 0
        count = self.type_count
        for index, row in self.words.iterrows():
            count += 1
            try:
                if not row['POS'][5] == '-':
                    result += 1
            except:
                pass

        self.name_entity_to_token_ratio = result / count

    def count_clauses_dependency_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if str(row['DepType']) in ['MARK', 'PURPCL', 'COMP', 'RCMOD', 'AUX', 'COMPM']:
                result += 1

        self.count_clauses_dependency = result

    def clause_dependency_total_dependency_analyse(self):
        result = 0
        for index, row in self.words.iterrows():
            if not str(row['DepType']) == 'PUNC':
                result += 1

        self.clause_dependency_total_dependency = self.count_clauses_dependency/result

# words = pd.read_csv('./sampleInputToDB-new.csv')
# import re
# words = pd.read_csv('./levelC-zabane-farsi-saffarMoqaddam-9.csv')
# for i, row in words.iterrows():
#     if 'not found' in str(row['q']):
#         print(i)
#         words.loc[i, 'WordIndex'] = last_index+1
#         words.loc[i, 'q'] = last_q
#         words.loc[i, 'wordForm'] = re.search(
#             'not found\*\*\*(.*)\*\*\*', row['q']).group(1)
#         last_index = last_index+1
#     else:
#         last_index = row['WordIndex']+1
#         last_q = row['q']
# # df.sport = df.sport.apply(lambda x: 'ball sport' if 'ball' in x else x)
# a = Analyser(words)
# a.analyse()
# result = a.get_vacancy_questions()
# # import pdb;pdb.set_trace()
# whole_text = ''
# res = ''
# sentences = []
# index = 0
# for sentence in result:
#     origin = ' '.join([word['word'] for word in sentence['words']])
#     res += origin 
#     vacancy_arr = []
#     answer = ''
#     answer_type = ''
#     for word in sentence['words']:
#         if not word['is_vacancy']:
#             vacancy_arr.append(word['word'])
#         else:
#             vacancy_arr.append('/&&__question__&&/')
#             answer = word['word']
#             if word['POSType'] and word['POSType'].startswith('V'):
#                 answer_type = 'verb'
#             if word['POSType'] and (word['POSType'].startswith('J') or word['POSType'].startswith('E')):
#                 answer_type = 'preposition'
#     vacancy_text = ' '.join(vacancy_arr)
#     origin = origin.replace('-', '‌')
#     vacancy_text = vacancy_text.replace('-', '‌')
#     answer = answer.replace('-', '‌')
#     sentences.append({
#         'index': index,
#         'origin': origin,
#         'vacancy': vacancy_text,
#         'answer': answer,
#         'answer_type': answer_type,
#         'level': sentence['level'],
#     })
#     index += 1

# for index, sentence in enumerate(sentences):
#     whole_vacancy = ''
#     for tmp_sen in sentences:
#         if tmp_sen['index'] == index:
#             whole_vacancy += tmp_sen['vacancy']
#         else:
#             whole_vacancy += tmp_sen['origin']
#     res = res.replace('-', '‌')
#     whole_vacancy = whole_vacancy.replace('-', '‌')
#     sentence['origin-text'] = res
#     sentence['whole_vacancy'] = whole_vacancy

# # import pdb;pdb.set_trace()
# text = Text.objects.create(
#     text=res,
#     level=''
# )
# for q in sentences:
#     # import pdb;pdb.set_trace()
#     if q['answer_type'] in ['verb', 'preposition']:
#         is_verb = q['answer_type'] == 'verb'
#         is_preposition = q['answer_type'] == 'preposition'
#         VacancyQuestion.objects.create(
#             text=q['vacancy'],
#             whole_text=q['whole_vacancy'],
#             origin_text=text,
#             level=q['level'],
#             answer=q['answer'],
#             is_verb=is_verb,
#             is_preposition=is_preposition,
#         )

# import pdb;pdb.set_trace()
# print(*result, sep='\n\n')
# print(a)
# print(a.tojson())
# print(res)

# run_perl()

# m = {}
# for field in fields:
#     m[field] = 0

# for i in range(1, 7):
#     words = pd.read_csv('./csvToDB/levelA-amuzeshe-zabane-farsi-samare-1.csv')
#     a = Analyser(words)
#     a.analyse()
#     print(a.tojson(), '\n\n\n')
#     for field in fields:
#         m[field] = a.__dict__[field]

# print(m)
