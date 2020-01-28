from django.contrib import admin
from django.apps import apps
from django.db import models
from language_skills.models import *
# Register your models here.


class GroupUsersInline(admin.TabularInline):
    model = Group.users.through

class GroupAdminsInline(admin.TabularInline):
    model = Group.admins.through


class GroupAdmin(admin.ModelAdmin):
    # raw_id_fields = ('users','admins')
    exclude = ('users','admins')
    inlines = (GroupUsersInline, GroupAdminsInline)

class QAUserAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)


app = apps.get_app_config('language_skills')
for model_name, model in app.models.items():
    if not(model_name in ['group', 'qauser']):
        admin.site.register(model)


admin.site.register(Group, GroupAdmin)
admin.site.register(QAUser, QAUserAdmin)