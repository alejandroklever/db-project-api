from apps.revista_cientifica.models import *


def populate():
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

    for i, user in enumerate(User.objects.all()):
        Author(user=user, institution='Universidad de la Habana', ORCID=i).save()
