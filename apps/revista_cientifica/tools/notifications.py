from apps.revista_cientifica import models


class Notifier:
    @staticmethod
    def notify_user(user: models.User, msg: str):
        notification = models.Notification(user=user, content=msg)
        notification.save()

    def notify_super_users(self, msg: str):
        for user in models.User.objects.filter(is_superuser=True):
            self.notify_user(user, msg)

    def notify_article_authors(self, article: models.Article, msg: str):
        for participation in models.Participation.objects.filter(article=article):
            self.notify_user(participation.author.user, msg)

    def notify_article_email_author(self, article: models.Article, msg: str):
        for participation in models.Participation.objects.filter(article=article, is_email_author=True):
            self.notify_user(participation.author.user, msg)

    def notify_article_referees(self, article: models.Article, msg: str):
        for review in models.ArticleInReview.objects.filter(article=article):
            self.notify_user(review.referee.user, msg)


class NotificationMaker:
    notifier = Notifier()

    def new_article(self, id_article):
        article = models.Article.objects.get(id=id_article)
        authors = self.__get_authors_for_article(article)
        self.notifier.notify_super_users(f'''New Article has been added title: "{article.title}"''')

    def updated_article(self, id_article, previous_evaluation):
        article = models.Article.objects.get(id=id_article)
        authors = self.__get_authors_for_article(article)
        text_reject = f'''The reports of the paper {article.title}{authors} have been sent.
Unfortunately, the paper cannot be accepted. Hopping to receive a new contribution from you soon'''
        text_chages_needed = f'''The reports of the paper {article.title}{authors} have been sent.
As you can see, a revised version shall be sent. We expect your answer within a month'''
        text_accept = f'''We are glad to communicate you that the paper {article.title}{authors} 
has been accepted for publication in "Revista Investigación Operacional".
The editor will contact you soon for the paper proofs of your article '''
        if previous_evaluation == '':
            if article.evaluation == 'Rechazado':
                self.notifier.notify_article_email_author(article, text_reject)
            if article.evaluation == 'Aprobado Con Cambios':
                self.notifier.notify_article_email_author(article, text_chages_needed)
            if article.evaluation == 'Aprobado':
                self.notifier.notify_article_email_author(article, text_accept)

    def new_file(self, id_article):
        article = models.Article.objects.get(id=id_article)
        authors = self.__get_authors_for_article(article)
        text = f'''File versions for article: "{article.title}"{authors} have been updated'''
        self.notifier.notify_super_users(text)
        self.notifier.notify_article_referees(article, text)

    def new_participation(self, id_participation):
        participation = models.Participation.objects.get(id=id_participation)
        article = participation.article
        author = participation.author.user
        self.notifier.notify_user(author, f'''We have received the paper "{article.title}". 
We are sending to the referees for their consideration.
We expect their response in 3 months.''')

    def new_review(self, id_review):
        review = models.ArticleInReview.objects.get(id=id_review)
        article = review.article
        authors = self.__get_authors_for_article(article)
        text_assigment = f'''You have been assigned as referee of the paper "{article.title}"{authors}.
 We expect your referee report in 3 months.'''
        text_first_petition = f'''You been asked to revise the paper "{article.title}"{authors}.
 Please let us know as soon as possible if you agree.
 We expect your referee report in 3 months.'''
        text_follow_petition = f'''Herein I am sending you the revised version of the paper "{article.title}"{authors}.
 Please, let us know if you agree to revise it.
 We expect your report within 3 months.'''
        if review.state == 'Esperando Respuesta':
            if review.round == 1:
                self.notifier.notify_user(review.referee.user, text_first_petition)
            else:
                self.notifier.notify_user(review.referee.user, text_follow_petition)
        if review.state == 'Calificando':
            self.notifier.notify_user(review.referee.user, text_assigment)

    def updated_review(self, id_review, previous_state):
        review = models.ArticleInReview.objects.get(id=id_review)
        referee = review.referee.user
        article = review.article
        authors = self.__get_authors_for_article(article)
        text_update = f'''Referee: {review.referee} has updated the review state for article: "{article.title}"{authors}'''
        text_thanks = f'''Herein I am thanking you for acting as referee of the paper "{article.title}"{authors}.'''
        self.notifier.notify_super_users(text_update)
        if previous_state == 'Esperando Respuesta':
            if review.state == 'Calificando':
                self.notifier.notify_user(referee, text_thanks)

    @staticmethod
    def __get_authors_for_article(article: models.Article):
        authors = [str(participation.author) for participation in models.Participation.objects.filter(article=article)]
        if len(authors) == 0:
            return ''
        authors_str = ' of ' + authors[0]
        for author in authors[1:]:
            authors_str += f'; {author}'
        return authors_str
