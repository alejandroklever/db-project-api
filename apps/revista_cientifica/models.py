import os

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, null=False, blank=False)
    date = models.DateTimeField(default=now, blank=True)
    checked = models.BooleanField(default=False, null=False, blank=True)

    def __str__(self):
        return f'destiny: {self.user}\n content: {self.content}'


class MCC(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    area = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id}: '+str(self.area)


class Article(models.Model):
    title: models.CharField = models.CharField(max_length=150, blank=False)
    mcc = models.ForeignKey(MCC, on_delete=models.CASCADE)
    keywords = models.CharField(null=True, blank=True, max_length=300)

    evaluation = models.CharField(blank=True, null=True, max_length=100)
    start_date = models.DateTimeField(blank=True, default=now)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.title)


class File(models.Model):
    file = models.FileField(null=False, upload_to='apps/revista_cientifica/media', blank=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=150)
    date = models.DateTimeField(blank=True, default=now)

    def __str__(self):
        return f'{self.file_name} from {self.article}'


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200, null=True, blank=True)
    articles = models.ManyToManyField(Article, through='Participation')
    ORCID = models.BigIntegerField(unique=True, null=True, blank=False, default=1000000000000000)

    def __str__(self):
        return f'{self.user}'


class Participation(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_email_author = models.BooleanField(default=False)

    class Meta:
        unique_together = ['author', 'article']

    def __str__(self):
        return f'{self.author} in {self.article}'


class Referee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    speciality = models.ManyToManyField(MCC)
    articles = models.ManyToManyField(Article, through='ArticleInReview')

    def __str__(self):
        return f'{self.user}'


class ArticleInReview(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE)
    evaluation = models.CharField(default='', blank=True, null=True, max_length=100)
    state = models.CharField(default='', max_length=100)

    round = models.IntegerField(null=True, blank=True, default=1)
    description = models.FileField(null=True, blank=True)

    start_date = models.DateTimeField(default=now, blank=True)
    final_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['referee', 'article', 'round']

    def __str__(self):
        return f'{self.referee} Reviewing {self.article} in round {self.round}'
