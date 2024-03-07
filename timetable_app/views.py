# timetable_app/views.py
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import TimetableSlot
from .forms import TimetableSlotForm  # Make sure this import matches the form's actual name

class TimetableSlotCreateView(CreateView):
    model = TimetableSlot
    form_class = TimetableSlotForm
    template_name = 'timetable_app/add_slot.html'
    success_url = reverse_lazy('timetable')  # Redirect to the timetable page after successful submission

def process_excel_file(file, faculty_name):
    # Add your logic to process the Excel file here
    # For example, you can use pandas to read the Excel file
    df = pd.read_excel(file)

    # Process the data and save it to the database
    for index, row in df.iterrows():
        TimetableSlot.objects.create(
            day=row['Day'],
            time=row['Time'],
            course=row['Course'],
            room=row['Room'],
            faculty=faculty_name,
        )

def timetable(request):
    slots = TimetableSlot.objects.all()
    return render(request, 'timetable_app/timetable.html', {'slots': slots})

def root_view(request):
    return render(request, 'timetable_app/root.html')

def add_slot(request):
    if request.method == 'POST':
        form = TimetableUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Retrieve uploaded files
            faculty_file = request.FILES.get('faculty_file')

            # Validate file types if needed
            valid_file_types = ['.xls', '.xlsx']
            if faculty_file and not any(faculty_file.name.lower().endswith(file_type) for file_type in valid_file_types):
                messages.error(request, 'Invalid file type. Supported file types are .xls, .xlsx.')
                return render(request, 'timetable_app/add_slot.html', {'form': form})

            # Process the uploaded Excel file
            process_excel_file(faculty_file, faculty_name='Faculty Name')  # Provide the actual faculty name

            # Redirect to the timetable view after processing
            return redirect('timetable')

    else:
        # Display the upload form
        form = TimetableUploadForm()

    return render(request, 'timetable_app/add_slot.html', {'form': form})

def add_timetable_slot(request):
    # Your implementation for handling the add timetable slot view
    # ...

    return render(request, 'timetable_app/your_template.html', context)
