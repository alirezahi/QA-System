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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import RedirectView
from account.views import TestView
from language_skills.views import reset_password, change_password, ChangePasswordTemplate, FinalChangePasswordTemplate, SuccessMailTemplate, ProgressTemplate


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('registration/login/',
    #      RedirectView.as_view(permanent=False, url='/accounts/login')),
    path('accounts/', include('account.urls')),
    path('question/', include('language_skills.urls')),
    path('progress/', ProgressTemplate.as_view()),
    path('test/', TestView.as_view()),
    path('login/', TemplateView.as_view(template_name='login.html')),
    path('signup/', TemplateView.as_view(template_name='register.html')),
    path('change-password-mail/',
        ChangePasswordTemplate.as_view()),
    path('request-change-password/',
        reset_password),
    path('send-success-mail', SuccessMailTemplate.as_view()),
    path('final-change-password/<uuid>',
        FinalChangePasswordTemplate.as_view()),
    path('validate-change-password/<uuid>',
        change_password),
    path('logout/', LogoutView.as_view(next_page='/login')),
]
