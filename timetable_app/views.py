# timetable_app/views.py
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import TimetableSlotForm
from .models import TimetableSlot, Venue, GeneratedTimetable
from django.http import HttpResponse
import pandas as pd
from openpyxl import Workbook
from django.conf import settings
from django.db import transaction

def generate_timetable_file():
    # Your actual logic for generating the timetable file should be added here
    # For now, let's create a simple timetable file using openpyxl as a placeholder

    # Create a workbook and add a sheet
    workbook = Workbook()
    sheet = workbook.active

    # Add some data to the sheet (replace this with your actual timetable data)
    sheet.append(['Day', 'Time', 'Course', 'Room'])

    # Example data
    timetable_data = [
        ['Monday', '10:00 AM', 'Math', 'Room A'],
        ['Tuesday', '02:00 PM', 'Physics', 'Room B'],
        # Add more rows as needed
    ]

    for row in timetable_data:
        sheet.append(row)

    # Generate a unique filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f'timetable_generated_{timestamp}.xlsx'
    file_path = os.path.join('/path/to/media/', file_name)

    # Save the workbook to the specified file path
    workbook.save(file_path)

    # Save information about the generated timetable
    generated_timetable = GeneratedTimetable.objects.create(file=file_path)
    generated_timetable.save()

    return file_path

def process_excel_file(faculty_file, faculty_name):
    # Process the Excel file using pandas
    df = pd.read_excel(faculty_file)

    # Create a workbook and add a sheet for each faculty
    workbook = Workbook()
    writer = pd.ExcelWriter(os.path.join(settings.MEDIA_ROOT, 'timetable_generated.xlsx'), engine='openpyxl')
    writer.book = workbook
    writer.sheets = {ws.title: ws for ws in workbook.worksheets}

    # Create a separate sheet for each faculty
    df_dict = {}
    for faculty in df['Faculty'].unique():
        faculty_df = df[df['Faculty'] == faculty]
        df_dict[faculty] = faculty_df
        faculty_df.to_excel(writer, index=False, sheet_name=faculty)

    # Process common courses
    common_courses = set()
    for faculty, faculty_df in df_dict.items():
        common_courses.intersection_update(faculty_df['Course']) if common_courses else common_courses.update(
            set(faculty_df['Course']))

    # Write common courses on the same sheet
    if common_courses:
        common_courses_df = pd.DataFrame()
        for course in common_courses:
            common_courses_df = pd.concat([common_courses_df, df[df['Course'] == course]])

        common_courses_df.to_excel(writer, index=False, sheet_name='CommonCourses')

    # Add a sheet for weekend courses
    weekend_courses = df[df['Day'].isin(['Saturday', 'Sunday'])]
    weekend_courses.to_excel(writer, index=False, sheet_name='WeekendCourses')

    writer.save()

    # Save the data to the database
    generated_file_path = os.path.join(settings.MEDIA_ROOT, 'timetable_generated.xlsx')

    # Clear existing timetable slots for the given faculty
    TimetableSlot.objects.filter(faculty=faculty_name).delete()

    for index, row in df.iterrows():
        timetable_slot = TimetableSlot.objects.create(
            day=row['Day'],
            time=row['Time'],
            course=row['Course'],
            room=row['Room'],  # Assuming 'Room' in the Excel file corresponds to 'Venue' in the model
            faculty=faculty_name,
        )

        # Your logic for setting venues and applying rules here...
        apply_rules_and_set_venues(timetable_slot)

    # Save the generated timetable file information in GeneratedTimetable model
    generated_timetable = GeneratedTimetable.objects.create(file=generated_file_path)

    return generated_file_path

def apply_rules_and_set_venues(timetable_slot):
    # Example rules:
    # Rule 1: Avoid scheduling the same course at the same time on different days
    conflicting_slots = TimetableSlot.objects.filter(
        course=timetable_slot.course,
        time=timetable_slot.time,
    ).exclude(day=timetable_slot.day)

    if conflicting_slots.exists():
        # Implement your resolution strategy here (e.g., reschedule, notify, etc.)
        print(f"Conflict detected for course {timetable_slot.course} at {timetable_slot.time} on {timetable_slot.day}")

    # Rule 2: Assign venues based on availability
    available_venues = Venue.objects.filter(is_available=True)
    if available_venues.exists():
        # Assign the first available venue for simplicity (you might have a more sophisticated logic)
        assigned_venue = available_venues.first()
        timetable_slot.room = assigned_venue.name
        assigned_venue.is_available = False  # Mark the venue as unavailable
        assigned_venue.save()
    else:
        # Handle the case when there are no available venues
        print("No available venues for assignment.")

    # Save the updated timetable slot
    timetable_slot.save()
def generate_and_download_timetable():
    # Placeholder logic for generating the timetable file
    # Your actual logic for generating the timetable file should be added here
    # For now, let's return a placeholder path
    return os.path.join(settings.MEDIA_ROOT, 'timetable_generated.xlsx')


def download_timetable_csv_view(request):
    # Fetch timetable data from the database
    timetable_data = TimetableSlot.objects.values('day', 'time', 'course', 'room', 'faculty')

    # Convert queryset to CSV content
    csv_content = "Day,Time,Course,Room,Faculty\n"
    for entry in timetable_data:
        csv_content += f"{entry['day']},{entry['time']},{entry['course']},{entry['room']},{entry['faculty']}\n"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="timetable.csv"'
    response.write(csv_content)

    return response


def timetable(request):
    # Use the generate_and_download_timetable function to get the file path
    file_path = generate_and_download_timetable()
    return render(request, 'timetable_app/download_timetable.html', {'file_path': file_path})


class TimetableSlotCreateView(CreateView):
    model = TimetableSlot
    form_class = TimetableSlotForm
    template_name = 'your_template_name.html'  # Change 'your_template_name.html' to your actual template name
    success_url = reverse_lazy('timetable')  # Change 'timetable' to the name of your timetable view


def home(request):
    return render(request, 'timetable_app/home.html')


def add_slot(request):
    if request.method == 'POST':
        form = TimetableSlotForm(request.POST, request.FILES)

        if form.is_valid():
            faculty_file = request.FILES.get('faculty_file')

            valid_file_types = ['.xls', '.xlsx']
            if faculty_file and not any(faculty_file.name.lower().endswith(file_type) for file_type in valid_file_types):
                messages.error(request, 'Invalid file type. Supported file types are .xls, .xlsx.')
                return render(request, 'timetable_app/add_slot.html', {'form': form})

            # Process the uploaded Excel file
            process_excel_file(faculty_file, faculty_name=form.cleaned_data['faculty'])  # Assuming you have a 'faculty' field in your form

            return redirect('timetable')  # Assuming 'timetable' is the name of the view you want to redirect to
    else:
        form = TimetableSlotForm()

    return render(request, 'timetable_app/add_slot.html', {'form': form})
