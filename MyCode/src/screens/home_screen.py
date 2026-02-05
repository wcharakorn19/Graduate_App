import flet as ft
import requests

def HomeScreen(page: ft.Page):
    
    # 1. ดึงข้อมูล Session
    current_user_email = page.session.get("user_email")
    
    # ถ้าไม่มี Session ให้ดีดกลับไป Login
    if not current_user_email:
        print("⚠️ No Session found, redirecting to login...")
        page.go("/login")
        return ft.View(controls=[ft.Text("Redirecting...")]) 

    API_ENDPOINT = f"http://127.0.0.1:8000/dashboard/{current_user_email}"

    # --- ฟังก์ชันดึงข้อมูล (เหมือนเดิม) ---
    def fetch_dashboard_data():
        try:
            response = requests.get(API_ENDPOINT, timeout=3)
            if response.status_code == 200:
                data = response.json()
                return {
                    "user_display_name": data.get("full_name", "ผู้ใช้งาน"), 
                    "documents": data.get("documents", []),
                    "stats": {
                        "pending": data.get("pending_count", 0),
                        "completed": data.get("completed_count", 0),
                        "failed": data.get("failed_count", 0)
                    }
                }
        except Exception:
            pass
        return None

    api_data = fetch_dashboard_data()

    # --- Fallback Data ---
    if not api_data:
        ui_data = {
            "user_display_name": "กำลังโหลด...",
            "documents": [],
            "current_doc": {"title": "-", "status": "-"},
            "stats": {"pending": 0, "completed": 0, "failed": 0}
        }
    else:
        docs = api_data.get("documents", [])
        first_doc = docs[0] if docs else {"title": "ไม่มีเอกสารดำเนินการ", "status": "-"}
        ui_data = {
            "user_display_name": api_data["user_display_name"],
            "documents": docs,
            "current_doc": first_doc,
            "stats": api_data["stats"]
        }

    # --- UI Components (เหมือนเดิม) ---
    def create_activity_item(title, status):
        status_color = "grey600"
        icon_color = "purple700"
        bg_color = "purple50"

        if status == "เสร็จสิ้น" or status == "ผ่านแล้ว": 
            status_color = "green"; icon_color = "green"; bg_color = "green50"
        elif status == "ไม่ผ่าน": 
            status_color = "red"; icon_color = "red"; bg_color = "red50"
        elif status == "กำลังตรวจสอบ": 
            status_color = "orange"

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(name="folder_open_outlined", color=icon_color, size=24),
                    padding=10, bgcolor=bg_color, border_radius=12,
                ),
                ft.Column([
                    ft.Text(title, size=14, weight="w500", color="black87"),
                    ft.Text(f"Status : {status}", size=12, color=status_color),
                ], spacing=2, expand=True)
            ], alignment=ft.MainAxisAlignment.START),
            padding=15, bgcolor="grey50", border_radius=12,
            border=ft.border.all(1, "grey200"), margin=ft.margin.only(bottom=10)
        )

    activity_controls = []
    if ui_data["documents"]:
        for doc in ui_data["documents"]:
            activity_controls.append(create_activity_item(doc['title'], doc['status']))
    else:
        activity_controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Icon(name="assignment_turned_in_outlined", color="grey400", size=40),
                    ft.Text("ไม่มีรายการกิจกรรมล่าสุด", color="grey500")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center, padding=30
            )
        )

    # --- Main Layout ---
    content_column = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text(ui_data['user_display_name'], size=22, weight="bold", color="black"),
                margin=ft.margin.only(top=10, bottom=15)
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Doc Name:", weight="bold", size=15, color="black"),
                    ft.Text(ui_data['current_doc']['title'], size=14, color="black87"), 
                    ft.Divider(height=10, color="transparent"),
                    ft.Text("สถานะ :", color="grey600", size=13),
                    ft.Text(
                        ui_data['current_doc']['status'], 
                        weight="bold", size=18, 
                        color="purple700" if ui_data['current_doc']['status'] != "-" else "grey400"
                    ),
                ], spacing=2),
                padding=25, bgcolor="white", border_radius=20, width=float("inf"),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color="#14000000", offset=ft.Offset(0, 4))
            ),
            ft.Container(
                content=ft.Text("Latest Activities", size=18, weight="bold", color="black"),
                margin=ft.margin.only(top=20, bottom=10)
            ),
            ft.Container(
                content=ft.Column(controls=activity_controls, spacing=0),
                padding=20, bgcolor="white", border_radius=20, width=float("inf"),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color="#14000000", offset=ft.Offset(0, 4))
            ),
            ft.Container(height=50)
        ],
        spacing=10
    )

    # --- Nav Logic ---
    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0: page.go("/profile")
        elif idx == 1: page.go("/home")  # ✅ แก้ให้ชี้มาที่ /home (ตัวเอง)
        elif idx == 2: page.go("/contact")

    bottom_nav_bar = ft.NavigationBar(
        bgcolor="white",
        indicator_color="#2A2A40",
        selected_index=1,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationBarDestination(icon="person_outline", selected_icon="person", label="Profile"),
            ft.NavigationBarDestination(icon="home_outlined", selected_icon="home", label="Home"),
            ft.NavigationBarDestination(icon="chat_bubble_outline", selected_icon="chat_bubble", label="Contact"),
        ],
    )

    return ft.View(
        route="/home", # ✅ แก้ Route ของหน้านี้ให้เป็น /home
        controls=[content_column], 
        bgcolor="white", 
        padding=20,
        scroll=ft.ScrollMode.AUTO,
        navigation_bar=bottom_nav_bar 
    )