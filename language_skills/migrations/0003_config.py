# Generated by Django 2.1.7 on 2019-11-01 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language_skills', '0002_selectedmcquestion_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]