from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F, Count, Case, When
import pandas as pd
from .models import *
from django.views import View
from django.shortcuts import redirect
from .utilities import Analyser
from django.http import HttpResponse, FileResponse
from threading import Thread
from scipy import spatial
from sklearn.model_selection import KFold
from sklearn.svm import SVC
import numpy as np
import os
import math

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

class BlankQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/v-question.html'
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        SHOW_WHOLE_TEXT = Config.objects.filter(name='show_whole_text', active=True).last(
            ).value if Config.objects.filter(name='show_whole_text', active=True) else 'false'
        ANSWER_REQUIRED = Config.objects.filter(name='answer_required', active=True).last(
            ).value if Config.objects.filter(name='answer_required', active=True) else 'false'
        TIMER_LIMIT = int(Config.objects.filter(name='timer_limit', active=True).last(
            ).value) if Config.objects.filter(name='timer_limit', active=True) else 60
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        if self.request.method == 'GET':
            data = self.request.GET
            answer = data.get('answer','')
        context = super().get_context_data(**kwargs)
        context['whole_text'] = True if SHOW_WHOLE_TEXT == 'true' else False
        context['answer_required'] = True if ANSWER_REQUIRED == 'true' else False
        context['timer_limit'] = TIMER_LIMIT
        question_set = BlankQuestionSet.objects.get(id=set_id)
        index = question_set.questions.filter(order__lt=order).count()
        context['question_progress'] = int((index+1) / question_set.questions.count() * 100)
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
        question_set = BlankQuestionSet.objects.get(id=set_id)
        question_select = question_set.questions.filter(
            order=order).last()
        last_question = question_set.questions.order_by('order').last()
        if not last_question:
            return redirect('/')
        if last_question.order < int(order):
            self.kwargs['last'] = True
            self.get_context_data(**kwargs)
            level_blank, is_verb_blank, is_prep_blank = calc_total_level_blank(
                request.user)
            p1 = Thread(target=update_blank_userquestion_relation, args=(
                request.user, level_blank, is_verb_blank, is_prep_blank,))
            p1.start()
            return redirect('/question/v/check-answers/'+str(set_id)+'')
        return super(BlankQuestionTemplate, self).dispatch(request, *args, **kwargs)


class OfferBlankQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/offer-v-question.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        SHOW_WHOLE_TEXT = Config.objects.filter(name='show_whole_text', active=True).last(
        ).value if Config.objects.filter(name='show_whole_text', active=True) else 'false'
        ANSWER_REQUIRED = Config.objects.filter(name='answer_required', active=True).last(
        ).value if Config.objects.filter(name='answer_required', active=True) else 'false'
        TIMER_LIMIT = int(Config.objects.filter(name='timer_limit', active=True).last(
            ).value) if Config.objects.filter(name='timer_limit', active=True) else 60
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        if self.request.method == 'GET':
            data = self.request.GET
            answer = data.get('answer', '')
        context = super().get_context_data(**kwargs)
        context['whole_text'] = True if SHOW_WHOLE_TEXT == 'true' else False
        context['answer_required'] = True if ANSWER_REQUIRED == 'true' else False
        context['timer_limit'] = TIMER_LIMIT
        question_set = BlankQuestionSet.objects.get(id=set_id)
        index = question_set.questions.filter(order__lt=order).count()
        context['question_progress'] = int((index+1) / question_set.questions.count() * 100)
        if answer:
            last_question = question_set.questions.filter(
                order__lt=order).order_by('order').last()
            last_question.answer = answer
            last_question.save()
        if not self.kwargs.get('last', None):
            question_select = question_set.questions.filter(
                order=order).last()
            context['question'] = question_select.question
            context['order'] = order
            context['next'] = '/question/v/offer/' + \
                str(set_id)+'/'+str(question_select.order+1)+''
        return context

    def dispatch(self, request, *args, **kwargs):
        kwargs['last'] = True
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        question_set = BlankQuestionSet.objects.get(id=set_id)
        question_select = question_set.questions.filter(
            order=order).last()
        last_question = question_set.questions.order_by('order').last()
        if not last_question:
            return redirect('/')
        if last_question.order < int(order):
            self.kwargs['last'] = True
            self.get_context_data(**kwargs)
            level_blank, is_verb_blank, is_prep_blank = calc_total_level_blank(
                request.user)
            p1 = Thread(target=update_blank_userquestion_relation, args=(
                request.user, level_blank, is_verb_blank, is_prep_blank,))
            p1.start()
            return redirect('/question/v/check-answers/'+str(set_id)+'')
        return super(OfferBlankQuestionTemplate, self).dispatch(request, *args, **kwargs)


class CommonBlankQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/offer-v-question.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        SHOW_WHOLE_TEXT = Config.objects.filter(name='show_whole_text', active=True).last(
        ).value if Config.objects.filter(name='show_whole_text', active=True) else 'false'
        ANSWER_REQUIRED = Config.objects.filter(name='answer_required', active=True).last(
        ).value if Config.objects.filter(name='answer_required', active=True) else 'false'
        TIMER_LIMIT = int(Config.objects.filter(name='timer_limit', active=True).last(
            ).value) if Config.objects.filter(name='timer_limit', active=True) else 60
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        if self.request.method == 'GET':
            data = self.request.GET
            answer = data.get('answer', '')
        context = super().get_context_data(**kwargs)
        context['whole_text'] = True if SHOW_WHOLE_TEXT == 'true' else False
        context['answer_required'] = True if ANSWER_REQUIRED == 'true' else False
        context['timer_limit'] = TIMER_LIMIT
        question_set = BlankQuestionSet.objects.get(id=set_id)
        index = question_set.questions.filter(order__lt=order).count()
        context['question_progress'] = int((index+1) / question_set.questions.count() * 100)
        if answer:
            last_question = question_set.questions.filter(
                order__lt=order).order_by('order').last()
            last_question.answer = answer
            last_question.save()
        if not self.kwargs.get('last', None):
            question_select = question_set.questions.filter(
                order=order).last()
            context['question'] = question_select.question
            context['order'] = order
            context['next'] = '/question/v/common/' + \
                str(set_id)+'/'+str(question_select.order+1)+''
        return context

    def dispatch(self, request, *args, **kwargs):
        kwargs['last'] = True
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        question_set = BlankQuestionSet.objects.get(id=set_id)
        question_select = question_set.questions.filter(
            order=order).last()
        last_question = question_set.questions.order_by('order').last()
        if not last_question:
            return redirect('/')
        if last_question.order < int(order):
            self.kwargs['last'] = True
            self.get_context_data(**kwargs)
            level_blank, is_verb_blank, is_prep_blank = calc_total_level_blank(
                request.user)
            p1 = Thread(target=update_blank_userquestion_relation, args=(
                request.user, level_blank, is_verb_blank, is_prep_blank,))
            p1.start()
            return redirect('/question/v/check-answers/'+str(set_id)+'')
        return super(CommonBlankQuestionTemplate, self).dispatch(request, *args, **kwargs)



class VQuestionNewTemplate(LoginRequiredMixin, RedirectView):
    template_name = 'question/v-question.html'
    login_url = '/login/'
    
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        super().get_redirect_url(*args, **kwargs)
        question_set = generate_vquestion_set(self.request.user)
        return '/question/v/'+str(question_set.id)+'/1'


class OfferVQuestionNewTemplate(LoginRequiredMixin, RedirectView):
    template_name = 'question/offer-v-question.html'
    login_url = '/login/'

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        super().get_redirect_url(*args, **kwargs)
        question_set = generate_offer_vquestion_set(self.request.user)
        if question_set.questions.all().count() == 0:
            return '/accounts/dashboard'
        return '/question/v/offer/'+str(question_set.id)+'/1'


class CommonVQuestionNewTemplate(LoginRequiredMixin, RedirectView):
    template_name = 'question/offer-v-question.html'
    login_url = '/login/'

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        super().get_redirect_url(*args, **kwargs)
        question_set = generate_common_vquestion_set(self.request.user)
        if question_set.questions.all().count() == 0:
            return '/accounts/dashboard'
        return '/question/v/common/'+str(question_set.id)+'/1'


class HistoryChoiceTemplate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/history-choice.html'



class ProgressTemplate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/progress.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from django.core import serializers
        qs = BlankQuestionSet.objects.filter(user=self.request.user.qauser).order_by('created')
        qs_json = serializers.serialize('json', qs)
        context['data'] = qs_json
        return context


class ProgressBlankTemplate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/progress-blank.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from django.core import serializers
        qs = BlankQuestionSet.objects.filter(user=self.request.user.qauser, leveldetectionquestion__isnull=True).order_by('created')
        qs_json = serializers.serialize('json', qs)
        context['data'] = qs_json
        return context


class ProgressMCTemplate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/progress-mc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from django.core import serializers
        qs = MCQuestionSet.objects.filter(user=self.request.user.qauser, leveldetectionquestion__isnull=True).order_by('created')
        qs_json = serializers.serialize('json', qs)
        context['data'] = qs_json
        return context


class NewQuestionTemplate(StaffRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/new.html'


class ChangePasswordTemplate(TemplateView):
    login_url = '/login/'
    template_name = 'registration/change-password.html'


class SuccessMailTemplate(TemplateView):
    login_url = '/login/'
    template_name = 'registration/success-mail.html'


class FinalChangePasswordTemplate(TemplateView):
    login_url = '/login/'
    template_name = 'registration/final-change-password.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['uuid'] = self.kwargs['uuid']
        return context


class VQuestionHistoryListTemplate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/vc-history-list.html'


class VQuestionListTemplate(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'question/vc-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = BlankQuestion.objects.all()
        return context


def generate_vquestion_set(user):
    SET_COUNT = int(Config.objects.filter(name='question_set_count', active=True).last(
    ).value) if Config.objects.filter(name='question_set_count', active=True) else 30
    answers = []
    v_list = []
    for i in range(SET_COUNT):
        q = BlankQuestion.active.exclude(answer__in=answers).order_by('?').first()
        v_list.append(q)
        answers.append(q.answer)
    v_list = sorted(v_list, key=lambda x: x.origin_text.id)
    v_set = BlankQuestionSet.objects.create(user=user.qauser)
    order_counter = 1
    for v in v_list:
        v_obj = SelectedBlankQuestion.objects.create(question=v, order=order_counter)
        v_set.questions.add(v_obj)
        order_counter += 1
    return v_set


def generate_offer_vquestion_set(user):
    SET_COUNT = int(Config.objects.filter(name='question_offer_set_count', active=True).last(
    ).value) if Config.objects.filter(name='question_offer_set_count', active=True) else 10
    v_list = BlankQuestion.objects.filter(userblankquestionrelation__user=user.qauser).order_by(
        '-userblankquestionrelation__cosine_similarity','?')[:SET_COUNT]
    v_set = BlankQuestionSet.objects.create(user=user.qauser)
    order_counter = 1
    for v in v_list:
        v_obj = SelectedBlankQuestion.objects.create(question=v, order=order_counter)
        v_set.questions.add(v_obj)
        order_counter += 1
    return v_set


def generate_common_vquestion_set(user):
    SET_COUNT = int(Config.objects.filter(name='question_common_set_count', active=True).last(
    ).value) if Config.objects.filter(name='question_common_set_count', active=True) else 10
    q = SelectedBlankQuestion.objects.filter(blankquestionset__user=user.qauser).values_list('question__id', flat=True).distinct()
    v_ids = SelectedBlankQuestion.objects.exclude(answer=F('question__answer')).annotate(c=Count('question__id')).annotate(has_answered=Case(When(question_id__in=q,then=True), default=False, output_field=models.BooleanField())).values('has_answered','c').order_by('has_answered').values_list('question__id', flat=True)
    v_list = BlankQuestion.active.filter(id__in=v_ids)[:SET_COUNT]
    v_set = BlankQuestionSet.objects.create(user=user.qauser)
    order_counter = 1
    for v in v_list:
        v_obj = SelectedBlankQuestion.objects.create(question=v, order=order_counter)
        v_set.questions.add(v_obj)
        order_counter += 1
    return v_set


def generate_leveled_vquestion_set(user):
    SET_COUNT = 5
    answers = []
    v_list_A = []
    for i in range(SET_COUNT):
        q = BlankQuestion.active.exclude(answer__in=answers).filter(
        level='A').order_by('?').first()
        if q:
            v_list_A.append(q)
            answers.append(q.answer)
    v_list_A = sorted(v_list_A, key=lambda x: x.origin_text.id)
    answers = []
    v_list_B = []
    for i in range(SET_COUNT):
        q = BlankQuestion.active.exclude(answer__in=answers).filter(
        level='B').order_by('?').first()
        if q:
            v_list_B.append(q)
            answers.append(q.answer)
    v_list_B = sorted(v_list_B, key=lambda x: x.origin_text.id)
    answers = []
    v_list_C = []
    for i in range(SET_COUNT):
        q = BlankQuestion.active.exclude(answer__in=answers).filter(
        level='C').order_by('?').first()
        if q:
            v_list_C.append(q)
            answers.append(q.answer)
    v_list_C = sorted(v_list_C, key=lambda x: x.origin_text.id)
    v_set = BlankQuestionSet.objects.create(user=user.qauser)
    order_counter = 1
    for v_list in [v_list_A, v_list_B, v_list_C]:
        for v in v_list:
            v_obj = SelectedBlankQuestion.objects.create(
            question=v, order=order_counter)
            v_set.questions.add(v_obj)
            order_counter += 1
    LevelDetectionQuestion.objects.create(user=user, blank=v_set)
    return v_set

def check_answer(request, question_id):
    if request.method == 'GET':
        data = request.GET
        if question_id and BlankQuestionSet.objects.filter(id=question_id).exists():
            v_set = BlankQuestionSet.objects.get(id=question_id)
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


class OfferMCQuestionNewTemplate(LoginRequiredMixin, RedirectView):
    template_name = 'question/offer-mc-question.html'
    login_url = '/login/'
    
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        super().get_redirect_url(*args, **kwargs)
        question_set = generate_offer_mcquestion_set(self.request.user)
        if question_set.questions.all().count() == 0:
            return '/accounts/dashboard'
        return '/question/mc/offer/'+str(question_set.id)+'/1'

class CommonMCQuestionNewTemplate(LoginRequiredMixin, RedirectView):
    template_name = 'question/offer-mc-question.html'
    login_url = '/login/'
    
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        super().get_redirect_url(*args, **kwargs)
        question_set = generate_common_mcquestion_set(self.request.user)
        if question_set.questions.all().count() == 0:
            return '/accounts/dashboard'
        return '/question/mc/common/'+str(question_set.id)+'/1'

class MCQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/mc-question.html'
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        SHOW_WHOLE_TEXT = Config.objects.filter(name='show_whole_text', active=True).last(
        ).value if Config.objects.filter(name='show_whole_text', active=True) else 'false'
        TIMER_LIMIT = int(Config.objects.filter(name='timer_limit', active=True).last(
            ).value) if Config.objects.filter(name='timer_limit', active=True) else 60
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        if self.request.method == 'GET':
            data = self.request.GET
            answer = data.get('answer','')
        context = super().get_context_data(**kwargs)
        context['whole_text'] = True if SHOW_WHOLE_TEXT == 'true' else False
        context['timer_limit'] = TIMER_LIMIT
        question_set = MCQuestionSet.objects.get(id=set_id)
        index = question_set.questions.filter(order__lt=order).count()
        context['question_progress'] = int((index+1) / question_set.questions.count() * 100)
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
            level_mc, is_verb_mc, is_prep_mc = calc_total_level_mc(
                request.user)
            p2 = Thread(target=update_mc_userquestion_relation, args=(
                request.user, level_mc, is_verb_mc, is_prep_mc,))
            p2.start()
            return redirect('/question/mc/check-answers/'+str(set_id)+'')
        return super(MCQuestionTemplate, self).dispatch(request, *args, **kwargs)


class OfferMCQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/offer-mc-question.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        SHOW_WHOLE_TEXT = Config.objects.filter(name='show_whole_text', active=True).last(
        ).value if Config.objects.filter(name='show_whole_text', active=True) else 'false'
        TIMER_LIMIT = int(Config.objects.filter(name='timer_limit', active=True).last(
            ).value) if Config.objects.filter(name='timer_limit', active=True) else 60
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        if self.request.method == 'GET':
            data = self.request.GET
            answer = data.get('answer', '')
        context = super().get_context_data(**kwargs)
        context['whole_text'] = True if SHOW_WHOLE_TEXT == 'true' else False
        context['timer_limit'] = TIMER_LIMIT
        question_set = MCQuestionSet.objects.get(id=set_id)
        index = question_set.questions.filter(order__lt=order).count()
        context['question_progress'] = int((index+1) / question_set.questions.count() * 100)
        if answer:
            last_question = question_set.questions.filter(
                order__lt=order).order_by('order').last()
            last_question.answer = answer
            last_question.save()
        if not self.kwargs.get('last', None):
            question_select = question_set.questions.filter(
                order=order).last()
            context['question'] = question_select.question
            context['order'] = order
            context['next'] = '/question/mc/offer/' + \
                str(set_id)+'/'+str(question_select.order+1)+''
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
            level_mc, is_verb_mc, is_prep_mc = calc_total_level_mc(
                request.user)
            p2 = Thread(target=update_mc_userquestion_relation, args=(
                request.user, level_mc, is_verb_mc, is_prep_mc,))
            p2.start()
            return redirect('/question/mc/check-answers/'+str(set_id)+'')
        return super(OfferMCQuestionTemplate, self).dispatch(request, *args, **kwargs)


class CommonMCQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/offer-mc-question.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        SHOW_WHOLE_TEXT = Config.objects.filter(name='show_whole_text', active=True).last(
        ).value if Config.objects.filter(name='show_whole_text', active=True) else 'false'
        TIMER_LIMIT = int(Config.objects.filter(name='timer_limit', active=True).last(
            ).value) if Config.objects.filter(name='timer_limit', active=True) else 60
        set_id = self.kwargs['set_id']
        order = self.kwargs['order']
        if self.request.method == 'GET':
            data = self.request.GET
            answer = data.get('answer', '')
        context = super().get_context_data(**kwargs)
        context['whole_text'] = True if SHOW_WHOLE_TEXT == 'true' else False
        context['timer_limit'] = TIMER_LIMIT
        question_set = MCQuestionSet.objects.get(id=set_id)
        index = question_set.questions.filter(order__lt=order).count()
        context['question_progress'] = int((index+1) / question_set.questions.count() * 100)
        if answer:
            last_question = question_set.questions.filter(
                order__lt=order).order_by('order').last()
            last_question.answer = answer
            last_question.save()
        if not self.kwargs.get('last', None):
            question_select = question_set.questions.filter(
                order=order).last()
            context['question'] = question_select.question
            context['order'] = order
            context['next'] = '/question/mc/common/' + \
                str(set_id)+'/'+str(question_select.order+1)+''
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
            level_mc, is_verb_mc, is_prep_mc = calc_total_level_mc(
                request.user)
            p2 = Thread(target=update_mc_userquestion_relation, args=(
                request.user, level_mc, is_verb_mc, is_prep_mc,))
            p2.start()
            return redirect('/question/mc/check-answers/'+str(set_id)+'')
        return super(CommonMCQuestionTemplate, self).dispatch(request, *args, **kwargs)



def generate_mcquestion_set(user):
    SET_COUNT = int(Config.objects.filter(name='question_set_count', active=True).last(
    ).value) if Config.objects.filter(name='question_set_count', active=True) else 30
    answers = []
    mc_list = []
    for i in range(SET_COUNT):
        q = MultipleChoiceQuestion.active.exclude(answer__in=answers).order_by('?').first()
        mc_list.append(q)
        answers.append(q.answer)
    mc_list = sorted(mc_list, key=lambda x: x.origin_text.id)
    mc_set = MCQuestionSet.objects.create(user=user.qauser)
    order_counter = 1
    for mc in mc_list:
        mc_obj = SelectedMCQuestion.objects.create(question=mc, order=order_counter)
        mc_set.questions.add(mc_obj)
        order_counter += 1
    return mc_set


def generate_offer_mcquestion_set(user):
    SET_COUNT = int(Config.objects.filter(name='question_offer_set_count', active=True).last(
    ).value) if Config.objects.filter(name='question_offer_set_count', active=True) else 30
    mc_list = MultipleChoiceQuestion.objects.filter(usermcquestionrelation__user=user.qauser).order_by(
        '-usermcquestionrelation__cosine_similarity')[:SET_COUNT]
    mc_set = MCQuestionSet.objects.create(user=user.qauser)
    order_counter = 1
    for mc in mc_list:
        mc_obj = SelectedMCQuestion.objects.create(question=mc, order=order_counter)
        mc_set.questions.add(mc_obj)
        order_counter += 1
    return mc_set


def generate_common_mcquestion_set(user):
    SET_COUNT = int(Config.objects.filter(name='question_common_set_count', active=True).last(
    ).value) if Config.objects.filter(name='question_common_set_count', active=True) else 30
    q = SelectedMCQuestion.objects.filter(mcquestionset__user=user.qauser).values_list('question__id', flat=True).distinct()
    mc_ids = SelectedMCQuestion.objects.exclude(answer=F('question__answer')).annotate(c=Count('question__id')).annotate(has_answered=Case(When(question_id__in=q,then=True), default=False, output_field=models.BooleanField())).values('has_answered','c').order_by('has_answered').values_list('question__id', flat=True)
    mc_list = MultipleChoiceQuestion.active.filter(id__in=mc_ids)[:SET_COUNT]
    mc_set = MCQuestionSet.objects.create(user=user.qauser)
    order_counter = 1
    for mc in mc_list:
        mc_obj = SelectedMCQuestion.objects.create(question=mc, order=order_counter)
        mc_set.questions.add(mc_obj)
        order_counter += 1
    return mc_set


def generate_leveled_mcquestion_set(user):
    SET_COUNT = 5
    answers = []
    v_list_A = []
    for i in range(SET_COUNT):
        q = MultipleChoiceQuestion.active.exclude(answer__in=answers).filter(
        level='A').order_by('?').first()
        if q:
            v_list_A.append(q)
            answers.append(q.answer)
    v_list_A = sorted(v_list_A, key=lambda x: x.origin_text.id)
    answers = []
    v_list_B = []
    for i in range(SET_COUNT):
        q = MultipleChoiceQuestion.active.exclude(answer__in=answers).filter(
        level='B').order_by('?').first()
        if q:
            v_list_B.append(q)
            answers.append(q.answer)
    v_list_B = sorted(v_list_B, key=lambda x: x.origin_text.id)
    answers = []
    v_list_C = []
    for i in range(SET_COUNT):
        q = MultipleChoiceQuestion.active.exclude(answer__in=answers).filter(
        level='C').order_by('?').first()
        if q:
            v_list_C.append(q)
            answers.append(q.answer)
    v_list_C = sorted(v_list_C, key=lambda x: x.origin_text.id)
    v_set = MCQuestionSet.objects.create(user=user.qauser)
    order_counter = 1
    for v_list in [v_list_A, v_list_B, v_list_C]:
        for v in v_list:
            v_obj = SelectedMCQuestion.objects.create(
                question=v, order=order_counter)
            v_set.questions.add(v_obj)
            order_counter += 1
    l = LevelDetectionQuestion.objects.filter(user=user).last()
    l.mc = v_set
    l.save()
    return v_set


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
            file_level = get_level(file)
            words = pd.read_csv('./data/'+file)
            a = Analyser(words)
            a.analyse()
            result = a.get_vacancy_questions()
            whole_text = ''
            res = ''
            sentences = []
            index = 0
            for sentence in result:
                origin = ' '.join([word['word'] for word in sentence['words']])
                res += origin + ' '
                vacancy_arr = []
                answer = ''
                answer_type = ''
                for word in sentence['words']:
                    if not word['is_vacancy']:
                        vacancy_arr.append(word['word'])
                    else:
                        vacancy_arr.append('/&&__question__&&/')
                        answer = word['word']
                        if word['POSType'] and (not isinstance(word['POSType'],float)) and str(word['POSType']).startswith('V'):
                            answer_type = 'verb'
                        if word['POSType'] and (not isinstance(word['POSType'],float)) and str(word['POSType'].startswith('J') or str(word['POSType']).startswith('E')):
                            answer_type = 'preposition'
                        if word['word'] in Blocked.objects.all().values_tolist('text', flat=True):
                            answer_type = ''
                        # if word['POSType'] and (not isinstance(word['POSType'],float)) and str(word['POSType']).startswith('V'):
                        #     answer_type = 'verb'
                        # if word['POSType'] and (not isinstance(word['POSType'],float)) and str(word['POSType'].startswith('J') or str(word['POSType']).startswith('E')):
                        #     answer_type = 'preposition'
                vacancy_text = ' '.join(vacancy_arr)
                origin = origin.replace('-', '‌').replace('&quot;','\"')
                vacancy_text = vacancy_text.replace(
                    '-', '‌').replace('&quot;', '\"')
                answer = answer.replace('-', '‌').replace('&quot;', '\"')
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
                        whole_vacancy += tmp_sen['vacancy'] + ' '
                    else:
                        whole_vacancy += tmp_sen['origin'] + ' '
                res = res.replace('-', '‌').replace('&quot;','\"')
                whole_vacancy = whole_vacancy.replace(
                    '-', '‌').replace('&quot;', '\"')
                sentence['origin-text'] = res
                sentence['whole_vacancy'] = whole_vacancy
            if len(res.split(' ')) < 3:
                continue
            text = Text.objects.create(
                text=res,
                level=''
            )
            for q in sentences:
                if q['answer_type'] in ['verb', 'preposition']:
                    is_verb = q['answer_type'] == 'verb'
                    is_preposition = q['answer_type'] == 'preposition'
                    BlankQuestion.objects.create(
                        text=q['vacancy'],
                        whole_text=q['whole_vacancy'],
                        origin_text=text,
                        level=file_level,
                        answer=q['answer'],
                        is_verb=is_verb,
                        is_preposition=is_preposition,
                    )
        return HttpResponse('Done')


def get_level(file):
    if file.startswith('levelA'):
        return 'A'
    if file.startswith('levelB'):
        return 'B'
    if file.startswith('levelC'):
        return 'C'
    return 'C'

class CreateMCQuestions(View):
    def get(self, request):
        files = os.listdir('./data')
        csv_files = []
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(file)

        for file in csv_files:
            import re
            file_level = get_level(file)
            words = pd.read_csv('./data/'+file)
            a = Analyser(words)
            a.analyse()
            result = a.get_vacancy_questions()
            whole_text = ''
            res = ''
            sentences = []
            index = 0
            for sentence in result:
                origin = ' '.join([word['word'] for word in sentence['words']])
                res += origin + ' '
                vacancy_arr = []
                answer = ''
                answer_type = ''
                for word in sentence['words']:
                    if not word['is_vacancy']:
                        vacancy_arr.append(word['word'])
                    else:
                        vacancy_arr.append('/&&__question__&&/')
                        answer = word['word']
                        if word['POSType'] and (not isinstance(word['POSType'], float)) and str(word['POSType']).startswith('V'):
                            answer_type = 'verb'
                        if word['POSType'] and (not isinstance(word['POSType'], float)) and (str(word['POSType']).startswith('J') or str(word['POSType']).startswith('E')):
                            answer_type = 'preposition'
                vacancy_text = ' '.join(vacancy_arr)
                origin = origin.replace('-', '‌').replace('&quot;', '\"')
                vacancy_text = vacancy_text.replace(
                    '-', '‌').replace('&quot;', '\"')
                answer = answer.replace('-', '‌').replace('&quot;', '\"')
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
                        whole_vacancy += tmp_sen['vacancy'] + ' '
                    else:
                        whole_vacancy += tmp_sen['origin'] + ' '
                res = res.replace('-', '‌').replace('&quot;', '\"')
                whole_vacancy = whole_vacancy.replace(
                    '-', '‌').replace('&quot;', '\"')
                sentence['origin-text'] = res
                sentence['whole_vacancy'] = whole_vacancy
            if len(res.split(' ')) < 3:
                continue
            text = Text.objects.create(
                text=res,
                level=''
            )
            for q in sentences:
                if q['answer_type'] in ['verb', 'preposition']:
                    is_verb = q['answer_type'] == 'verb'
                    is_preposition = q['answer_type'] == 'preposition'
                    mc = MultipleChoiceQuestion.objects.create(
                        text=q['vacancy'],
                        whole_text=q['whole_vacancy'],
                        origin_text=text,
                        level=file_level,
                        answer=q['answer'],
                        is_verb=is_verb,
                        is_preposition=is_preposition,
                    )
                    o, is_created = OptionAnswer.objects.get_or_create(text=q['answer'])
                    options = [o]
                    
                    if is_verb:
                        # TODO: make more options
                        if VerbForm.objects.filter(form=q['answer']).exists():
                            verb_form = VerbForm.objects.filter(
                                form=q['answer']).last()
                            v_forms = list(verb_form.verb.verbform_set.exclude(form=q['answer']).order_by('-freq'))[:12]
                            import random
                            random.shuffle(v_forms)
                            v_forms = v_forms[:3]
                            for v in v_forms:
                                opt, is_created = OptionAnswer.objects.get_or_create(
                                    text=v.form)
                                options.append(opt)
                        else:
                            v_forms = list(VerbForm.objects.exclude(
                                form=q['answer']).order_by('-freq')[:50])
                            import random
                            random.shuffle(v_forms)
                            v_forms = v_forms[:3]
                            for v in v_forms:
                                opt, is_created = OptionAnswer.objects.get_or_create(text=v.form)
                                options.append(opt)
                        import random
                        random.shuffle(options)
                        for option in options:
                            mc.options.add(option)
                        if VerbForm.objects.filter(form=q['answer']).exists():
                            mc.id = None
                            mc.save()
                            mc.options.add(o)
                            verb_form = VerbForm.objects.filter(
                                form=q['answer']).last()
                            v_forms = list(VerbForm.objects.filter(tense=verb_form.tense).exclude(
                                form=q['answer']).order_by('-freq'))[:40]
                            import random
                            random.shuffle(v_forms)
                            v_forms = v_forms[:3]
                            for v in v_forms:
                                opt, is_created = OptionAnswer.objects.get_or_create(
                                    text=v.form)
                                mc.options.add(opt)

                    if is_preposition:
                        pres = PrePosition.objects.exclude(
                            text=q['answer']).order_by('?')[:3]
                        
                        mc.options.add(o)
                        for p in pres:
                            opt, is_created = OptionAnswer.objects.get_or_create(
                                text=p.text)
                            mc.options.add(opt)

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
    return redirect('/accounts/dashboard/')



def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        if User.objects.filter(username=username).exists():
            user = User.objects.filter(username=username).last()
            if not user.qauser.uuid:
                user.qauser.uuid = uuid.uuid4
                user.qauser.save()
            subject = 'تغییر رمز - سامانه یادگیری زبان فارسی'
            message = 'جهت تغییر رمز کاربری خود وارد لینک زیر شوید:\n' + \
                'http://46.209.4.197:8000/final-change-password/'+str(user.qauser.uuid)
            email(subject, message, username)
        return redirect('/send-success-mail')


def email(subject, message, dest):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [dest, ]
    send_mail(subject, message, email_from, recipient_list)


def change_password(request, uuid):
    if User.objects.filter(qauser__uuid=uuid).exists():
        user = User.objects.filter(qauser__uuid=uuid).last()
        user.set_password(request.POST.get('password','123456'))
        user.save()
        return redirect('/login')


class MCLevelQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/mc-level-question.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        SHOW_WHOLE_TEXT = Config.objects.filter(name='show_whole_text', active=True).last(
        ).value if Config.objects.filter(name='show_whole_text', active=True) else 'false'
        TIMER_LIMIT = int(Config.objects.filter(name='timer_limit', active=True).last(
            ).value) if Config.objects.filter(name='timer_limit', active=True) else 60
        order = self.kwargs['order']
        if self.request.method == 'GET':
            data = self.request.GET
            answer = data.get('answer', '')
        context = super().get_context_data(**kwargs)
        context['whole_text'] = True if SHOW_WHOLE_TEXT == 'true' else False
        context['timer_limit'] = TIMER_LIMIT
        question_set = LevelDetectionQuestion.objects.filter(user=self.request.user).last().mc
        index = question_set.questions.filter(order__lt=order).count()
        context['question_progress'] = int((index+1) / question_set.questions.count() * 100)
        if answer:
            last_question = question_set.questions.filter(
                order__lt=order).order_by('order').last()
            last_question.answer = answer
            last_question.save()
        if not self.kwargs.get('last', None):
            question_select = question_set.questions.filter(
                order=order).last()
            context['question'] = question_select.question
            context['order'] = order
            context['next'] = '/question/level-detection/mc/' +str(question_select.order+1)+''
        return context

    def dispatch(self, request, *args, **kwargs):
        kwargs['last'] = True
        order = self.kwargs['order']
        question_set = LevelDetectionQuestion.objects.filter(
            user=request.user).last().mc
        question_select = question_set.questions.filter(
            order=order).last()
        last_question = question_set.questions.order_by('order').last()
        if not last_question:
            return redirect('/')
        if last_question.order < int(order):
            self.kwargs['last'] = True
            self.get_context_data(**kwargs)
            return redirect('/question/level-check')
        return super(MCLevelQuestionTemplate, self).dispatch(request, *args, **kwargs)


class BlankLevelQuestionTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'question/v-level-question.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        generate_leveled_vquestion_set(self.request.user)
        generate_leveled_mcquestion_set(self.request.user)
        SHOW_WHOLE_TEXT = Config.objects.filter(name='show_whole_text', active=True).last(
        ).value if Config.objects.filter(name='show_whole_text', active=True) else 'false'
        ANSWER_REQUIRED = Config.objects.filter(name='answer_required', active=True).last(
        ).value if Config.objects.filter(name='answer_required', active=True) else 'false'
        TIMER_LIMIT = int(Config.objects.filter(name='timer_limit', active=True).last(
            ).value) if Config.objects.filter(name='timer_limit', active=True) else 60
        order = self.kwargs['order']
        if self.request.method == 'GET':
            data = self.request.GET
            answer = data.get('answer', '')
        context = super().get_context_data(**kwargs)
        context['whole_text'] = True if SHOW_WHOLE_TEXT == 'true' else False
        context['answer_required'] = True if ANSWER_REQUIRED == 'true' else False
        context['timer_limit'] = TIMER_LIMIT
        question_set = LevelDetectionQuestion.objects.filter(user=self.request.user).last().blank
        index = question_set.questions.filter(order__lt=order).count()
        context['question_progress'] = int((index+1) / question_set.questions.count() * 100)
        if answer:
            last_question = question_set.questions.filter(
                order__lt=order).order_by('order').last()
            last_question.answer = answer
            last_question.save()
        if not self.kwargs.get('last', None):
            question_select = question_set.questions.filter(
                order=order).last()
            context['question'] = question_select.question
            context['order'] = order
            context['next'] = '/question/level-detection/b/' + \
                str(question_select.order+1)+''
        return context

    def dispatch(self, request, *args, **kwargs):
        kwargs['last'] = True
        order = self.kwargs['order']
        question_set = LevelDetectionQuestion.objects.filter(
            user=request.user).last().blank
        question_select = question_set.questions.filter(
            order=order).last()
        last_question = question_set.questions.order_by('order').last()
        if not last_question:
            return redirect('/')
        if last_question.order < int(order):
            self.kwargs['last'] = True
            self.get_context_data(**kwargs)
            return redirect('/question/level-detection/mc/1')
        return super(BlankLevelQuestionTemplate, self).dispatch(request, *args, **kwargs)


def level_check(request):
    if request.method == 'GET':
        data = request.GET
        l_detect = LevelDetectionQuestion.objects.filter(
            user=request.user).last()
        mc_set = LevelDetectionQuestion.objects.filter(user=request.user).last().mc
        questions = mc_set.questions.all().order_by('order')
        answers_count = questions.count()
        my_data = []
        true_count = 0
        user_answers = []
        answers = []
        levels = {
            'A': 0,
            'B': 0,
            'C': 0,
        }
        WEIGHTS = {
            'A': 0.8,
            'B': 1,
            'C': 1.2,
        }
        for q in questions:
            answer = q.answer
            order = q.order
            user_answers.append(
                {'order': int(order), 'text': answer})
            if(answer == q.question.answer):
                levels[q.question.level] += 1 * WEIGHTS[q.question.level]
                true_count += 1
        mc_set.right_answers = true_count
        mc_set.question_count = answers_count
        mc_set.answer_percentage = true_count/answers_count if answers_count else 0
        mc_set.save()

        v_set = LevelDetectionQuestion.objects.filter(
            user=request.user).last().blank
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
                levels[q.question.level] += 1
                true_count += 1
        v_set.right_answers = true_count
        v_set.question_count = answers_count
        v_set.answer_percentage = true_count/answers_count if answers_count else 0
        v_set.save()
        level = calc_level(levels)
        p1 = Thread(target=update_blank_userquestion_relation, args=(request.user,level,1,1,))
        p1.start()
        p2 = Thread(target=update_mc_userquestion_relation, args=(request.user,level,1,1,))
        p2.start()
        request.user.qauser.level = level
        l_list = LevelDetectionQuestion.objects.all().exclude(id=l_detect.id)
        for l in l_list:
            if l.blank:
                l.blank.delete()
            if l.mc:
                l.mc.delete()
            l.delete()
        l_detect.has_answered_blank = True
        l_detect.has_answered_mc = True
        l_detect.save()
        return render(request, template_name='result.html', context={'level':level,'levels': levels})


def calc_level(levels):
    score = levels['A'] + levels['B'] + levels['C']
    if score < 9:
        return 'A'
    if score < 19:
        return 'B'
    return 'C'


SCORE_POINT = {
    'A': 1,
    'B': 2,
    'C': 3,
}

def update_blank_userquestion_relation(user, level, is_verb, is_prep):
    UserBlankQuestionRelation.objects.filter(user=user.qauser).delete()
    for q in BlankQuestion.objects.all():
        first_set = [q.level == 'A', q.level == 'B',q.level == 'C', q.is_verb, q.is_preposition]
        second_set = [level == 'A', level == 'B',level == 'C', is_verb, is_prep]
        cosine_similarity = spatial.distance.cosine(first_set, second_set)
        c = 1 if math.isnan(cosine_similarity) else 1-cosine_similarity
        UserBlankQuestionRelation.objects.create(user=user.qauser, question=q, cosine_similarity=c)


def update_mc_userquestion_relation(user, level, is_verb, is_prep):
    UserMCQuestionRelation.objects.filter(user=user.qauser).delete()
    for q in MultipleChoiceQuestion.objects.all():
        first_set = [q.level == 'A', q.level == 'B',q.level == 'C', q.is_verb, q.is_preposition]
        second_set = [level == 'A', level == 'B',level == 'C', is_verb, is_prep]
        cosine_similarity = spatial.distance.cosine(first_set, second_set)
        c = 1 if math.isnan(cosine_similarity) else 1-cosine_similarity
        UserMCQuestionRelation.objects.create(user=user.qauser, question=q, cosine_similarity=c)


def calc_total_level_mc(user):
    mc_questions = MultipleChoiceQuestion.objects.filter(
        selectedmcquestion__mcquestionset__user=user.qauser).values('level', 'selectedmcquestion__answer', 'answer', 'is_verb', 'is_preposition')
    sum_num = 0
    point = 0
    question_count = 0
    is_verb_count = 0
    is_verb = 0
    is_preposition_count = 0
    is_preposition  = 0
    for q in mc_questions:
        question_count += 1
        sum_num += SCORE_POINT[q['level']]
        if q['is_verb']:
            is_verb_count += 1
            if not q['selectedmcquestion__answer'] or q['selectedmcquestion__answer'] != q['answer']:
                is_verb += 1
        if q['is_preposition']:
            is_preposition_count += 1
            if not q['selectedmcquestion__answer'] or q['selectedmcquestion__answer'] != q['answer']:
                is_preposition += 1
        if q['selectedmcquestion__answer'] and q['selectedmcquestion__answer'] == q['answer']:
            point += SCORE_POINT[q['level']]
    result = point/sum_num
    level = ''
    if result < 0.33:
        level = 'A'
    elif result < 0.67:
        level = 'B'
    else:
        level = 'C'
    is_verb_prob = 0 if is_verb_count == 0 or is_verb/is_verb_count < 0.5 else 1
    is_preposition_prob = 0 if is_preposition_count == 0 or is_preposition/is_preposition_count < 0.5 else 1
    return level, is_verb_prob, is_preposition_prob
    

def calc_total_level_blank(user):
    mc_questions = BlankQuestion.objects.filter(
        selectedblankquestion__blankquestionset__user=user.qauser).values('level', 'selectedblankquestion__answer', 'answer', 'is_verb','is_preposition')
    sum_num = 0
    point = 0
    question_count = 0
    is_verb_count = 0
    is_verb = 0
    is_preposition_count = 0
    is_preposition = 0
    for q in mc_questions:
        question_count += 1
        sum_num += SCORE_POINT[q['level']]
        if q['is_verb']:
            is_verb_count += 1
            if not q['selectedblankquestion__answer'] or q['selectedblankquestion__answer'] != q['answer']:
                is_verb += 1
        if q['is_preposition']:
            is_preposition_count += 1
            if not q['selectedblankquestion__answer'] or q['selectedblankquestion__answer'] != q['answer']:
                is_preposition += 1
        if q['selectedblankquestion__answer'] and q['selectedblankquestion__answer'] == q['answer']:
            point += SCORE_POINT[q['level']]
    result = point/sum_num
    level = ''
    if result < 0.33:
        level = 'A'
    elif result < 0.67:
        level = 'B'
    else:
        level = 'C'
    is_verb_prob = 0 if is_verb_count == 0 or is_verb/is_verb_count < 0.5 else 1
    is_preposition_prob = 0 if is_preposition_count ==0 or is_preposition/is_preposition_count < 0.5 else 1
    return level, is_verb_prob, is_preposition_prob



def text_writing(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        user = request.user.qauser
        TextWriting.objects.create(user=user ,text=text)
        texts = TextWriting.objects.filter(user=user)
        return redirect('/text_list?add=true')
    return redirect('/')


def text_correct_api(request, id):
    if request.method == 'POST':
        modified_text = request.POST.get('modified_text', '')
        is_done = request.POST.get('is_done', 'off')
        if is_done == 'on':
            is_done = True
        else:
            is_done = False
        user = request.user.qauser
        TextWriting.objects.filter(id=id).update(modified_text=modified_text, is_done=is_done)
        texts = TextWriting.objects.filter(user__qagroup_users__admins=user)
        return redirect('/text_correct_list?add=true')
    return redirect('/')


class TextCorrectList(TemplateView):
    template_name = 'text_correct_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.qauser
        texts = TextWriting.objects.filter(user__qagroup_users__admins=user)
        add = self.request.GET.get('add', False)
        if add == 'true':
            add = True
        context['texts'] = texts
        context['add'] = add
        return context

class TextCorrect(TemplateView):
    template_name = 'text_correct.html'

    def get_context_data(self, **kwargs):
        text_id = kwargs['id']
        context = super().get_context_data(**kwargs)
        text_writing = TextWriting.objects.get(id=text_id)
        context['text_writing'] = text_writing
        return context


class TextList(TemplateView):
    template_name = 'text_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.qauser
        texts = TextWriting.objects.filter(user=user)
        add = self.request.GET.get('add', False)
        if add == 'true':
            add = True
        context['texts'] = texts
        context['add'] = add
        return context


class TextDetail(TemplateView):
    template_name = 'text_detail.html'

    def get_context_data(self, **kwargs):
        text_id = kwargs['id']
        context = super().get_context_data(**kwargs)
        text_writing = TextWriting.objects.get(id=text_id)
        context['text_writing'] = text_writing
        return context


def export_to_xml(request):
    if request.method == 'GET':
        from django.core import serializers
        from django.core.files import File
        text_id = request.GET.get('id', None)
        list_type = request.GET.get('type', None)
        user = request.user.qauser
        params = {
            'user': user
        }
        if text_id:
            params = {
                'id': text_id
            }
        if list_type == 'correct':
            params = {
                'user__qagroup_users__admins': user
            }
        texts = TextWriting.objects.filter(**params)
        data = serializers.serialize("xml", texts)
        f = open('./static/texts-'+request.user.username+'.xml', 'w+')
        myfile = File(f)
        myfile.write(data)
        myfile.close()
        response = FileResponse(open('./static/texts-'+request.user.username+'.xml', 'rb'))
        response['Content-Disposition'] = 'attachment; filename=' + 'texts-'+request.user.username+'.xml'
        return response



def svm_req(request):

    SPLIT_COUNT = int(Config.objects.filter(name='split_count', active=True).last().value) if Config.objects.filter(name='split_count', active=True) else 10
    SVM_DEGREE = int(Config.objects.filter(name='svm_degree', active=True).last().value) if Config.objects.filter(name='svm_degree', active=True) else 10
    MAX_ITER = int(Config.objects.filter(name='max_iter', active=True).last().value) if Config.objects.filter(name='max_iter', active=True) else 30
    SVM_GAMMA = Config.objects.filter(name='svm_gamma', active=True).last().value if Config.objects.filter(name='split_count', active=True) else 'scale'
    files = os.listdir('./data')

    csv_files = []
    for file in files:
        if file.endswith('.csv'):
            csv_files.append(file)

    datas = []
    levels = []

    for file in csv_files:
        file_level = get_level(file)
        levels.append(file_level)
        words = pd.read_csv('./data/'+file)
        a = Analyser(words)
        a.analyse()
        datas.append(a.tolist())

    X = np.array(datas)
    X = np.reshape(X,(len(X),-1))
    y = np.array(levels)
    kf = KFold(n_splits=SPLIT_COUNT)

    response = ''
    counter = 1

    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf = SVC(gamma=SVM_GAMMA, degree=SVM_DEGREE, max_iter=MAX_ITER)
        clf.fit(X_train, y_train)
        response += '<div> Test '+ str(counter) + ':</div>'
        response += '<div> '+ str(clf.score(X_test, y_test)) + ':</div>'
        counter += 1
    
    return HttpResponse(response)
