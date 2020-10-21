from django.contrib import admin
from .models import Article, ArticleInReview, Author, Referee, Participation, MCC, Notification, File

admin.site.register(Author)
admin.site.register(Referee)
admin.site.register(Article)
admin.site.register(ArticleInReview)
admin.site.register(Participation)
admin.site.register(MCC)
admin.site.register(Notification)
admin.site.register(File)
