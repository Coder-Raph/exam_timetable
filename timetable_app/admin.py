# timetable_app/admin.py
from django.contrib import admin
from django.urls import path
from .models import TimetableSlot
from .forms import TimetableSlotForm 

class TimetableSlotAdmin(admin.ModelAdmin):
    form = TimetableSlotForm

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add_timetable_slot/', self.admin_site.admin_view(self.add_timetable_slot), name='add_timetable_slot'),
        ]
        return custom_urls + urls

    def add_timetable_slot(self, request):
        if request.method == 'POST':
            form = TimetableUploadForm(request.POST, request.FILES)

            if form.is_valid():
                # Retrieve uploaded file
                faculty_file = request.FILES.get('faculty_file')

                # Process the uploaded Excel file
                process_excel_file(faculty_file)

                # Redirect back to the Timetable Slot change list after processing
                return redirect('admin:timetable_app_timetableslot_changelist')

        else:
            # Display the upload form
            form = TimetableUploadForm()

        context = {
            'form': form,
            'opts': self.model._meta,
            'title': 'Add Timetable Slot',
            'site_header': self.admin_site.site_header,
            'site_title': self.admin_site.site_title,
            'has_permission': self.has_add_permission(request),
        }

        return render(request, 'admin/timetable_app/timetableslot/add_timetable_slot.html', context)

# Register your model with the custom admin class
admin.site.register(TimetableSlot, TimetableSlotAdmin)