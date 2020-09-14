from background_task import background
from apps.revista_cientifica import models
from django.conf import settings
import os


def delete_file(file: models.File):
    path = os.path.join(settings.BASE_DIR, file.file.name)
    os.remove(path)
    file.delete()


@background(schedule=10)
def delete_old_files():
    print('Doing Background not necessary files delete')
    newest_files = {}
    for file in models.File.objects.all():
        if file.article.end_date is not None:
            try:
                if newest_files[file.article.id].date > file.date:
                    delete_file(file)
                else:
                    delete_file(newest_files[file.article.id])
                    newest_files[file.article.id] = file
            except KeyError:
                newest_files[file.article.id] = file
