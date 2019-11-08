from django.contrib import admin
from django.apps import apps
# Register your models here.

app = apps.get_app_config('language_skills')
for model_name, model in app.models.items():
    admin.site.register(model)
