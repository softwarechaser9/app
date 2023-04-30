from django.urls import path

from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('display_line/<int:line_number>/<str:language>/', views.display_line, name='display_line'),
    path('skip_line/<int:line_number>/<int:lines_to_skip>/<str:language>/', views.skip_line, name='skip_line'),

]
