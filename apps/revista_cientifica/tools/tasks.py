import os

from background_task import background
from django.conf import settings

from apps.revista_cientifica.models import File


def delete_file(file: File):
    path = os.path.join(settings.BASE_DIR, file.file.name)
    os.remove(path)
    file.delete()


@background(schedule=10)
def delete_old_files():
    print('Doing Background not necessary files delete')
    newest_files = {}
    for file in File.objects.all():
        if file.article.end_date is not None:
            try:
                if newest_files[file.article.id].date > file.date:
                    delete_file(file)
                else:
                    delete_file(newest_files[file.article.id])
                    newest_files[file.article.id] = file
            except KeyError:
                newest_files[file.article.id] = file

# Run Once Only for Initialize Tasks
# if len(Task.objects.all()) == 0:
#     delete_old_files(repeat=Task.DAILY)
