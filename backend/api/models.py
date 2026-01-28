from django.db import models


class UploadedDataset(models.Model):
    file = models.FileField(upload_to="datasets/")
    original_filename = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField()

    def __str__(self):
        return f"Dataset {self.id} ({self.original_filename}) uploaded at {self.uploaded_at}"
