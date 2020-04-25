"""QASystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .views import *

urlpatterns = [
    path('history-choice', HistoryChoiceTemplate.as_view()),
    path('offer-options', TemplateView.as_view(template_name='question/offer-option.html')),
    path('new', NewQuestionTemplate.as_view()),
    path('create', CreateQuestions.as_view()),
    path('create-mc', CreateMCQuestions.as_view()),
    # v-questions
    path('v/new', VQuestionNewTemplate.as_view()),
    path('v/offer/new', OfferVQuestionNewTemplate.as_view()),
    path('v/common/new', CommonVQuestionNewTemplate.as_view()),
    path('v/list', VQuestionListTemplate.as_view()),
    path('v/history-list', VQuestionHistoryListTemplate.as_view()),
    path('v/check-answers/<question_id>', check_answer),
    path('v/<set_id>/<order>', BlankQuestionTemplate.as_view()),
    path('v/offer/<set_id>/<order>', OfferBlankQuestionTemplate.as_view()),
    path('v/common/<set_id>/<order>', CommonBlankQuestionTemplate.as_view()),
    # mc-questions
    path('mc/new', MCQuestionNewTemplate.as_view()),
    path('mc/offer/new', OfferMCQuestionNewTemplate.as_view()),
    path('mc/common/new', CommonMCQuestionNewTemplate.as_view()),
    path('mc/list', MCQuestionListTemplate.as_view()),
    path('mc/history-list', MCQuestionHistoryListTemplate.as_view()),
    path('mc/mcc', MCQuestionHistoryListTemplate1.as_view()),
    path('mc/check-answers/<question_id>', check_answer_mc),
    path('mc/<set_id>/<order>', MCQuestionTemplate.as_view()),
    path('mc/offer/<set_id>/<order>', OfferMCQuestionTemplate.as_view()),
    path('mc/common/<set_id>/<order>', CommonMCQuestionTemplate.as_view()),
    # level-detection
    path('level-detection/b/<order>', BlankLevelQuestionTemplate.as_view()),
    path('level-detection/mc/<order>', MCLevelQuestionTemplate.as_view()),
    path('level-check', level_check),
    #text
    path('add_list', AddListTemplateView.as_view()),
    path('add_list_request', add_list),
    path('export_to_xml', export_to_xml),
    path('svm/csv', svm_csv_req),
    path('svm', svm_req),
    path('rf/csv', rf_csv_req),
    path('rf', rf_req),
    path('logistic/csv', logistic_csv_req),
    path('logistic', logistic_req),
    path('analyse', analyse_request),
]
