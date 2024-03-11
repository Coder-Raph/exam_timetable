# timetable_app/urls.py

from django.urls import path
from .views import timetable, TimetableSlotCreateView, download_timetable_csv_view, download_timetable

urlpatterns = [
    path('download_generated_timetable/', download_generated_timetable, name='download_generated_timetable'),
    path('timetable/', timetable, name='timetable'),
    path('add_slot/', TimetableSlotCreateView.as_view(), name='add_slot'),
    path('download_timetable/', download_timetable, name='download_timetable'),  # Add this line
    
]
