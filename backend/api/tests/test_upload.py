from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
import io
import pandas as pd

class UploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('upload-csv')
        
    def test_upload_valid_csv(self):
        # Create a valid minimal CSV
        df = pd.DataFrame({
            "Equipment Name": ["Eq1"],
            "Type": ["Pump"],
            "Flowrate": [100],
            "Pressure": [50],
            "Temperature": [300]
        })
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        file = SimpleUploadedFile("valid.csv", csv_buffer.getvalue(), content_type="text/csv")
        response = self.client.post(self.url, {'file': file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("dataset_id", response.data)

    def test_upload_invalid_extension(self):
        file = SimpleUploadedFile("test.txt", b"some content", content_type="text/plain")
        response = self.client.post(self.url, {'file': file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid file format", str(response.data))

    def test_upload_missing_columns(self):
        # Missing 'Pressure'
        df = pd.DataFrame({
            "Equipment Name": ["Eq1"],
            "Type": ["Pump"],
            "Flowrate": [100],
            "Temperature": [300]
        })
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        file = SimpleUploadedFile("incomplete.csv", csv_buffer.getvalue(), content_type="text/csv")
        response = self.client.post(self.url, {'file': file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing required columns", str(response.data))

    def test_upload_empty_csv(self):
        file = SimpleUploadedFile("empty.csv", b"", content_type="text/csv")
        response = self.client.post(self.url, {'file': file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("empty", str(response.data).lower())
