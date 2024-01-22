from django.urls import path
from django.views import generic
from bus_schedule.bus.views import ScheduleCreateView, schedule_show_view

urlpatterns = [
    path("upload/", ScheduleCreateView.as_view(), name="upload"),
    path("schedule/", schedule_show_view, name="schedule"),

]
