from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
# from language_skills.utilities import a

# Create your views here.


class TestView(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        # context['sample'] = a.tojson()
        return context


def register(request):
    if request.method == 'POST':
        import pdb;pdb.set_trace()
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        name = request.POST.get('name', '')
        lastname = request.POST.get('lastname', '')
        birth_date = request.POST.get(
            'birth-date', '1990-01-01') or '1990-01-01'
        country = request.POST.get('country', '')
        native_language = request.POST.get('native-language', '')
        is_parent_persian = request.POST.get('is_parent_persian', False)
        is_student = request.POST.get('is_student',False)
        university = request.POST.get('university','')
        major = request.POST.get('major','')
        reason = request.POST.get('reason','')
        is_knowing_persian = request.POST.get('is_knowing_persian', False)
        how_knowing = request.POST.get('how-knowing', '')

        if User.objects.filter(username=username).exists():
            return ''
        
        user = User.objects.create(username=username,first_name=name,last_name=lastname)
        user.set_password(password)
        user.save()
        qauser = user.qauser
        qauser.birth_date = birth_date
        qauser.birth_country = country
        qauser.native_lang = native_language
        qauser.is_parent_persian = is_parent_persian
        qauser.is_student = is_student
        qauser.university = university
        qauser.major = major
        qauser.lang_reason = reason
        qauser.is_knowing_persian = is_knowing_persian
        qauser.persian_knowing_reason = how_knowing
        qauser.save()
        new_user = authenticate(username=username,
                                password=password,
                                )
        login(request, new_user)
        return HttpResponseRedirect("/accounts/dashboard")
