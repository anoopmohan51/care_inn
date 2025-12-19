from django.urls import path
from staticfiles_api.views.static_files.static_files import *
urlpatterns = [
    path('static-files',StaticFilesCreateView.as_view()),
    path('static-files/<uuid:pk>',StaticFilesDetailView.as_view()),
]