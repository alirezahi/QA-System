# Generated by Django 2.1.7 on 2020-01-20 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language_skills', '0009_auto_20191215_0643'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextWriting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('modified_text', models.TextField()),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
    ]
