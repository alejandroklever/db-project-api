from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, null=False, blank=False)
    ref = models.CharField(max_length=300, null=False, blank=False)
    date = models.DateTimeField(default=now, null=False, blank=True)

    def __str__(self):
        return f'{self.content} para {self.user}'


class MCC(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    area = models.CharField(max_length=100)


class ArticleEvaluation(models.Model):
    evaluation = models.CharField(max_length=150, blank=False)


class Article(models.Model):
    title = models.CharField(max_length=150, blank=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    keywords = models.CharField(null=True, blank=True, max_length=300)
    mcc = models.ForeignKey(MCC, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(ArticleEvaluation, on_delete=models.CASCADE, blank=True, null=True)


class File(models.Model):
    file = models.FileField(null=False, upload_to='media/', blank=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=150)
    date = models.DateTimeField(default=now, blank=True, null=True)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200, null=True, blank=True)
    articles = models.ManyToManyField(Article, through='Participation')
    ORCID = models.IntegerField(unique=True, null=True, blank=False)

    def __str__(self):
        return f'{self.user}'


class Participation(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_email_author = models.BooleanField(default=False)

    class Meta:
        unique_together = ['author', 'article']


class State(models.Model):
    state = models.CharField(max_length=50)


class Evaluation(models.Model):
    evaluation = models.CharField(max_length=50)


class Referee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    speciality = models.ManyToManyField(MCC)
    articles = models.ManyToManyField(Article, through='ArticleInReview')


class ArticleInReview(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, default=1)
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=3)

    round = models.IntegerField(null=True, blank=True, default=1)
    description = models.FileField(null=True, blank=True)

    start_date = models.DateField(null=True)
    final_date = models.DateField(null=True, blank=True)
