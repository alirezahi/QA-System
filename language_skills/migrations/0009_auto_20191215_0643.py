# Generated by Django 2.1.7 on 2019-12-15 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language_skills', '0008_blankquestionset_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='qauser',
            name='gender',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='verbform',
            name='freq',
            field=models.IntegerField(default=0),
        ),
    ]
