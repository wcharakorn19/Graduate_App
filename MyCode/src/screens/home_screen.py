import flet as ft
# --- 1. Import API Client ของเรา ---
from src.core.real_api_client import RealApiClient

def HomeScreen(page: ft.Page):
    
    # --- 2. สร้าง instance ของ API Client ---
    api_client = RealApiClient()

    # --- โครงสร้าง UI เดิมของคุณ ---
    pending_count = ft.Text("...", size=20, weight=ft.FontWeight.BOLD)
    completed_count = ft.Text("...", size=20, weight=ft.FontWeight.BOLD)
    failed_count = ft.Text("...", size=20, weight=ft.FontWeight.BOLD)
    recent_documents_list = ft.Column(spacing=15)

    # --- ฟังก์ชันสำหรับอัปเดต UI (เหมือนเดิม) ---
    def update_dashboard_data(data):
        pending_count.value = str(data.get("pending_count", 0))
        completed_count.value = str(data.get("completed_count", 0))
        failed_count.value = str(data.get("failed_count", 0))
        recent_documents_list.controls.clear()
        
        documents = data.get("documents", [])
        if not documents:
            recent_documents_list.controls.append(ft.Text("ไม่มีเอกสารล่าสุด", color="grey"))
        else:
            for doc in documents:
                recent_documents_list.controls.append(
                    _create_document_card(doc.get("title"), doc.get("status"))
                )
        # ไม่ต้องเรียก page.update() ที่นี่ เพราะเราจะเรียกตอนท้ายทีเดียว

    # --- Helper Functions (เหมือนเดิม) ---
    def _create_status_card(count_control, label, bgcolor, border_color):
        return ft.Container(
            width=110, height=90, bgcolor=bgcolor, border_radius=15,
            border=ft.border.all(1, border_color), padding=15,
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Container(
                        width=24, height=24, bgcolor="white",
                        border_radius=12, alignment=ft.alignment.center,
                        content=count_control
                    ),
                    ft.Text(label, size=12)
                ]
            )
        )
    def _create_document_card(title, status):
        return ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Row(
                    controls=[
                        ft.Container(width=60, height=60, bgcolor="#eeeeee", border_radius=10),
                        ft.Column(
                            [
                                ft.Text(title, weight=ft.FontWeight.BOLD, size=14),
                                ft.Text(f"สถานะ: {status}", size=12, color="grey"),
                            ],
                            spacing=5, expand=True,
                        )
                    ]
                )
            )
        )
    
    # --- 3. ย้าย Logic การเรียก API มาไว้ตรงนี้ (ตำแหน่งที่ถูกต้อง) ---
    # โค้ดส่วนนี้จะทำงานทันทีที่หน้า Home ถูกสร้างขึ้น
    user_data = getattr(page, "user_data", {})
    user_email = user_data.get("email")

    if user_email:
        print(f"--- HomeScreen CREATED, fetching data for {user_email} ---")
        response = api_client.get(f"/dashboard/{user_email}")
        if response.status_code == 200:
            dashboard_data = response.json()
            # นำข้อมูลที่ได้ไปใส่ใน UI ทันที
            update_dashboard_data(dashboard_data)
        else:
            print("Failed to fetch dashboard data.")
            update_dashboard_data({})
    else:
        print("No user email found to fetch dashboard data.")
        update_dashboard_data({})

    # --- โครงสร้าง UI เดิมของคุณ (แก้ไขไวยากรณ์ให้ถูกต้อง) ---
    header_content = ft.Container(
        height=200, bgcolor="black", border_radius=ft.border_radius.vertical(bottom=25), padding=20,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row([
                    ft.Image(src="logo_1.jpeg", width=50, height=50, fit=ft.ImageFit.CONTAIN),
                    ft.IconButton(icon="exit_to_app", icon_color="white", on_click=lambda _: page.go("/"))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.TextField(
                    hint_text="Search",
                    border_radius=10, bgcolor="#424242",
                    border_color="transparent", height=40, text_size=14, content_padding=10
                )
            ]
        )
    )
    overview_content = ft.Container(
        bgcolor="white", border_radius=15, padding=20,
        content=ft.Column(
            [
                ft.Text("Process Overview", weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        _create_status_card(pending_count, "กำลังตรวจสอบ", "#fff9c4", "#fbc02d"),
                        _create_status_card(completed_count, "เสร็จสิ้น", "#c8e6c9", "#388e3c"),
                        _create_status_card(failed_count, "ไม่ผ่าน", "#ffcdd2", "#d32f2f"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                )
            ],
            spacing=15
        )
    )
    documents_content = ft.Container(
        bgcolor="white", border_radius=15, padding=20,
        content=ft.Column(
            [ft.Text("Recent Documents", weight=ft.FontWeight.BOLD), recent_documents_list],
            spacing=15,
            scroll=ft.ScrollMode.AUTO
        )
    )

    def on_nav_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0: page.go("/profile")
        elif selected_index == 2: page.go("/contact")
    bottom_nav_bar = ft.NavigationBar(
        selected_index=1,
        destinations=[
            ft.NavigationBarDestination(icon="person_outline", selected_icon="person", label="Profile"),
            ft.NavigationBarDestination(icon="home_outlined", selected_icon="home", label="Home"),
            ft.NavigationBarDestination(icon="chat_bubble_outline", selected_icon="chat_bubble", label="Contact"),
        ],
        on_change=on_nav_change
    )

    return ft.View(
        route="/home",
        bgcolor="#f0f0f0",
        padding=0,
        controls=[
            ft.Column(
                expand=True, spacing=0,
                controls=[
                    header_content,
                    ft.Container(
                        padding=20, expand=True,
                        content=ft.Column(
                            [overview_content, documents_content],
                            spacing=20, expand=True, scroll=ft.ScrollMode.AUTO
                        )
                    ),
                    bottom_nav_bar,
                ]
            )
        ]
    )

