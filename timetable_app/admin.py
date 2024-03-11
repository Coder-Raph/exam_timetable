# your_app_name/admin.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import TimetableSlot, Venue, GeneratedTimetable
from .forms import TimetableSlotForm, CommonCourseForm
from .views import process_excel_file

def generate_timetable(modeladmin, request, queryset):
    for obj in queryset:
        try:
            process_excel_file(obj.faculty1_file, faculty_name=obj.faculty_name)
        except AttributeError:
            pass

    modeladmin.message_user(request, "Timetable generation complete")

generate_timetable.short_description = "Generate timetable from uploaded files"

class VenueAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(GeneratedTimetable)
class GeneratedTimetableAdmin(admin.ModelAdmin):
    list_display = ('file', 'created_at', 'display_related_slots')
    readonly_fields = ('file', 'created_at')

    def display_related_slots(self, obj):
        # Fetch and display related TimetableSlot records
        slots = TimetableSlot.objects.filter(generated_timetable=obj)
        return ', '.join([str(slot) for slot in slots])

    display_related_slots.short_description = 'Related Timetable Slots'

@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    form = TimetableSlotForm
    actions = [generate_timetable]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add_timetable_slot/', self.admin_site.admin_view(self.add_timetable_slot), name='add_timetable_slot'),
        ]
        return custom_urls + urls

    def add_timetable_slot(self, request):
        if request.method == 'POST':
            form = TimetableSlotForm(request.POST, request.FILES)

            if form.is_valid():
                faculty_file = request.FILES.get('faculty_file')
                try:
                    process_excel_file(faculty_file, faculty_name=form.cleaned_data['faculty_name'])
                except AttributeError:
                    pass
                return redirect('admin:your_app_name_timetableslot_changelist')

        else:
            form = TimetableSlotForm()

        context = {
            'form': form,
            'opts': self.model._meta,
            'title': 'GCTU TIMETABLE GENERATOR',
            'site_header': self.admin_site.site_header,
            'site_title': self.admin_site.site_title,
            'has_permission': self.has_add_permission(request),
        }

        return render(request, 'admin/your_app_name/timetableslot/add_timetable_slot.html', context)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name',)

    
# Register your model with the custom admin class
# admin.site.register(TimetableSlot, TimetableSlotAdmin)
# admin.site.register(Venue, VenueAdmin)
