import flet as ft
import requests

def FormOneDetailScreen(page: ft.Page, submission_id: str):
    
    # --- 1. เตรียมตัวแปรและ UI Loading ---
    token = page.session.get("token")
    
    # UI Components (สร้างรอไว้ก่อนจะเอาข้อมูลมาหยอด)
    student_name_val = ft.Text("-", size=14, color="#333333")
    student_id_val = ft.Text("-", size=14, color="#333333")
    degree_val = ft.Text("-", size=14, color="#333333")
    program_val = ft.Text("-", size=14, color="#333333")
    dept_val = ft.Text("-", size=14, color="#333333")
    faculty_val = ft.Text("-", size=14, color="#333333")
    plan_val = ft.Text("-", size=14, color="#333333")
    phone_val = ft.Text("-", size=14, color="#333333")
    email_val = ft.Text("-", size=14, color="#333333")
    
    main_advisor_val = ft.Text("-", size=14, color="#333333")
    co_advisor_val = ft.Text("-", size=14, color="#333333")

    # --- 2. ฟังก์ชันดึงข้อมูลจาก Server ---
    def load_data():
        if not token: return
        
        try:
            # ยิงไปที่ API ดึงรายละเอียด Submission
            api_url = f"http://127.0.0.1:3000/api/submissions/{submission_id}"
            headers = {"Authorization": f"Bearer {token}"}
            res = requests.get(api_url, headers=headers)
            
            if res.status_code == 200:
                data = res.json()
                detail = data.get("documentDetail", {}) # ข้อมูลเอกสาร + โปรไฟล์
                advisors_list = data.get("advisors", []) # รายชื่ออาจารย์ทั้งหมด (เอาไว้เทียบ ID เป็นชื่อ)
                
                # Helper หาชื่ออาจารย์จาก ID
                def get_advisor_name(adv_id):
                    if not adv_id: return "-"
                    for adv in advisors_list:
                        if adv.get("advisor_id") == adv_id:
                            return f"{adv.get('prefix_th')}{adv.get('first_name_th')} {adv.get('last_name_th')}"
                    return f"รหัส {adv_id}"

                # --- Map ข้อมูลลง UI ---
                # 1. ข้อมูลส่วนตัว
                prefix = detail.get("prefix_th") or ""
                first = detail.get("first_name_th") or ""
                last = detail.get("last_name_th") or ""
                student_name_val.value = f"{prefix}{first} {last}"
                
                student_id_val.value = detail.get("student_id", "-")
                degree_val.value = detail.get("degree", "-")
                program_val.value = detail.get("program_name", "-")
                dept_val.value = detail.get("department_name", "-")
                faculty_val.value = detail.get("faculty", "-")
                plan_val.value = detail.get("plan", "-")
                phone_val.value = detail.get("phone", "-")
                email_val.value = detail.get("email", "-")

                # 2. ข้อมูลที่ขอในฟอร์ม (Form Details)
                form_details = detail.get("form_details", {})
                
                req_main_id = form_details.get("main_advisor_id") or detail.get("main_advisor_id")
                req_co_id = form_details.get("co_advisor_id") or detail.get("co_advisor_id")
                
                main_advisor_val.value = get_advisor_name(req_main_id)
                co_advisor_val.value = get_advisor_name(req_co_id)
                
                page.update()
                
        except Exception as e:
            print(f"Error loading form 1 detail: {e}")

    # --- 3. สร้าง UI Helper Function ---
    def create_row(label, value_control):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    width=120, 
                    content=ft.Text(label, size=14, color="#888888")
                ),
                ft.Container(
                    expand=True,
                    content=value_control
                )
            ]
        )

    # --- 4. ประกอบร่าง Layout ---
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
                create_row("ระดับการศึกษา:", degree_val),
                create_row("หลักสูตร:", program_val),
                create_row("ภาควิชา:", dept_val),
                create_row("คณะ:", faculty_val),
                create_row("แผนการเรียน:", plan_val),
                create_row("เบอร์โทรศัพท์:", phone_val),
                create_row("อีเมล:", email_val),
            ]
        )
    )

    advisor_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#08000000", offset=ft.Offset(0, 4)),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("อาจารย์ที่ปรึกษา", size=16, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                create_row("อาจารย์ที่ปรึกษาหลัก:", main_advisor_val),
                ft.Divider(height=1, color="#EEEEEE"),
                create_row("อาจารย์ที่ปรึกษาร่วม:", co_advisor_val),
            ]
        )
    )

    load_data()

    return ft.View(
        route=f"/form1/{submission_id}",
        bgcolor="#FFF5F7",
        
        # ✅ แก้ไขจุดที่ 1: เพิ่ม Scroll ที่ตัว View หลักเลย (สำคัญมาก)
        scroll=ft.ScrollMode.AUTO, 
        
        appbar=ft.AppBar(
            leading=ft.IconButton(icon="arrow_back", icon_color="black", on_click=lambda _: page.go("/home")),
            title=ft.Text("KMITL", color="black", weight="bold"),
            center_title=True,
            bgcolor="#FFF5F7",
            elevation=0
        ),
        controls=[
            ft.Column(
                # ✅ แก้ไขจุดที่ 2: ลบ scroll ออกจาก Column ข้างใน (เพื่อไม่ให้ชนกัน)
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=20, right=20, bottom=10),
                        content=ft.Text(
                            "แบบฟอร์มขอรับรองการเป็นอาจารย์\nที่ปรึกษาวิทยานิพนธ์ หลัก/ร่วม", 
                            size=18, 
                            weight="bold", 
                            color="black", 
                            text_align="center"
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(padding=10), 
                    student_card,
                    ft.Container(padding=5),  
                    advisor_card,
                    ft.Container(padding=20), 
                ]
            )
        ]
    )