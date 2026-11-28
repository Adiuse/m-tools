from time import sleep

from django.core.management.base import BaseCommand

from core.exports import process_one


class Command(BaseCommand):
    help = "Process pending executive exports in the application worker."

    def add_arguments(self, parser):
        parser.add_argument("--watch", action="store_true")

    def handle(self, *args, **options):
        if options["watch"]:
            while True:
                if not process_one():
                    sleep(1)
        else:
            for _ in range(20):
                if not process_one():
                    break
