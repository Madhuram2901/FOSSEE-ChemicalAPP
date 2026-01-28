"""
API Client for Chemical Equipment Visualizer Desktop App
Handles all communication with the Django backend
"""
import requests
from typing import Optional, Dict, List, Any


class APIClient:
    """Client for interacting with the backend API"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        """
        Initialize API client
        
        Args:
            base_url: Base URL for the API (default: http://localhost:8000/api)
        """
        self.base_url = base_url
        self.timeout = 30  # 30 seconds timeout
    
    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Upload a CSV file to the backend
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            dict: Response containing dataset_id and message
            
        Raises:
            Exception: If upload fails
        """
        url = f"{self.base_url}/upload/"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    raise Exception(error_data.get('error', str(e)))
                except:
                    raise Exception(f"Upload failed: {str(e)}")
            raise Exception(f"Upload failed: {str(e)}")
    
    def get_summary(self, dataset_id: int) -> Dict[str, Any]:
        """
        Get summary for a specific dataset
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            dict: Summary data containing total_equipment, averages, type_distribution, and table
            
        Raises:
            Exception: If request fails
        """
        url = f"{self.base_url}/summary/{dataset_id}/"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    raise Exception(error_data.get('error', str(e)))
                except:
                    raise Exception(f"Failed to fetch summary: {str(e)}")
            raise Exception(f"Failed to fetch summary: {str(e)}")
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get list of recent uploads
        
        Returns:
            list: List of datasets with id, filename, and uploaded_at
            
        Raises:
            Exception: If request fails
        """
        url = f"{self.base_url}/history/"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    raise Exception(error_data.get('error', str(e)))
                except:
                    raise Exception(f"Failed to fetch history: {str(e)}")
            raise Exception(f"Failed to fetch history: {str(e)}")
    
    def check_connection(self) -> bool:
        """
        Check if backend is accessible
        
        Returns:
            bool: True if backend is accessible, False otherwise
        """
        try:
            url = f"{self.base_url}/"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False
