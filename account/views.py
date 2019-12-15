from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from language_skills.models import *
# from language_skills.utilities import a

# Create your views here.


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
        context['has_answered_level_detection'] = not(LevelDetectionQuestion.objects.filter(user=self.request.user, has_answered_blank=False).exists() or LevelDetectionQuestion.objects.filter(user=self.request.user, has_answered_mc=False).exists())
        context['has_answered_blank'] = not(LevelDetectionQuestion.objects.filter(user=self.request.user, has_answered_blank=False).exists())
        context['has_answered_mc'] = not(LevelDetectionQuestion.objects.filter(user=self.request.user, has_answered_mc=False).exists())
        return context


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        name = request.POST.get('name', '')
        lastname = request.POST.get('lastname', '')
        birth_date = str(request.POST.get('birth-date-year', '2000')) +'-'+ str(request.POST.get('birth-date-month', '01')) +'-'+ str(request.POST.get('birth-date-day', '01'))
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
        qauser.save()
        new_user = authenticate(username=username,
                                password=password,
                                )
        login(request, new_user)
        return HttpResponseRedirect("/accounts/dashboard")
