from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from language_skills.models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from language_skills.views import email
import threading
# from language_skills.utilities import a

# Create your views here.
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

class TestView(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        # context['sample'] = a.tojson()
        return context


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        show_level_detection = Config.objects.filter(name='show_level_detection', active=True).last(
        ).value if Config.objects.filter(name='show_level_detection', active=True) else ''
        if show_level_detection == 'true':
            context['has_answered_level_detection'] = False
        else:
            context['has_answered_level_detection'] = not(LevelDetectionQuestion.objects.filter(
            user=self.request.user, has_answered_blank=False).exists() or LevelDetectionQuestion.objects.filter(user=self.request.user, has_answered_mc=False).exists())
        context['has_answered_blank'] = not(LevelDetectionQuestion.objects.filter(user=self.request.user, has_answered_blank=False).exists())
        context['has_answered_mc'] = not(LevelDetectionQuestion.objects.filter(user=self.request.user, has_answered_mc=False).exists())
        return context


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        name = request.POST.get('name', '')
        lastname = request.POST.get('lastname', '')
        birth_date = str(request.POST.get('birth-date-year', '2000') or '2000') +'-'+ str(request.POST.get('birth-date-month', '01') or '01') +'-'+ str(request.POST.get('birth-date-day', '01') or '01')
        country = request.POST.get('country', '')
        gender = request.POST.get('gender', '')
        native_language = request.POST.get('native-language', '')
        is_mother_persian = request.POST.get('is_mother_persian', '')
        mother_native_language = request.POST.get(
            'mother-native-language', '')
        is_father_persian = request.POST.get('is_father_persian', '')
        father_native_language = request.POST.get('father-native-language', '')
        is_student = request.POST.get('is_student','')
        university = request.POST.get('university','')
        major = request.POST.get('major','')
        reason = request.POST.get('reason','')
        is_knowing_persian = request.POST.get('is_knowing_persian', '')
        how_knowing = request.POST.get('how-knowing', '')
        if User.objects.filter(username=username).exists():
            return HttpResponse('User Duplicate')
        
        user = User.objects.create(username=username,first_name=name,last_name=lastname)
        user.set_password(password)
        user.save()
        qauser = user.qauser
        qauser.birth_date = birth_date
        qauser.gender = gender
        qauser.native_lang = native_language
        qauser.is_mother_persian = is_mother_persian == 'on'
        qauser.mother_native_language = mother_native_language
        qauser.is_father_persian = is_father_persian == 'on'
        qauser.father_native_language = father_native_language
        qauser.is_student = is_student == 'on'
        qauser.university = university
        qauser.major = major
        qauser.lang_reason = reason
        qauser.is_knowing_persian = is_knowing_persian == 'on'
        qauser.persian_knowing_reason = how_knowing
        new_user = authenticate(username=username,
                                password=password,
                                )
            
        subject = 'فعال‌سازی حساب کاربری'
        account_activation_token = TokenGenerator().make_token(user)
        qauser.activation_token = account_activation_token
        qauser.save()
        message = 'جهت فعال‌سازی حساب کاربری خود وارد لینک زیر شوید:\nhttp://'+request.get_host()+'/accounts/confirmation-mail?username='+username+'&token='+account_activation_token
        dest = username
        t1 = threading.Thread(target=email, args=(message,dest,))
        t1.start()
        login(request, new_user)
        return HttpResponseRedirect("/accounts/dashboard")


def send_mail_confirm(request):
    user = request.user
    username = user.username
    qauser = user.qauser
    account_activation_token = ''
    if not qauser.activation_token:
        account_activation_token = TokenGenerator().make_token(user)
        qauser.activation_token = account_activation_token
        qauser.save()
    else:
        account_activation_token = qauser.activation_token
    subject = 'فعال‌سازی حساب کاربری'
    message = 'جهت فعال‌سازی حساب کاربری خود وارد لینک زیر شوید:\nhttp://'+request.get_host()+'/accounts/confirmation-mail?username='+username+'&token='+account_activation_token
    dest = username
    t1 = threading.Thread(target=email, args=(message,dest,))
    t1.start()
    return HttpResponseRedirect("/accounts/dashboard")


def confirmation_mail(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')
        token = request.GET.get('token', '')
        user = User.objects.filter(username=username).first()
        qauser = user.qauser
        if qauser.activation_token == token:
            qauser.is_activate = True
            qauser.save()
            return HttpResponseRedirect("/accounts/confirmation-success")
    return HttpResponseRedirect("/accounts/dashboard")
