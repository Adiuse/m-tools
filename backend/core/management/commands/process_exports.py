from time import monotonic, sleep

from django.core.management.base import BaseCommand

from core.exports import process_one, prune_expired


class Command(BaseCommand):
    help = "Process pending executive exports in the application worker."

    def add_arguments(self, parser):
        parser.add_argument("--watch", action="store_true")

    def handle(self, *args, **options):
        prune_expired()
        if options["watch"]:
            next_sweep = monotonic() + 60
            while True:
                if monotonic() >= next_sweep:
                    prune_expired()
                    next_sweep = monotonic() + 60
                if not process_one():
                    sleep(1)
        else:
            for _ in range(20):
                if not process_one():
                    break
