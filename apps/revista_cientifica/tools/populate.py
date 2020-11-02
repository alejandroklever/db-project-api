import random
from typing import List
from rest_framework.authtoken.models import Token
from apps.revista_cientifica.models import *

users = [
    {
        'username': 'alejandroklever',
        'first_name': 'Alejandro',
        'last_name': 'Klever',
        'email': 'alejandroklever@gmail.com',
        'password': 'qwer1234.',
        'is_superuser': True,
        'author': {
            'orcid': 1,
            'institution': 'Universidad De La Habana'
        },
        'referee': {
            'speciality': [
                'Computación',
                'Matemáticas',
            ]
        }
    },
    {
        'username': 'miguelcalles',
        'first_name': 'Miguel Angel',
        'last_name': 'Gonzalez',
        'email': 'miguelcalles@gmail.com',
        'password': 'qwer1234.',
        'is_superuser': True,
        'author': {
            'orcid': 2,
            'institution': 'Universidad De La Habana'
        },
        'referee': None
    },
    {
        'username': 'yasmincisneros',
        'first_name': 'Yasmin',
        'last_name': 'Cisneros',
        'email': 'yasmincisneros@gmail.com',
        'password': 'qwer1234.',
        'is_superuser': True,
        'author': {
            'orcid': 3,
            'institution': 'Universidad De La Habana'
        },
        'referee': None
    },
    {
        'username': 'luisibarra',
        'first_name': 'Luis Ernesto',
        'last_name': 'Ibarra',
        'email': 'luisibarra@gmail.com',
        'password': 'qwer1234.',
        'is_superuser': False,
        'author': {
            'orcid': 4,
            'institution': 'Universidad De La Habana'
        },
        'referee': None
    },
    {
        'username': 'luisdalmau',
        'first_name': 'Luis Enrique',
        'last_name': 'Dalmau',
        'email': 'luisdalmau@gmail.com',
        'password': 'qwer1234.',
        'is_superuser': False,
        'author': {
            'orcid': 5,
            'institution': 'Universidad De La Habana'
        },
        'referee': None
    },
    {
        'username': 'lauratamayo',
        'first_name': 'Laura',
        'last_name': 'Tamayo',
        'email': 'lauratamayo@gmail.com',
        'password': 'qwer1234.',
        'is_superuser': False,
        'author': {
            'orcid': 6,
            'institution': 'Universidad De La Habana'
        },
        'referee': None
    },
    {
        'username': 'jessygigato',
        'first_name': 'Jessy',
        'last_name': 'Gigato',
        'email': 'jessygigato@gmail.com',
        'password': 'qwer1234.',
        'is_superuser': False,
        'author': {
            'orcid': 7,
            'institution': 'Universidad De La Habana'
        },
        'referee': None
    },
]

titles = [
    'Fourier y Detección De Bordes en Imágenes',
    'FFT y optimización competitiva',
    'Corte de centroides en grafos conexos',
    'Aproximación a la inferencia de tipos a través de digrafos',
    'Detección de privacidad en redes sociales',

    'Spotify en tiempos de Covid-19',
    'Autogoal',
    'Generación automática de artículos periodísticos sobre la Serie Nacional de Pelota',
    'PyJapt: Just Another Parsing Tool Written in Python',
    'Nivel de adquisición de la famalia cubana',

    'Generación automaticas de perfiles en redes sociales',
    'Creación de un modelo 3D de un corazón a partir de radiografías',
    'Godot ML Agents',
    'Generación de mapas bidimencionales usando Perlin Noise',
    'Flocking Optimizado',

    'Compresión de datos',
    'Recaudación descentralizada de información',
    'Revisor de encuestas automaticas. Un trabajo de análisis de imágenes',
    'Proyección de menus usando realida aumentada',
    'Generación automática de memes',

    'Algoritmos de Hash',
    'Formas no recursivas de DFS en Python',
    'Análisis y comparación entre Angular, React y Vue',
    'Rutas de avión y geodesicas',
    'Análisis de felicidad de países por el índice de libertad económica'
]

MCCs = [
    MCC(area=s, id=s) for s in
    [f'mcc {i}' for i in range(len(titles) - 2)] + ['Computación', 'Matemáticas']]


def populate():
    for mcc in MCCs:
        mcc.save()

    indexes: List[int] = []
    authors: List[Author] = []
    for i, user in enumerate(users):
        indexes.append(i)
        new_user = User.objects.create_user(username=user['username'],
                                            first_name=user['first_name'],
                                            last_name=user['last_name'],
                                            email=user['email'],
                                            password=user['password'],
                                            is_superuser=user['is_superuser'])
        new_user.save()
        Token.objects.get_or_create(user=new_user)
        authors.append(Author(user=new_user,
                              institution=user['author']['institution'],
                              orcid=user['author']['orcid']))
        authors[-1].save()
        if user['referee'] is not None:
            referee = Referee(user=new_user)
            referee.save()
            for speciality in user['referee']['speciality']:
                referee.specialities.add(MCC.objects.get(id=speciality))

    for i, title in enumerate(titles):
        article = Article(title=title, mcc=MCCs[i], keywords=f'Foo {i}', evaluation='-')
        article.save()

        random.shuffle(indexes)
        for j in range(random.randrange(1, len(authors))):
            author = authors[indexes[j]]
            Participation(author=author, article=article, is_email_author=j == 0).save()

    alejandroklever = User.objects.get(username='alejandroklever')
    articles_in_review = Article.objects.exclude(author__user=alejandroklever)
    for article in articles_in_review:
        ArticleInReview(article=article, referee=Referee.objects.get(user=alejandroklever), round=1).save()
