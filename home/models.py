from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.http import Http404
from .RichTextBleachField import RichTextBleachField
from django.db.models import Count


class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    UNSPECIFIED = 'U', 'Unspecified'


class Profile(models.Model):
    '''
    Profile will be used as the base user in the Shlifim website.
    Profile is an extention to the imported 'User' from 'django.contrib.auth.models'.
    Imported Fields:
    username - Required. 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
    password - Required. A hash of, and metadata about, the password. (Django doesn’t store the raw password).
               Raw passwords can be arbitrarily long and can contain any character.
    date_joined - A datetime designating when the account was created. Is set to the current date/time by default
        when the account is created.
    email - Email address.
    is_superuser - Boolean. Designates that this user has all permissions without explicitly assigning them.
    Added Fields:
    gender - Default gender is set to 'Unspecified', A user can choose to specifie its gender to Male/Female.
    is blocked - Boolean. Designates that this user won't be able to login until an admin unblockes him.
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.UNSPECIFIED)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return '{self.user.username}'.format(self=self)

    @classmethod
    def create(cls, username, password, email, gender='U', is_blocked=False):
        user = User.objects.create_user(username=username, password=password, email=email)
        profile = cls(user=user, gender=gender, is_blocked=is_blocked)
        profile.save()
        return profile


class Subject(models.Model):
    subject_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.subject_name


class Sub_Subject(models.Model):
    sub_subject_name = models.CharField(max_length=100)
    related_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_subject_name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub_subject_name', 'related_subject'], name='unique_sub_subject')
        ]


class Book(models.Model):
    book_name = models.CharField(max_length=100, unique=True)
    related_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.book_name


class Grade(models.TextChoices):
    GRADE7 = '7', 'Seventh Grade'
    GRADE8 = '8', 'Eighth grade'
    GRADE9 = '9', 'Ninth grade'
    GRADE10 = '10', 'Tenth grade'
    GRADE11 = '11', 'Eleventh grade'
    GRADE12 = '12', 'Twelfth grade'


class Question(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = RichTextBleachField(blank=True, null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    sub_subject = models.ForeignKey(Sub_Subject, on_delete=models.CASCADE, blank=True, null=True)  # field not required
    grade = models.CharField(max_length=2, choices=Grade.choices)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)  # field not required
    book_page = models.IntegerField(null=True, blank=True,
                                    validators=[MinValueValidator(1), MaxValueValidator(999)])  # field not required
    is_edited = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', through='Question_Tag')

    class Meta:
        ordering = ['-publish_date']  # default ordered by publish_date

    def __str__(self):
        return f"Question #{self.id} : {self.title} ( {self.publish_date.strftime('%d/%m/%Y %H:%M')} )"

    # Input: a set of strings represting tag names.
    def add_tags_to_question(self, tags):
        for tag_name in tags:
            # if tag exist in DB - fetch the tag. else, create a new tag.
            tag, created = Tag.objects.get_or_create(tag_name=tag_name)
            if created:
                tag.tag_name = tag_name
                tag.save()
            # add a new Question_Tag only if tag not in self.tags.
            if tag not in self.tags.all():
                new_pair = Question_Tag()
                new_pair.question = self
                new_pair.tag = tag
                new_pair.save()

    def get_answers_feed(self, filter_type=''):
        '''
        Get all the answers in the DB for that question
        Also get filter type param for chosing between date / likes count filter
        '''
        answers = self.answer_set
        if filter_type == 'date' or filter_type == '':
            answers = answers.order_by('-publish_date')
        elif filter_type == 'votes':
            answers = answers.annotate(q_count=Count('likes')).order_by('-q_count')
        else:
            raise Http404()
        return answers

    def get_question_title(self):
        return str(self.subject) + '-' + self.title

    def get_answers_num(self):
        return self.answer_set.count()


class Answer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = RichTextBleachField(blank=True, null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(Profile, blank=True, related_name='user_answer_likes')
    dislikes = models.ManyToManyField(Profile, blank=True, related_name='user_answer_dislikes')
    is_edited = models.BooleanField(default=False)
    ordering = ['publish_date']

    def __str__(self):
        return self.content

    def profile_liked(self, profile):
        return profile in self.likes.all()

    def profile_disliked(self, profile):
        return profile in self.dislikes.all()

    def set_is_edited(self, newVal):
        self.is_edited = newVal

    def handle_thumb_up(self, profile):
        liked = self.likes.filter(user_id=profile.user_id).exists()
        disliked = self.dislikes.filter(user_id=profile.user_id).exists()
        if liked:
            self.likes.remove(profile)
        else:
            self.likes.add(profile)
        if disliked:
            self.dislikes.remove(profile)

    def handle_thumb_down(self, profile):
        liked = self.likes.filter(user_id=profile.user_id).exists()
        disliked = self.dislikes.filter(user_id=profile.user_id).exists()

        if disliked:
            self.dislikes.remove(profile)
        else:
            self.dislikes.add(profile)
        if liked:
            self.likes.remove(profile)

    @classmethod
    def get_answers_tuples(cls, question, sort_answer_by, profile):
        answers = question.get_answers_feed(sort_answer_by)
        answers_tuples = []
        for answer in answers:
            answers_tuples.append((answer, answer.profile_liked(profile), answer.profile_disliked(profile)))
        return answers_tuples

    @property
    def show_content(self):
        from django.utils.html import strip_tags
        return strip_tags(self.content)

    @classmethod
    def get_answers_by_date(cls):
        return cls.objects.order_by('-publish_date')


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    questions = models.ManyToManyField('Question', through='Question_Tag')

    def __str__(self):
        return self.tag_name

    # The function returnss all tags ordered by name tag.
    @classmethod
    def tags_feed(cls, search=''):
        return cls.objects.filter(tag_name__contains=search).order_by('tag_name')

    @classmethod
    def check_tag_array(cls, tags_array):
        if(len(tags_array) > 5):
            return False
        for tag in tags_array:
            if(len(tag) < 2 or len(tag) > 20):
                return False
        return True


class Question_Tag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_ID')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_ID')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'tag'], name='question_tag')
        ]

    def __str__(self):
        return f"{self.question}, Tag : {self.tag}"
