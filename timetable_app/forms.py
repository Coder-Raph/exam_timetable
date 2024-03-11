from django import forms
from django.forms import ModelForm
from .models import TimetableSlot

class CommonCourseForm(forms.Form):
    # Define the fields for the CommonCourse form
    course_name = forms.CharField(max_length=100)
    # Add more fields as needed

class TimetableSlotForm(forms.ModelForm):
    class Meta:
        model = TimetableSlot
        fields = ['day', 'start_time', 'end_time', 'duration', 'faculty', 'course_file', 'venue']

    def clean_faculty_file(self):
        faculty_file = self.cleaned_data.get('faculty_file')
        if faculty_file:
            # Validate file types if needed
            valid_file_types = ['.xls', '.xlsx']
            if not any(faculty_file.name.lower().endswith(file_type) for file_type in valid_file_types):
                raise forms.ValidationError('Invalid file type. Supported file types are .xls, .xlsx.')
        return faculty_file
