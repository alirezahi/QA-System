# Generated by Django 2.1.7 on 2020-02-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language_skills', '0014_auto_20200207_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blocked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
            ],
        ),
    ]
