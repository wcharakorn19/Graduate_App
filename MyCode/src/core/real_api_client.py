import requests
import json

# class chek api กรณีทำงานไม่ได้แต่ต้อง run sever
class MockErrorResponse:
    
    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self._error_message = error_message

    def json(self):
        return {"error": self._error_message}
        
    @property
    def text(self):
        return json.dumps(self.json())


# class core API
class RealApiClient:
    
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def post(self, endpoint, data=None):
        
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=data)
            return response
        
        except requests.exceptions.RequestException as e:
            
            print(f"API call failed: {e}")
            
            return MockErrorResponse(status_code=503, error_message="Service Unavailable")

    # --- เพิ่มเมธอด GET เข้าไป ---
    def get(self, endpoint):
        """
        ส่ง GET request ไปยัง Server จริง
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(f"API call failed: {e}")
            return MockErrorResponse(status_code=503, error_message="Service Unavailable")

