from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from ...randomizer.logic.main import VERSION
from ...randomizer.models import Seed


class Command(BaseCommand):
    help = 'Remove old seeds that are from previous versions, or at least 6 months old.'

    def handle(self, *args, **options):
        count = 0

        for seed in Seed.objects.filter(~Q(version=VERSION)):
            with transaction.atomic():
                seed.patch_set.all().delete()
                seed.delete()
                count += 1

        self.stdout.write("Cleared {} old seeds".format(count))
