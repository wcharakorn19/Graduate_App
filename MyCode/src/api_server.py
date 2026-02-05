from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import json
import os

def _load_users_from_json():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "core", "users_db.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Database file not found at {file_path}")
        return {}

app = FastAPI()
USERS_DB = _load_users_from_json()

# --- 1. สร้างฐานข้อมูลจำลองสำหรับหน้า Dashboard ---
DASHBOARD_DATA = {
    "65030226@kmitl.ac.th": {
        "pending_count": 3,
        "completed_count": 8,
        "failed_count": 1,
        "documents": [
            {"title": "แบบเสนอหัวข้อและเค้าโครงวิทยานิพนธ์", "status": "กำลังตรวจสอบ"},
            {"title": "แบบขอสอบวัดคุณสมบัติ", "status": "เสร็จสิ้น"},
            {"title": "แบบขอเปลี่ยนชื่อ-นามสกุล", "status": "เสร็จสิ้น"},
        ]
    },
    "65030276@kmitl.ac.th": {
        "pending_count": 1,
        "completed_count": 5,
        "failed_count": 2,
        "documents": [
            {"title": "แบบขออนุมัติสำเร็จการศึกษา", "status": "ไม่ผ่าน"},
            {"title": "แบบขอลงทะเบียนล่าช้า", "status": "กำลังตรวจสอบ"},
        ]
    }
}

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
def login_endpoint(request: LoginRequest):
    email = request.email
    password = request.password
    user = USERS_DB.get(email)
    if user and user.get("password") == password:
        user_data = user.copy()
        user_data.pop("password", None)
        print(f"Login successful for: {email}")
        return user_data
    else:
        print(f"Login failed for: {email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

# --- 2. Endpoint สำหรับหน้า Home ---
@app.get("/dashboard/{email}")
def get_dashboard_data(email: str):
    print(f"Dashboard data requested for: {email}")
    
    dashboard_data = DASHBOARD_DATA.get(email)
    
    if not dashboard_data:
        dashboard_data = {
            "pending_count": 0, "completed_count": 0,
            "failed_count": 0, "documents": []
        }
    
    user_info = USERS_DB.get(email, {})
    full_name = user_info.get("full_name", "Unknown User") 

    response_data = dashboard_data.copy()
    response_data["full_name"] = full_name 
    
    return response_data

# --- 3. (เพิ่มใหม่) Endpoint สำหรับหน้า Profile ---
@app.get("/profile/{email}")
def get_user_profile(email: str):
    print(f"Profile data requested for: {email}")
    user = USERS_DB.get(email)
    if user:
        user_data = user.copy()
        user_data.pop("password", None)
        return user_data
    else:
        return {}

if __name__ == "__main__":
    print("Starting FastAPI server at http://127.0.0.1:8000")
    uvicorn.run("src.api_server:app", host="127.0.0.1", port=8000, reload=True)