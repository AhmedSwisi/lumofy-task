from django.core.exceptions import ValidationError
import mimetypes

def validate_file_size(file):
    max_size_mb  = 5
    mime_type, encoding = mimetypes.guess_type(file.name)
    video_mime_types = ['video/mp4', 'video/avi', 'video/mpeg', 'video/quicktime', 'video/x-ms-wmv']
    if mime_type in video_mime_types:
        max_size_mb = 25
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size exceeds {max_size_mb} MB limit for this file type")