import random
from typing import List
from rest_framework.authtoken.models import Token
from apps.revista_cientifica.models import *

NUMBER_OF_ARTICLES = 25
MCCs = [MCC(area=s, id=s) for s in [f'mcc {i}' for i in range(NUMBER_OF_ARTICLES)]]


def populate():
    for mcc in MCCs:
        mcc.save()

    username = 'miguelcalles'
    User.objects.create_user(username=username,
                             first_name='Miguel Angel',
                             last_name='Calles',
                             email=f'{username}@gmail.com',
                             password='adminrc1234.',
                             is_superuser=True
                             ).save()

    username = 'alejandroklever'
    User.objects.create_user(username=username,
                             first_name='Alejandro',
                             last_name='Klever',
                             email=f'{username}@gmail.com',
                             password='adminrc1234.',
                             is_superuser=True
                             ).save()

    username = 'yasmincisneros'
    User.objects.create_user(username=username,
                             first_name='Yasmin',
                             last_name='Cisneros',
                             email=f'{username}@gmail.com',
                             password='adminrc1234.',
                             is_superuser=True
                             ).save()

    username = 'luisibarra'
    User.objects.create_user(username=username,
                             first_name='Luis Ernesto',
                             last_name='Ibarra',
                             email=f'{username}@gmail.com',
                             password='qwer1234.'
                             ).save()

    username = 'luisdalmau'
    User.objects.create_user(username=username,
                             first_name='Luis Enrique',
                             last_name='Dalmau',
                             email=f'{username}@gmail.com',
                             password='qwer1234.',
                             ).save()

    username = 'lauratamayo'
    User.objects.create_user(username=username,
                             first_name='Laura',
                             last_name='Tamayo',
                             email=f'{username}@gmail.com',
                             password='qwer1234.'
                             ).save()

    username = 'jessygigato'
    User.objects.create_user(username=username,
                             first_name='Jessy',
                             last_name='Gigato',
                             email=f'{username}@gmail.com',
                             password='qwer1234.'
                             ).save()

    indexes: List[int] = []
    authors: List[Author] = []
    for i, user in enumerate(User.objects.all()):
        indexes.append(i)
        Token.objects.get_or_create(user=user)
        authors.append(Author(user=user, institution='Universidad de la Habana', orcid=i))
        authors[-1].save()

    for i in range(NUMBER_OF_ARTICLES):
        title = f'Article {i}'
        article = Article(title=title, mcc=MCCs[i], keywords=f'Foo {i}', evaluation='-')
        article.save()

        random.shuffle(indexes)
        for j in range(random.randrange(1, len(authors))):
            author = authors[indexes[j]]
            Participation(author=author, article=article, is_email_author=j == 0).save()
