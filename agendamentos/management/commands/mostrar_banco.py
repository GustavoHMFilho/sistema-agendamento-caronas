from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Mostra informacoes seguras sobre o banco usado pela aplicacao.'

    def handle(self, *args, **options):
        database = settings.DATABASES['default']
        self.stdout.write('Banco configurado:')
        self.stdout.write(f"ENGINE={database.get('ENGINE')}")
        self.stdout.write(f"HOST={database.get('HOST', '')}")
        self.stdout.write(f"PORT={database.get('PORT', '')}")
        self.stdout.write(f"NAME={database.get('NAME', '')}")
