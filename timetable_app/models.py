from django.db import models
from django.utils import timezone

class GeneratedTimetable(models.Model):
    file = models.FileField(upload_to='generated_timetables/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} - {self.created_at}"

class Rule(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(default=100)  # Change 100 to your desired default value
    rules = models.ManyToManyField(Rule, blank=True)

    def __str__(self):
        return self.name

class TimetableSlot(models.Model):
    day = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    duration = models.DurationField(null=True)
    faculty = models.CharField(max_length=255, default='Unknown')
    course_file = models.FileField(upload_to='course_files/', null=True, blank=True)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, null=True, blank=True)
    timestamp_field = models.DateTimeField(default=timezone.now)
    rules = models.ManyToManyField('Rule', blank=True)

    def __str__(self):
        return f'{self.day} - {self.duration} - {self.course_file.name} - {self.venue} - {self.faculty}'
