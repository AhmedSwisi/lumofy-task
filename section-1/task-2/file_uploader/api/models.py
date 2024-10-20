from django.db import models
import mimetypes
from .validators import validate_file_size
import os
from django.conf import settings

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/',validators=[validate_file_size])
    mime_type = models.CharField(max_length=100, editable=False)
    file_extension = models.CharField(max_length=50,editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        file_path = self.file.name
        self.file_extension = os.path.splitext(self.file.name)[1][1:].lower()
        mime_type, encoding = mimetypes.guess_type(file_path)
        self.mime_type = mime_type or 'application/octet-stream'
        super().save(*args,**kwargs)
