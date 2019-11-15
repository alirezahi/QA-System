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
    path('new', NewQuestionTemplate.as_view()),
    path('create', CreateQuestions.as_view()),
    # v-questions
    path('v/new', VQuestionNewTemplate.as_view()),
    path('v/list', VQuestionListTemplate.as_view()),
    path('v/history-list', VQuestionHistoryListTemplate.as_view()),
    path('v/check-answers/<question_id>', check_answer),
    path('v/<set_id>/<order>', BlankQuestionTemplate.as_view()),
    # mc-questions
    path('mc/new', MCQuestionNewTemplate.as_view()),
    path('mc/list', MCQuestionListTemplate.as_view()),
    path('mc/history-list', MCQuestionHistoryListTemplate.as_view()),
    path('mc/mcc', MCQuestionHistoryListTemplate1.as_view()),
    path('mc/check-answers/<question_id>', check_answer_mc),
    path('mc/<set_id>/<order>', MCQuestionTemplate.as_view()),
]
