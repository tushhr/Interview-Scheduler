from django.urls import path, re_path

from . import views

app_name = 'scheduler'

urlpatterns = [
    path('', views.index, name = "index"),
    path('schedule', views.schedule_interview, name = "schedule_interview"),
    path('timeline', views.timeline, name = "timeline"),
    path(r'^/<int:interview_id>/$', views.interview_page, name = "interview_page"),
    path('edit', views.edit_interview, name = "edit_interview")
]