import flet as ft
import requests

def FormFourDetailScreen(page: ft.Page, submission_id: str):
    
    token = page.session.get("token")
    
    # --- 1. สร้างตัวแปร UI รอรับข้อมูล ---
    # กลุ่มข้อมูลนักศึกษา (เหมือนเดิมทุกฟอร์ม)
    student_name_val = ft.Text("-", size=14, color="#333333")
    student_id_val = ft.Text("-", size=14, color="#333333")
    degree_val = ft.Text("-", size=14, color="#333333")
    program_val = ft.Text("-", size=14, color="#333333")
    dept_val = ft.Text("-", size=14, color="#333333")

    # กลุ่มข้อมูลหัวข้อวิทยานิพนธ์
    approve_date_val = ft.Text("-", size=14, color="#333333")
    title_th_val = ft.Text("-", size=14, color="#333333")
    title_en_val = ft.Text("-", size=14, color="#333333")

    # กลุ่มข้อมูลผู้ทรงคุณวุฒิ (Expert)
    expert_title_val = ft.Text("-", size=14, color="#333333") # คำนำหน้า/ยศ
    expert_name_val = ft.Text("-", size=14, color="#333333")  # ชื่อ
    expert_surname_val = ft.Text("-", size=14, color="#333333") # นามสกุล
    expert_org_val = ft.Text("-", size=14, color="#333333")   # สถาบัน/หน่วยงาน
    expert_phone_val = ft.Text("-", size=14, color="#333333") # เบอร์โทร
    expert_email_val = ft.Text("-", size=14, color="#333333") # อีเมล

    # --- 2. ฟังก์ชันดึงข้อมูลจาก Server ---
    def load_data():
        if not token: return
        
        try:
            api_url = f"http://127.0.0.1:3000/api/submissions/{submission_id}"
            headers = {"Authorization": f"Bearer {token}"}
            res = requests.get(api_url, headers=headers)
            
            if res.status_code == 200:
                data = res.json()
                detail = data.get("documentDetail", {})
                
                # 2.1 Map ข้อมูลนักศึกษา
                prefix = detail.get("prefix_th") or ""
                first = detail.get("first_name_th") or ""
                last = detail.get("last_name_th") or ""
                student_name_val.value = f"{prefix}{first} {last}"
                
                student_id_val.value = detail.get("student_id", "-")
                degree_val.value = detail.get("degree", "-")
                program_val.value = detail.get("program_name", "-")
                dept_val.value = detail.get("department_name", "-")

                # 2.2 Map ข้อมูลฟอร์ม (Form Details)
                form_details = detail.get("form_details", {})

                # ข้อมูลหัวข้อ
                approve_date_val.value = form_details.get("approved_date") or detail.get("updated_at", "-")[:10]
                title_th_val.value = form_details.get("thesis_title_th", "-")
                title_en_val.value = form_details.get("thesis_title_en", "-")

                # ข้อมูลผู้ทรงคุณวุฒิ
                # (Key ตรงนี้ต้องตรงกับที่ Web ส่งมา เช็คใน DB อีกทีนะครับ)
                expert_info = form_details.get("expert_info", {}) 
                # ถ้า Web ไม่ได้เก็บเป็น Object expert_info ให้ลองดึงตรงๆ จาก form_details
                
                expert_title_val.value = expert_info.get("title") or form_details.get("expert_title", "-")
                expert_name_val.value = expert_info.get("firstname") or form_details.get("expert_firstname", "-")
                expert_surname_val.value = expert_info.get("lastname") or form_details.get("expert_lastname", "-")
                expert_org_val.value = expert_info.get("institution") or form_details.get("expert_institution", "-")
                expert_phone_val.value = expert_info.get("phone") or form_details.get("expert_phone", "-")
                expert_email_val.value = expert_info.get("email") or form_details.get("expert_email", "-")

                page.update()
                
        except Exception as e:
            print(f"Error loading form 4 detail: {e}")

    # --- 3. UI Helper ---
    def create_row(label, value_control):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    width=140, 
                    content=ft.Text(label, size=14, color="#888888")
                ),
                ft.Container(
                    expand=True,
                    content=value_control
                )
            ]
        )

    # --- 4. Layout ประกอบร่าง ---
    
    # Card 1: ข้อมูลนักศึกษา
    student_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#08000000", offset=ft.Offset(0, 4)),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("ข้อมูลนักศึกษา", size=16, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                create_row("ชื่อ-นามสกุล:", student_name_val),
                create_row("รหัสนักศึกษา:", student_id_val),
                create_row("ระดับปริญญา:", degree_val),
                create_row("หลักสูตรและสาขาวิชา:", program_val),
                create_row("ภาควิชา:", dept_val),
            ]
        )
    )

    # Card 2: ข้อมูลหัวข้อ
    thesis_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#08000000", offset=ft.Offset(0, 4)),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("ข้อมูลหัวข้อวิทยานิพนธ์ (ที่ได้อนุมัติ)", size=16, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                create_row("วันที่เสนอเค้าโครงได้รับอนุมัติ:", approve_date_val),
                create_row("ชื่อเรื่อง (TH):", title_th_val),
                create_row("ชื่อเรื่อง (ENG):", title_en_val),
            ]
        )
    )

    # Card 3: ข้อมูลผู้ทรงคุณวุฒิ
    expert_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#08000000", offset=ft.Offset(0, 4)),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("ข้อมูลผู้ทรงคุณวุฒิ คนที่ 1", size=16, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                create_row("คำนำหน้า/ ยศ(ตำแหน่ง):", expert_title_val),
                create_row("ชื่อ:", expert_name_val),
                create_row("นามสกุล:", expert_surname_val),
                create_row("สถาบัน/หน่วยงาน:", expert_org_val),
                create_row("เบอร์โทรศัพท์:", expert_phone_val),
                create_row("อีเมล:", expert_email_val),
            ]
        )
    )

    # โหลดข้อมูล
    load_data()

    return ft.View(
        route=f"/form4/{submission_id}",
        bgcolor="#FFF5F7",
        scroll=ft.ScrollMode.AUTO, # ✅ Scroll ได้
        appbar=ft.AppBar(
            leading=ft.IconButton(icon="arrow_back", icon_color="black", on_click=lambda _: page.go("/home")),
            title=ft.Text("KMITL", color="black", weight="bold"),
            center_title=True,
            bgcolor="#FFF5F7",
            elevation=0
        ),
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=20, right=20, bottom=10),
                        content=ft.Text(
                            "แบบขอหนังสือเชิญเป็นผู้ทรงคุณวุฒิ\nตรวจและประเมิน...เพื่อวิจัย", 
                            size=18, 
                            weight="bold", 
                            color="black", 
                            text_align="center"
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(padding=5),
                    student_card,
                    ft.Container(padding=5),
                    thesis_card,
                    ft.Container(padding=5),
                    expert_card,
                    ft.Container(padding=20),
                ]
            )
        ]
    )