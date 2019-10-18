from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

# Create your views here.

class VacancyQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/v-question.html'
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        question_id = self.kwargs['question_id']
        context = super().get_context_data(**kwargs)
        context['question'] = VacancyQuestion.objects.filter(id=question_id).last()
        return context


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


def check_answer(request, question_id):
    if request.method == 'POST':
        data = request.POST
        if question_id and VacancyQuestion.objects.filter(id=question_id).exists():
            question = VacancyQuestion.objects.get(id=question_id)
            answers = question.answers.all().order_by('order')
            answers_count = len(answers)
            my_data = []
            true_count = 0
            user_answers = []
            for q, v in data.items():
                if q.isdigit():
                    answer = answers.get(order=int(q))
                    user_answers.append({'order':int(q), 'text': v})
                    if(answer.text == v):
                        true_count += 1
            # vch = VQuestionHistory.objects.filter(question=question, right_answers=true_count, answers_count=answers_count,answer_percentage = true_count/answers_count).last()
            vch = VQuestionHistory(question=question, right_answers=true_count, answers_count=answers_count,answer_percentage = true_count/answers_count)
            vch.save()
            user = request.user.qauser
            user.v_questions.add(vch)
            return render(request, template_name='question/v-question.html', context={'question': question,'answers': answers, 'user_answers': user_answers, 'answer_page': True})
    return redirect('/accounts/dashboard/')





# ===========================

class MCQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/mc-question.html'
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        question_id = self.kwargs['question_id']
        context = super().get_context_data(**kwargs)
        context['question'] = MultipleChoiceQuestion.objects.filter(id=question_id).last()
        return context


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


def check_answer_mc(request, question_id):
    if request.method == 'POST':
        data = request.POST
        if question_id and MultipleChoiceQuestion.objects.filter(id=question_id).exists():
            question = MultipleChoiceQuestion.objects.get(id=question_id)
            answers = question.answers.all().order_by('order')
            answers_count = len(answers)
            my_data = []
            true_count = 0
            user_answers = []
            for q, v in data.items():
                if q.isdigit():
                    answer = answers.get(order=int(q))
                    user_answers.append({'order':int(q), 'text': v})
                    if(answer.text == v):
                        true_count += 1
            mch = MCQuestionHistory(question=question, right_answers=true_count, answers_count=answers_count,answer_percentage = true_count/answers_count)
            mch.save()
            user = request.user.qauser
            user.mc_questions.add(mch)
            return render(request, template_name='question/mc-question.html', context={'question': question,'answers': answers, 'user_answers': user_answers, 'answer_page': True})
    return redirect('/accounts/dashboard/')
