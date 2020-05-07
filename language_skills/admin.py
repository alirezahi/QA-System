from django.contrib import admin
from django.apps import apps
from django.db import models
from language_skills.models import *
# Register your models here.


class GroupUsersInline(admin.TabularInline):
    model = QAGroup.users.through

class GroupAdminsInline(admin.TabularInline):
    model = QAGroup.admins.through


class GroupAdmin(admin.ModelAdmin):
    # raw_id_fields = ('users','admins')
    exclude = ('users','admins')
    inlines = (GroupUsersInline, GroupAdminsInline)

class QAUserAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')


app = apps.get_app_config('language_skills')
for model_name, model in app.models.items():
    if not(model_name in ['qagroup', 'qauser', 'config']):
        admin.site.register(model)


admin.site.register(QAGroup, GroupAdmin)
admin.site.register(QAUser, QAUserAdmin)
admin.site.register(Config, ConfigAdmin)