from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.


# =======   general classes    ========
class RandomManager(models.Manager):
    
  def get_random(self, items=1):
    '''
    items is integer value
    By default it returns 1 random item
    '''
    if isinstance(items, int):
        return self.model.objects.order_by('?')[:items]
    return self.all()

# ===============

class QAUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class MCQuestionHistory(models.Model):
    question = models.ForeignKey('MCQuestionSet', on_delete=models.CASCADE)
    right_answers = models.IntegerField()
    answers_count = models.IntegerField()
    answer_percentage = models.FloatField()


class AbstractAnswer(models.Model):
    answer = models.CharField(max_length=200)
    is_verb = models.BooleanField(default=False)
    is_preposition = models.BooleanField(default=False)

    class Meta:
        abstract = True


class AbstractOrder(models.Model):
    order = models.IntegerField()

    class Meta:
        abstract = True


class AbstractActive(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Text(models.Model):
    text = models.TextField()
    level = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return self.text[:20] or ''


class OptionAnswer(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:20] or ''


class MultipleChoiceQuestion(AbstractAnswer, AbstractActive):
    text = models.TextField()
    whole_text = models.TextField()
    level = models.CharField(max_length=4)
    options = models.ManyToManyField(OptionAnswer, blank=True)
    origin_text = models.ForeignKey(Text, on_delete=models.CASCADE)

    objects = RandomManager()

    def __str__(self):
        return self.text[:20] or ''


class SelectedMCQuestion(AbstractOrder):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200, blank=True, null=True)
    

class MCQuestionSet(models.Model):
    questions = models.ManyToManyField(SelectedMCQuestion, blank=True)
    right_answers = models.IntegerField(blank=True, null=True)
    question_count = models.IntegerField(blank=True, null=True)
    answer_percentage = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(
        QAUser, null=True, blank=True, on_delete=models.CASCADE)


class VacancyQuestion(AbstractAnswer, AbstractActive):
    text = models.TextField()
    whole_text = models.TextField()
    level = models.CharField(max_length=4)
    origin_text = models.ForeignKey(Text, on_delete=models.CASCADE)

    objects = RandomManager()

    def __str__(self):
        return self.text[:20] or ''


class SelectedVacancyQuestion(AbstractOrder):
    question = models.ForeignKey(VacancyQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200, blank=True, null=True)


class VacancyQuestionSet(models.Model):
    questions = models.ManyToManyField(SelectedVacancyQuestion, blank=True)
    right_answers = models.IntegerField(blank=True, null=True)
    question_count = models.IntegerField(blank=True, null=True)
    answer_percentage = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(QAUser, null=True, blank=True, on_delete=models.CASCADE)


class Config(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    value = models.CharField(max_length=200, null=False, blank=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' - ' + self.value


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
      QAUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
     instance.qauser.save()
