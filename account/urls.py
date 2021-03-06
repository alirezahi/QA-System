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
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from account.views import register, ProfileView, confirmation_mail, send_mail_confirm


urlpatterns = [
    path('dashboard/', login_required(ProfileView.as_view()), name='dashboard'),
    path('login/', LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name='login'),
    path('register/', register, name='register'),
    path('send-mail-confirm/', send_mail_confirm, name='send_mail_confirm'),
    path('confirmation-mail/', confirmation_mail, name='confirmation_mail'),
    path('confirmation-success/', TemplateView.as_view(template_name='registration/confirmation-success.html'), name='confirmation_success'),
    path('profile/', RedirectView.as_view(permanent=False, url='/accounts/dashboard')),
]
