# Generated by Django 2.1.7 on 2019-12-08 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('language_skills', '0003_leveldetectionquestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leveldetectionquestion',
            name='blank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='language_skills.BlankQuestionSet'),
        ),
        migrations.AlterField(
            model_name='leveldetectionquestion',
            name='mc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='language_skills.MCQuestionSet'),
        ),
    ]