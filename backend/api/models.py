from django.db import models


class UploadedDataset(models.Model):
    file = models.FileField(upload_to="datasets/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField()

    def __str__(self):
        return f"Dataset {self.id} uploaded at {self.uploaded_at}"
