from django.urls import path
from .views import timetable, add_slot, root_view, TimetableSlotCreateView, download_timetable_csv_view


urlpatterns = [
    path('download_timetable_csv/', download_timetable_csv_view, name='download_timetable_csv'),
    path('timetable/', timetable, name='timetable'),
    path('add_slot/', TimetableSlotCreateView.as_view(), name='add_slot'),    path('root_view/', root_view, name='root_view'),
    path('', timetable),  # Redirect to the timetable view for the empty path
]
