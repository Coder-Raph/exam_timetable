from django.core.management.base import BaseCommand
from timetable_app.timetable_generator import generate_timetable

class Command(BaseCommand):
    help = 'Generate a timetable and save it to the database'

    def handle(self, *args, **options):
        generated_timetable = generate_timetable()

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {len(generated_timetable)} timetable slots.'))
