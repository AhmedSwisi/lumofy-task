from django.shortcuts import render
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import UploadedFile
from rest_framework.response import Response
from .serializers import UploadedFileSerializer, UserRegistrationSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny

class FileUploadListView(generics.ListCreateAPIView):
    serializer_class = UploadedFileSerializer
    parser_classes = [MultiPartParser,FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mime_type']

    def get_queryset(self):
        # Only return files uploaded by the logged-in user
        return UploadedFile.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        if not files:
            return Response({"error": "No files were uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        uploaded_files = []
        errors = {}
        for file in files:
            uploaded_file = UploadedFile(file = file, user=request.user)
            try:
                uploaded_file.full_clean()
                uploaded_file.save()
                uploaded_files.append(uploaded_file)
            except ValidationError as e:
                 errors[file.name] = e.message_dict

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(uploaded_files, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FileRetrieveView(generics.RetrieveAPIView):
    serializer_class = UploadedFileSerializer

    def get_queryset(self):
        return UploadedFile.objects.filter(user = self.request.user)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


