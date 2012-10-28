from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_models


class Command(BaseCommand):
    help = 'Print all project models and their count'

    def handle(self, *args, **options):
        for Model in get_models():
            count = Model.objects.count()
            mname = Model.__module__ + '.' + Model.__name__
            line = '%s: %s\n' % (mname, count)
            self.stdout.write(line)
            self.stderr.write('error: ' + line)
