import random
from typing import List

from apps.revista_cientifica.models import *

NUMBER_OF_ARTICLES = 25
MCCs = [MCC(area=s, id=s) for s in [f'mcc {i}' for i in range(NUMBER_OF_ARTICLES)]]


def populate():
    for mcc in MCCs:
        mcc.save()

    User(username='miguelcalles',
         first_name='Miguel Angel',
         last_name='Calles',
         password='adminrc1234.',
         is_superuser=True
         ).save()

    User(username='alejandroklever',
         first_name='Alejandro',
         last_name='Klever',
         password='adminrc1234.',
         is_superuser=True
         ).save()

    User(username='yasmincisneros',
         first_name='Yasmin',
         last_name='Cisneros',
         password='adminrc1234.',
         is_superuser=True
         ).save()

    User(username='luisibarra',
         first_name='Luis Ernesto',
         last_name='Ibarra',
         password='qwer1234.'
         ).save()

    User(username='luisdalmau',
         first_name='Luis Enrique',
         last_name='Dalmau',
         password='qwer1234.',
         ).save()

    User(username='lauratamayo',
         first_name='Laura',
         last_name='Tamayo',
         password='qwer1234.'
         ).save()

    User(username='jessygigato',
         first_name='Jessy',
         last_name='Gigato',
         password='qwer1234.'
         ).save()

    indexes: List[int] = []
    authors: List[Author] = []
    for i, user in enumerate(User.objects.all()):
        indexes.append(i)
        authors.append(Author(user=user, institution='Universidad de la Habana', ORCID=i))
        authors[-1].save()

    for i in range(NUMBER_OF_ARTICLES):
        title = f'Article {i}'
        article = Article(title=title, mcc=MCCs[i], keywords=f'Foo {i}', evaluation='-')
        article.save()

        random.shuffle(indexes)
        for j in range(random.randrange(1, len(authors))):
            author = authors[indexes[j]]
            Participation(author=author, article=article).save()
