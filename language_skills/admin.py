from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Text)
admin.site.register(QAUser)
admin.site.register(MCAnswer)
admin.site.register(OptionAnswer)
admin.site.register(VacancyAnswer)
admin.site.register(VacancyQuestion)
admin.site.register(VQuestionHistory)
admin.site.register(MCQuestionHistory)
admin.site.register(MultipleChoiceQuestion)
