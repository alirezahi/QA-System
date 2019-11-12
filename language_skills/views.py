from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
from .models import *
from django.views import View
from django.shortcuts import redirect
from .utilities import Analyser
from django.http import HttpResponse
import os



# SET_COUNT = int(Config.objects.filter(name='question_set_count', active=True).last().value) or 30
SET_COUNT = 30
# SHOW_WHOLE_TEXT = int(Config.objects.filter(name='show_whole_text', active=True).last().value) or 'false'
SHOW_WHOLE_TEXT = 'false'


class StaffRequiredMixin(object):
    """
    View mixin which requires that the authenticated user is a staff member
    (i.e. `is_staff` is True).
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request,
                'You do not have the permission required to perform the '
                'requested operation.')
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request,
                                                        *args, **kwargs)

# Create your views here.

class VacancyQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/v-question.html'
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        if self.request.method == 'GET':
            data = self.request.GET
            answer = data.get('answer','')
        context = super().get_context_data(**kwargs)
        question_set = VacancyQuestionSet.objects.get(id=set_id)
        if answer:
            last_question = question_set.questions.filter(order__lt=order).order_by('order').last()
            last_question.answer = answer
            last_question.save()
        if not self.kwargs.get('last',None):
            question_select = question_set.questions.filter(
                order=order).last()
            context['question'] = question_select.question
            context['order'] = order
            context['next'] = '/question/v/' + str(set_id)+'/'+str(question_select.order+1)+''
        return context
    
    def dispatch(self, request, *args, **kwargs):
        kwargs['last'] = True
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        question_set = VacancyQuestionSet.objects.get(id=set_id)
        question_select = question_set.questions.filter(
            order=order).last()
        last_question = question_set.questions.order_by('order').last()
        if not last_question:
            return redirect('/')
        if last_question.order < int(order):
            self.kwargs['last'] = True
            self.get_context_data(**kwargs)
            return redirect('/question/v/check-answers/'+str(set_id)+'')
        return super(VacancyQuestionTemplate, self).dispatch(request, *args, **kwargs)


class VQuestionNewTemplate(LoginRequiredMixin, RedirectView):
    template_name = 'question/v-question.html'
    login_url = '/login/'
    
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        super().get_redirect_url(*args, **kwargs)
        question_set = generate_vquestion_set(self.request.user)
        return '/question/v/'+str(question_set.id)+'/1'


class HistoryChoiceTemplate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/history-choice.html'


class NewQuestionTemplate(StaffRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/new.html'


class VQuestionHistoryListTemplate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/vc-history-list.html'


class VQuestionListTemplate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/vc-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = VacancyQuestion.objects.all()
        return context


def generate_vquestion_set(user):
    v_list = VacancyQuestion.objects.get_random(SET_COUNT)
    v_set = VacancyQuestionSet.objects.create(user=user.qauser)
    order_counter = 1
    for v in v_list:
        v_obj = SelectedVacancyQuestion.objects.create(question=v, order=order_counter)
        v_set.questions.add(v_obj)
        order_counter += 1
    return v_set


def check_answer(request, question_id):
    if request.method == 'GET':
        data = request.GET
        if question_id and VacancyQuestionSet.objects.filter(id=question_id).exists():
            v_set = VacancyQuestionSet.objects.get(id=question_id)
            questions = v_set.questions.all().order_by('order')
            answers_count = questions.count()
            my_data = []
            true_count = 0
            user_answers = []
            answers = []
            for q in questions:
                answer = q.answer
                order = q.order
                user_answers.append(
                    {'order': int(order), 'text': answer})
                if(answer == q.question.answer):
                    true_count += 1
            v_set.right_answers = true_count
            v_set.question_count = answers_count
            v_set.answer_percentage = true_count/answers_count if answers_count else 0
            v_set.save()
            return render(request, template_name='question/v-question.html', context={'questions': questions, 'user_answers': user_answers, 'answer_page': True, 'state':v_set})
    return redirect('/accounts/dashboard/')



# ===========================


class MCQuestionNewTemplate(LoginRequiredMixin, RedirectView):
    template_name = 'question/mc-question.html'
    login_url = '/login/'
    
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        super().get_redirect_url(*args, **kwargs)
        question_set = generate_mcquestion_set(self.request.user)
        return '/question/mc/'+str(question_set.id)+'/1'


class MCQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/mc-question.html'
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        if self.request.method == 'GET':
            data = self.request.GET
            answer = data.get('answer','')
        context = super().get_context_data(**kwargs)
        question_set = MCQuestionSet.objects.get(id=set_id)
        if answer:
            last_question = question_set.questions.filter(order__lt=order).order_by('order').last()
            last_question.answer = answer
            last_question.save()
        if not self.kwargs.get('last',None):
            question_select = question_set.questions.filter(
                order=order).last()
            context['question'] = question_select.question
            context['order'] = order
            context['next'] = '/question/mc/' + str(set_id)+'/'+str(question_select.order+1)+''
        return context
    
    def dispatch(self, request, *args, **kwargs):
        kwargs['last'] = True
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        question_set = MCQuestionSet.objects.get(id=set_id)
        question_select = question_set.questions.filter(
            order=order).last()
        last_question = question_set.questions.order_by('order').last()
        if not last_question:
            return redirect('/')
        if last_question.order < int(order):
            self.kwargs['last'] = True
            self.get_context_data(**kwargs)
            return redirect('/question/mc/check-answers/'+str(set_id)+'')
        return super(MCQuestionTemplate, self).dispatch(request, *args, **kwargs)


def generate_mcquestion_set(user):
    mc_list = MultipleChoiceQuestion.objects.get_random(SET_COUNT)
    mc_set = MCQuestionSet.objects.create(user=user.qauser)
    order_counter = 1
    for mc in mc_list:
        mc_obj = SelectedMCQuestion.objects.create(question=mc, order=order_counter)
        mc_set.questions.add(mc_obj)
        order_counter += 1
    return mc_set



class MCQuestionHistoryListTemplate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/mc-history-list.html'


class MCQuestionHistoryListTemplate1(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/mcc-question.html'


class MCQuestionListTemplate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/mc-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = MultipleChoiceQuestion.objects.all()
        return context


class CreateQuestions(View):
    def get(self, request):
        files = os.listdir('./data')
        csv_files = []
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(file)

        for file in csv_files:
            import re
            last_index = 0
            last_q = 0
            words = pd.read_csv('./data/'+file)
            for i, row in words.iterrows():
                if 'not found' in str(row['q']):
                    print(i)
                    words.loc[i, 'WordIndex'] = '0' if i!= 0 else last_index
                    words.loc[i, 'q'] = last_q
                    words.loc[i, 'wordForm'] = re.search(
                        'not found\*\*\*(.*)\*\*\*', row['q']).group(1)
                    last_index = last_index+1
                else:
                    last_index = row['WordIndex']+1
                    last_q = row['q']
            a = Analyser(words)
            a.analyse()
            result = a.get_vacancy_questions()
            whole_text = ''
            res = ''
            sentences = []
            index = 0
            for sentence in result:
                origin = ' '.join([word['word'] for word in sentence['words']])
                res += origin
                vacancy_arr = []
                answer = ''
                answer_type = ''
                for word in sentence['words']:
                    if not word['is_vacancy']:
                        vacancy_arr.append(word['word'])
                    else:
                        vacancy_arr.append('/&&__question__&&/')
                        answer = word['word']
                        if word['POSType'] and word['POSType'].startswith('V'):
                            answer_type = 'verb'
                        if word['POSType'] and (word['POSType'].startswith('J') or word['POSType'].startswith('E')):
                            answer_type = 'preposition'
                vacancy_text = ' '.join(vacancy_arr)
                origin = origin.replace('-', '‌')
                vacancy_text = vacancy_text.replace('-', '‌')
                answer = answer.replace('-', '‌')
                sentences.append({
                    'index': index,
                    'origin': origin,
                    'vacancy': vacancy_text,
                    'answer': answer,
                    'answer_type': answer_type,
                    'level': sentence['level'],
                })
                index += 1

            for index, sentence in enumerate(sentences):
                whole_vacancy = ''
                for tmp_sen in sentences:
                    if tmp_sen['index'] == index:
                        whole_vacancy += tmp_sen['vacancy']
                    else:
                        whole_vacancy += tmp_sen['origin']
                res = res.replace('-', '‌')
                whole_vacancy = whole_vacancy.replace('-', '‌')
                sentence['origin-text'] = res
                sentence['whole_vacancy'] = whole_vacancy

            text = Text.objects.create(
                text=res,
                level=''
            )
            for q in sentences:
                # import pdb;pdb.set_trace()
                if q['answer_type'] in ['verb', 'preposition']:
                    is_verb = q['answer_type'] == 'verb'
                    is_preposition = q['answer_type'] == 'preposition'
                    VacancyQuestion.objects.create(
                        text=q['vacancy'],
                        whole_text=q['whole_vacancy'],
                        origin_text=text,
                        level=q['level'],
                        answer=q['answer'],
                        is_verb=is_verb,
                        is_preposition=is_preposition,
                    )
        return HttpResponse('Done')

def check_answer_mc(request, question_id):
    if request.method == 'GET':
        data = request.GET
        if question_id and MCQuestionSet.objects.filter(id=question_id).exists():
            mc_set = MCQuestionSet.objects.get(id=question_id)
            questions = mc_set.questions.all().order_by('order')
            answers_count = questions.count()
            my_data = []
            true_count = 0
            user_answers = []
            answers = []
            for q in questions:
                answer = q.answer
                order = q.order
                user_answers.append(
                    {'order': int(order), 'text': answer})
                if(answer == q.question.answer):
                    true_count += 1
            mc_set.right_answers = true_count
            mc_set.question_count = answers_count
            mc_set.answer_percentage = true_count/answers_count if answers_count else 0
            mc_set.save()
            return render(request, template_name='question/mc-question.html', context={'questions': questions, 'user_answers': user_answers, 'answer_page': True, 'state':mc_set})
        # data = request.GET
        # if question_id and MultipleChoiceQuestion.objects.filter(id=question_id).exists():
        #     question = MultipleChoiceQuestion.objects.get(id=question_id)
        #     answers = question.answers.all().order_by('order')
        #     answers_count = len(answers)
        #     my_data = []
        #     true_count = 0
        #     user_answers = []
        #     for q, v in data.items():
        #         if q.isdigit():
        #             answer = answers.get(order=int(q))
        #             user_answers.append({'order':int(q), 'text': v})
        #             if(answer.text == v):
        #                 true_count += 1
        #     mch = MCQuestionHistory(question=question, right_answers=true_count, answers_count=answers_count,answer_percentage = true_count/answers_count)
        #     mch.save()
        #     user = request.user.qauser
        #     user.mc_questions.add(mch)
        #     return render(request, template_name='question/mc-question.html', context={'question': question,'answers': answers, 'user_answers': user_answers, 'answer_page': True})
    return redirect('/accounts/dashboard/')
