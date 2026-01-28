"""
API Client for Chemical Equipment Visualizer Desktop App
Handles all communication with the Django backend
"""
import os
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
        self.token = self._load_token()

    def _load_token(self) -> Optional[str]:
        """Load token from local file"""
        try:
            if os.path.exists("token.txt"):
                with open("token.txt", "r") as f:
                    return f.read().strip()
        except Exception:
            pass
        return None

    def save_token(self, token: str):
        """Save token to local file"""
        self.token = token
        try:
            with open("token.txt", "w") as f:
                f.write(token)
        except Exception as e:
            print(f"Failed to save token: {e}")

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token"""
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def login(self, username, password) -> bool:
        """Login to get JWT token"""
        url = f"{self.base_url}/token/"
        try:
            response = requests.post(url, data={'username': username, 'password': password}, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            self.save_token(data['access'])
            return True
        except Exception as e:
            if hasattr(e, 'response') and e.response:
                raise Exception(f"Login failed: {e.response.text}")
            raise Exception(f"Login failed: {e}")

    def register(self, username, email, password) -> bool:
        """Register a new user"""
        url = f"{self.base_url}/register/"
        try:
            response = requests.post(url, data={'username': username, 'email': email, 'password': password}, timeout=self.timeout)
            response.raise_for_status()
            return True
        except Exception as e:
            if hasattr(e, 'response') and e.response:
                raise Exception(f"Registration failed: {e.response.text}")
            raise Exception(f"Registration failed: {e}")

    def logout(self):
        """Logout by clearing local token"""
        self.token = None
        if os.path.exists("token.txt"):
            try:
                os.remove("token.txt")
            except:
                pass
    
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
                filename = os.path.basename(file_path)
                files = {'file': (filename, f)}
                response = requests.post(url, files=files, headers=self._get_headers(), timeout=self.timeout)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 401:
                    raise Exception("Authentication failed")
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
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 401:
                    raise Exception("Authentication failed")
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
            response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 401:
                    raise Exception("Authentication failed")
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
            url = f"{self.base_url}/"  # This is usually allowed, but if not, 401 means server is up
            response = requests.get(url, timeout=5)
            # 200 is good. 401 means it's there but protected (which counts as connected).
            return response.status_code in [200, 401]
        except:
            return False
