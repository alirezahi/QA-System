from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.
REASONS = (
    (1, 'تحصیل دانشجوی خارجی در ایران'),
    (2, 'اختلال در یادگیری زبان فارسی'),
    (3, 'ایرانی مقیم خارج از کشور'),
    (4, 'علاقه شخصی'),
)

# =======   general classes    ========


class RandomManager(models.Manager):

    def get_random(self,order=[], items=1):
        '''
        items is integer value
        By default it returns 1 random item
        '''
        if isinstance(items, int):
            return self.model.objects.order_by('?',*order)[:items]
        return self.all()


class IsActiveManager(models.Manager):
    def get_queryset(self):
        return super(IsActiveManager, self).get_queryset().filter(is_active=True)
# ===============


class QAUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_token = models.CharField(max_length=100, null=True, blank=True)
    is_activate = models.BooleanField(default=False)
    level = models.CharField(max_length=10, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    birth_country = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    native_lang = models.CharField(max_length=200, null=True, blank=True)
    is_mother_persian = models.BooleanField(default=False)
    is_father_persian = models.BooleanField(default=False)
    mother_native_language = models.CharField(
        max_length=200, null=True, blank=True)
    father_native_language = models.CharField(
        max_length=200, null=True, blank=True)
    is_student = models.BooleanField(default=False)
    university = models.CharField(max_length=200, null=True, blank=True)
    major = models.CharField(max_length=200, null=True, blank=True)
    lang_reason = models.CharField(
        choices=REASONS, max_length=50, null=True, blank=True)
    is_knowing_persian = models.BooleanField(default=False)
    persian_knowing_reason = models.TextField(null=True, blank=True)
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    

    def __str__(self):
        return self.user.username


class QAGroup(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(QAUser, blank=True,related_name='qagroup_users')
    admins = models.ManyToManyField(QAUser, blank=True,related_name='qagroup_admins')

    def __str__(self):
        return self.name




class AbstractAnswer(models.Model):
    answer = models.CharField(max_length=200)
    kind = models.CharField(max_length=200, null=True, blank=True)
    # is_verb = models.BooleanField(default=False)
    # is_preposition = models.BooleanField(default=False)

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
    part_text = models.TextField(null=True,blank=True)
    level = models.CharField(max_length=4)
    options = models.ManyToManyField(OptionAnswer, blank=True)
    origin_text = models.ForeignKey(Text, on_delete=models.CASCADE)

    objects = RandomManager()
    active = IsActiveManager()

    @property
    def options_random(self):
        return self.options.order_by('?')
    
    def __str__(self):
        return self.text[:20] or ''


class SelectedMCQuestion(AbstractOrder):
    question = models.ForeignKey(
        MultipleChoiceQuestion, on_delete=models.CASCADE, related_name='selectedmcquestion')
    answer = models.CharField(max_length=200, blank=True, null=True)


class MCQuestionSet(models.Model):
    questions = models.ManyToManyField(SelectedMCQuestion, blank=True, related_name='mcquestionset')
    right_answers = models.IntegerField(blank=True, null=True)
    question_count = models.IntegerField(blank=True, null=True)
    answer_percentage = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    user = models.ForeignKey(
        QAUser, null=True, blank=True, on_delete=models.CASCADE)




class BlankQuestion(AbstractAnswer, AbstractActive):
    text = models.TextField()
    whole_text = models.TextField()
    part_text = models.TextField(null=True,blank=True)
    level = models.CharField(max_length=4)
    origin_text = models.ForeignKey(Text, on_delete=models.CASCADE)

    objects = RandomManager()
    active = IsActiveManager()

    def __str__(self):
        return self.text[:20] or ''


class SelectedBlankQuestion(AbstractOrder):
    question = models.ForeignKey(BlankQuestion, on_delete=models.CASCADE, related_name='selectedblankquestion')
    answer = models.CharField(max_length=200, blank=True, null=True)


class BlankQuestionSet(models.Model):
    questions = models.ManyToManyField(SelectedBlankQuestion, blank=True,related_name='blankquestionset')
    right_answers = models.IntegerField(blank=True, null=True)
    question_count = models.IntegerField(blank=True, null=True)
    answer_percentage = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(
        QAUser, null=True, blank=True, on_delete=models.CASCADE)


class Blocked(models.Model):
    text = models.CharField(max_length=200)


class RandomModel(models.Model):
    objects = RandomManager()

class PrePosition(models.Model):
    text = models.CharField(max_length=100)

    objects = RandomManager()

    def __str__(self):
        return self.text[:20] or ''


class VerbInfo(models.Model):
    infinitive = models.CharField(max_length=100)
    past_root = models.CharField(max_length=100)
    passive = models.CharField(max_length=200)
    
    def __str__(self):
        return self.infinitive


class VerbForm(models.Model):
    tense = models.CharField(max_length=100)
    form = models.CharField(max_length=100)
    verb = models.ForeignKey(VerbInfo, on_delete=models.CASCADE)
    freq = models.IntegerField(default=0)

    objects = RandomManager()

    def __str__(self):
        return self.form


class Classifier(RandomModel):
    text = models.CharField(max_length=100)
    root = models.CharField(max_length=100)
    freq = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:20] or ''


class Adjective(RandomModel):
    text = models.CharField(max_length=100)
    root = models.CharField(max_length=100)
    freq = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:20] or ''


class Adverb(RandomModel):
    text = models.CharField(max_length=100)
    root = models.CharField(max_length=100)
    freq = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:20] or ''


class Interjection(RandomModel):
    text = models.CharField(max_length=100)
    root = models.CharField(max_length=100)
    freq = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:20] or ''


class Determiner(RandomModel):
    text = models.CharField(max_length=100)
    root = models.CharField(max_length=100)
    freq = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:20] or ''


class Noun(RandomModel):
    text = models.CharField(max_length=100)
    root = models.CharField(max_length=100)
    freq = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:20] or ''


class Conjunction(RandomModel):
    text = models.CharField(max_length=100)
    root = models.CharField(max_length=100)
    freq = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:20] or ''


class Pronoun(RandomModel):
    text = models.CharField(max_length=100)
    root = models.CharField(max_length=100)
    freq = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:20] or ''


class Config(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    value = models.CharField(max_length=200, null=False, blank=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' - ' + self.value


class LevelDetectionQuestion(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    blank = models.ForeignKey(BlankQuestionSet,
                              null=True, blank=True, on_delete=models.CASCADE)
    mc = models.ForeignKey(
        MCQuestionSet, null=True, blank=True, on_delete=models.CASCADE)
    has_answered_blank = models.BooleanField(default=False)
    has_answered_mc = models.BooleanField(default=False)


class UserMCQuestionRelation(models.Model):
    user = models.ForeignKey(QAUser, on_delete=models.CASCADE, related_name='usermcquestionrelation')
    question = models.ForeignKey(
        MultipleChoiceQuestion, on_delete=models.CASCADE, related_name='usermcquestionrelation')
    cosine_similarity = models.FloatField(default=1)


class UserBlankQuestionRelation(models.Model):
    user = models.ForeignKey(QAUser, on_delete=models.CASCADE, related_name='userblankquestionrelation')
    question = models.ForeignKey(BlankQuestion, on_delete=models.CASCADE, related_name='userblankquestionrelation')
    cosine_similarity = models.FloatField(default=1)


class TextWriting(models.Model):
    user = models.ForeignKey(QAUser, on_delete=models.CASCADE, related_name='user_text_writing', null=True, blank=True)
    text = models.TextField()
    modified_text = models.TextField()
    is_done = models.BooleanField(default=False)


# ==================


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    from language_skills.views import generate_leveled_vquestion_set, generate_leveled_mcquestion_set
    if created:
        QAUser.objects.create(user=instance)
        generate_leveled_vquestion_set(instance)
        generate_leveled_mcquestion_set(instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.qauser.save()


# ==================


# @receiver(post_save, sender=BlankQuestion)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         for user in QAUser.objects.all():
#             QAUser.objects.first().blankquestionset_set.values_list('questions__id').distinct()
#       QAUser.objects.create(user=instance)
