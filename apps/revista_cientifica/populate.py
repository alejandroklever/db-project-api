import random

from apps.revista_cientifica.models import *

MCCs = [MCC(area=s, id=s) for s in [f'mcc {i}' for i in range(25)]]


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

    indexes = []
    for i, user in enumerate(User.objects.all()):
        indexes.append(i)
        Author(user=user, institution='Universidad de la Habana', ORCID=i).save()

    for i in range(25):
        title = f'Article {i}'
        article = Article(title=title, mcc=MCCs[i], keywords=f'Foo {i}', evaluation='-')
        article.save()

        authors = list(Author.objects.all())
        random.shuffle(indexes)

        for j in range(3):
            author = authors[indexes[j]]
            Participation(author=author, article=article).save()
