# timetable_app/models.py
from django.db import models
from django.utils import timezone

class TimetableSlot(models.Model):
    faculty1_file = models.FileField(upload_to='faculty1/', null=True, blank=True)
    faculty2_file = models.FileField(upload_to='faculty2/', null=True, blank=True)
    faculty3_file = models.FileField(upload_to='faculty3/', null=True, blank=True)
    other_field1 = models.CharField(max_length=100, default='')  # Add a default value
    other_field2 = models.CharField(max_length=100, default='')  # Add a default value
    timestamp_field = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Example: Set default values if the fields are not provided
        if not self.faculty1_file:
            self.faculty1_file = 'default_faculty1_file.pdf'

        # Example: Perform additional actions before saving
        # For instance, you might want to extract information from the uploaded files
        # or perform some processing based on other fields
        self.process_additional_data()

        super().save(*args, **kwargs)
    
    def process_additional_data(self):
        # Example: Perform additional processing based on other_field1
        if self.other_field1 == 'some_condition':
            # Add your logic here based on other_field1
            pass
    
        # Example: Perform additional processing based on other_field2
        if self.other_field2 == 'another_condition':
            # Add your logic here based on other_field2
            pass
    
        # Add more conditions based on other fields as needed
        # ...
        pass



class Faculty(models.Model):
    # Your Faculty model fields here
    name = models.CharField(max_length=255)

