from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.


class QAUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    v_questions = models.ManyToManyField('VQuestionHistory', blank=True)
    mc_questions = models.ManyToManyField('MCQuestionHistory', blank=True)


class VQuestionHistory(models.Model):
    question = models.ForeignKey('VacancyQuestion', on_delete=models.CASCADE)
    right_answers = models.IntegerField()
    answers_count = models.IntegerField()
    answer_percentage = models.FloatField()


class MCQuestionHistory(models.Model):
    question = models.ForeignKey('MultipleChoiceQuestion', on_delete=models.CASCADE)
    right_answers = models.IntegerField()
    answers_count = models.IntegerField()
    answer_percentage = models.FloatField()


class AbstractAnswer(models.Model):
    text = models.CharField(max_length=200)
    order = models.IntegerField()

    class Meta:
        abstract = True


class Text(models.Model):
    text = models.TextField()
    level = models.CharField(max_length=4)

    def __str__(self):
        return self.text[:20] or ''


class OptionAnswer(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:20] or ''


class MCAnswer(AbstractAnswer):
    options = models.ManyToManyField(OptionAnswer)

    def __str__(self):
        return self.text[:20] or ''
    

class MultipleChoiceQuestion(models.Model):
    text = models.TextField()
    level = models.CharField(max_length=4)
    answers = models.ManyToManyField(MCAnswer)
    origin_text = models.ForeignKey(Text, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20] or ''


class VacancyAnswer(AbstractAnswer):
    text = models.TextField()

    def __str__(self):
        return self.text[:20] or ''


class VacancyQuestion(models.Model):
    text = models.TextField()
    level = models.CharField(max_length=4)
    answers = models.ManyToManyField(VacancyAnswer)
    origin_text = models.ForeignKey(Text, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20] or ''

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
      QAUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
     instance.qauser.save()