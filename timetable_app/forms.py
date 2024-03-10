# timetable_app/forms.py
from django import forms
from .models import TimetableSlot

class TimetableSlotForm(forms.ModelForm):
    class Meta:
        model = TimetableSlot
        fields = '__all__'
        # Add any additional form fields and configurations here

    def clean_faculty_file(self):
        faculty_file = self.cleaned_data.get('faculty_file')
        if faculty_file:
            # Validate file types if needed
            valid_file_types = ['.xls', '.xlsx']
            if not any(faculty_file.name.lower().endswith(file_type) for file_type in valid_file_types):
                raise forms.ValidationError('Invalid file type. Supported file types are .xls, .xlsx.')
        return faculty_file
