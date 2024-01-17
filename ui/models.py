# # models.py
# from django.db import models
from djongo import models

class UserProfile(models.Model):
    userName = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
# myapp/models.py

from django.db import models
# from django.contrib.auth.models import User

class Summary(models.Model):
    user = models.IntegerField(default=0)
    input_text = models.TextField()
    generated_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)

    # In pdf_summarizer/models.py

from django.db import models

class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='uploaded_pdfs/')


