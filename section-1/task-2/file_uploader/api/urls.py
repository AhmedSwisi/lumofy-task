from django.urls import path
from .views import FileUploadListView, FileRetrieveView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('files/', FileUploadListView.as_view(), name='file-upload-list'),
    path('files/<int:pk>',FileRetrieveView.as_view(),name='file-details')
]