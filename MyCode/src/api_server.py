from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
import uvicorn
import json                         
import os                             

# fuction อ่าน data json
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

# class จะรับแค่ email and password for Login
class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/login")

# fuction request
def login_endpoint(request: LoginRequest):

    email = request.email
    password = request.password

    # ค้นหาผู้ใช้ใน USERS_DB ด้วย email
    user = USERS_DB.get(email)
    
    # ตรวจสอบว่ามีผู้ใช้นี้อยู่จริง และรหัสผ่านที่ส่งมาตรงกันหรือไม่
    if user and user.get("password") == password:
        user_data = user.copy()
        user_data.pop("password", None)
        
        print(f"Login successful for: {email}")
        return user_data
    
    else:
        print(f"Login failed for: {email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")


if __name__ == "__main__":
    print("Starting FastAPI server at http://127.0.0.1:8000")
    
    uvicorn.run("api_server:app", host="127.0.0.1", port=8000, reload=True)

