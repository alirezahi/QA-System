from django.shortcuts import render
from language_skills.models import *

# Create your views here.
def add_preposition(request):
    f = open('../static/file/prep.txt')
    for line in f:
        if line != '':
            PrePosition.objects.get_or_create(text=line.strip('\n'))

def add_verb(request):
    import pandas as pd
    df = pd.read_csv('../static/file/verbs.csv')
    for i in df.head(541).iterrows():
        verb = VerbInfo.objects.create(
            infinitive=i[0], past_root=i[1][df.columns.get_loc('بن ماضی')-1], passive=i[1][df.columns.get_loc('اسم مفعول')-1])
        for form in ['گذشته ساده ۱ مفرد', 'گذشته ساده ۲ مفرد', 'گذشته ساده ۳ مفرد', 'گذشته ساده ۱ جمع ', 'گذشته ساده ۲ جمع ', 'گذشته ساده ۳ جمع ', 'ماضی استمراری ۱ مفرد', 'ماضی استمراری ۲ مفرد', 'ماضی استمراری ۳ مفرد', 'ماضی استمراری ۱ جمع', 'ماضی استمراری ۲ جمع', 'ماضی استمراری ۳ جمع', 'حال کامل ۱ مفرد ', 'حال کامل ۲ مفرد ', 'حال کامل ۳ مفرد ', 'حال کامل ۱ جمع ', 'حال کامل ۲ جمع ', 'حال کامل ۳ جمع ', 'گذشته استمراری التزامی ۱ مفرد', 'گذشته استمراری التزامی ۲ مفرد', 'گذشته استمراری التزامی ۳ مفرد', 'گذشته استمراری التزامی ۱ جمع', 'گذشته استمراری التزامی ۲ جمع', 'گذشته استمراری التزامی ۳ جمع', 'بن مضارع', 'مضارع ساده ۱ مفرد', 'مضارع ساده ۲ مفرد', 'مضارع ساده ۳ مفرد', 'مضارع ساده ۱ جمع', 'مضارع ساده ۲ جمع', 'مضارع ساده ۳ جمع', 'مضارع اخباری ۱مفرد', 'مضارع اخباری ۲مفرد', 'مضارع اخباری ۳مفرد', 'مضارع اخباری ۱ جمع', 'مضارع اخباری ۲ جمع', 'مضارع اخباری ۳ جمع', 'مضارع التزامی ۱ مفرد', 'مضارع التزامی ۲ مفرد', 'مضارع التزامی ۳ مفرد', 'مضارع التزامی ۱ جمع', 'مضارع التزامی ۲ جمع', 'مضارع التزامی ۳ جمع', 'حال استمراری التزامی ۱ مفرد ', 'حال استمراری التزامی ۲ مفرد ', 'حال استمراری التزامی ۳ مفرد ', 'حال استمراری التزامی ۱ جمع ', 'حال استمراری التزامی ۲ جمع ', 'حال استمراری التزامی ۳ جمع ', 'ماضی نقلی ۱ مفرد', 'ماضی نقلی ۲ مفرد', 'ماضی نقلی ۳ مفرد', 'ماضی نقلی ۱ جمع', 'ماضی نقلی ۲ جمع', 'ماضی نقلی 3 جمع\u200cاند', 'ماضی بعید ۱ مفرد', 'ماضی بعید ۲ مفرد', 'ماضی بعید ۳ مفرد', 'ماضی بعید ۱ جمع', 'ماضی بعید ۲ جمع', 'ماضی بعید ۳ جمع\u200cبودند', 'ماضی نقلی استمراری ۱ مفرد', 'ماضی نقلی استمراری ۲ مفرد', 'ماضی نقلی استمراری ۳ مفرد', 'ماضی نقلی استمراری ۱ جمع', 'ماضی نقلی استمراری ۲ جمع', 'ماضی نقلی استمراری ۳ جمع', 'امری', 'ماضی ساده مجمول ۱ مفرد', 'ماضی ساده مجمول ۲ مفرد', 'ماضی ساده مجمول ۳ مفرد', 'ماضی ساده مجمول ۱ جمع', 'ماضی ساده مجمول ۲ جمع', 'ماضی ساده مجمول ۳ جمع', 'ماضی استمراری مجمول ۱ مفرد', 'ماضی استمراری مجمول ۲ مفرد', 'ماضی استمراری مجمول ۳ مفرد', 'ماضی استمراری مجمول ۱ جمع', 'ماضی استمراری مجمول ۲ جمع', 'ماضی استمراری مجمول ۳ جمع']:
            id_num = df.columns.get_loc(form)
            freq = i[1][id_num]
            VerbForm.objects.create(
                tense=form, form=i[1][df.columns.get_loc(form)-1], verb=verb, freq=freq)
