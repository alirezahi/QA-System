from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class QAUser(User):
    pass


class AbstractAnswer(models.Model):
    text = models.CharField(max_length=200)
    order = models.IntegerField()

    class Meta:
        abstract = True


class Text(models.Model):
    text = models.TextField()
    level = models.CharField(max_length=4)


class OptionAnswer(models.Model):
    text = models.TextField()


class MCAnswer(AbstractAnswer):
    start = models.IntegerField()
    end = models.IntegerField()
    options = models.ManyToManyField(OptionAnswer)
    

class MultipleChoiceQuestion(models.Model):
    text = models.TextField()
    level = models.CharField(max_length=4)
    answers = models.ForeignKey(MAAnswer, on_delete=models.CASCADE)
    origin_text = models.ForeignKey(Text, on_delete=models.CASCADE)


class VacancyAnswer(AbstractAnswer):
    start = models.IntegerField()
    end = models.IntegerField()
    text = models.TextField()


class VacancyQuestion(models.Model):
    text = models.TextField()
    level = models.CharField(max_length=4)
    answers = models.ForeignKey(VacancyAnswer, on_delete=models.CASCADE)
    origin_text = models.ForeignKey(Text, on_delete=models.CASCADE)
