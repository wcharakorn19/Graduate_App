import flet as ft
import requests

def FormThreeDetailScreen(page: ft.Page, submission_id: str):
    
    token = page.session.get("token")
    
    # --- 1. สร้างตัวแปร UI รอรับข้อมูล ---
    # กลุ่มข้อมูลนักศึกษา
    student_name_val = ft.Text("-", size=14, color="#333333")
    student_id_val = ft.Text("-", size=14, color="#333333")
    degree_val = ft.Text("-", size=14, color="#333333")
    program_val = ft.Text("-", size=14, color="#333333")
    dept_val = ft.Text("-", size=14, color="#333333")

    # กลุ่มข้อมูลหัวข้อวิทยานิพนธ์
    approve_date_val = ft.Text("-", size=14, color="#333333")
    title_th_val = ft.Text("-", size=14, color="#333333")
    title_en_val = ft.Text("-", size=14, color="#333333")

    # กลุ่มอาจารย์ผู้รับผิดชอบ
    chair_val = ft.Text("-", size=14, color="#333333")       # ประธาน
    main_advisor_val = ft.Text("-", size=14, color="#333333") # ที่ปรึกษาหลัก
    co_advisor_val = ft.Text("-", size=14, color="#333333")   # ที่ปรึกษาร่วม 1

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
                advisors_list = data.get("advisors", [])
                
                # Helper แปลง ID เป็นชื่อ
                def get_advisor_name(adv_id):
                    if not adv_id: return "-"
                    for adv in advisors_list:
                        if adv.get("advisor_id") == adv_id:
                            return f"{adv.get('prefix_th')}{adv.get('first_name_th')} {adv.get('last_name_th')}"
                    return f"รหัส {adv_id}"

                # 2.1 Map ข้อมูลนักศึกษา
                prefix = detail.get("prefix_th") or ""
                first = detail.get("first_name_th") or ""
                last = detail.get("last_name_th") or ""
                student_name_val.value = f"{prefix}{first} {last}"
                
                student_id_val.value = detail.get("student_id", "-")
                degree_val.value = detail.get("degree", "-")
                program_val.value = detail.get("program_name", "-")
                dept_val.value = detail.get("department_name", "-")

                # 2.2 Map ข้อมูลฟอร์ม
                form_details = detail.get("form_details", {})
                
                # ข้อมูลหัวข้อ
                # (สมมติว่ามี field approved_date ถ้าไม่มีใช้ updated_at แทนไปก่อน)
                approve_date_val.value = form_details.get("approved_date") or detail.get("updated_at", "-")[:10]
                title_th_val.value = form_details.get("thesis_title_th", "-")
                title_en_val.value = form_details.get("thesis_title_en", "-")

                # ข้อมูลอาจารย์ (ดึงจาก committee หรือ advisor fields)
                committee = form_details.get("committee", {})
                
                # ประธานกรรมการสอบ
                chair_val.value = get_advisor_name(committee.get("chair_id"))
                
                # ที่ปรึกษาหลัก
                main_id = form_details.get("main_advisor_id") or detail.get("main_advisor_id")
                main_advisor_val.value = get_advisor_name(main_id)
                
                # ที่ปรึกษาร่วม 1
                co_id = form_details.get("co_advisor_id") or detail.get("co_advisor1_id")
                co_advisor_val.value = get_advisor_name(co_id)

                page.update()
                
        except Exception as e:
            print(f"Error loading form 3 detail: {e}")

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

    # Card 2: ข้อมูลหัวข้อและอาจารย์
    thesis_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#08000000", offset=ft.Offset(0, 4)),
        content=ft.Column(
            spacing=12,
            controls=[
                # ส่วนที่ 1: ข้อมูลหัวข้อ
                ft.Text("ข้อมูลหัวข้อวิทยานิพนธ์ (ที่ได้อนุมัติ)", size=16, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                create_row("วันที่อนุมัติหัวข้อ:", approve_date_val),
                create_row("ชื่อเรื่อง (TH):", title_th_val),
                create_row("ชื่อเรื่อง (ENG):", title_en_val),
                
                ft.Divider(height=20, color="#EEEEEE"), # เส้นคั่น
                
                # ส่วนที่ 2: อาจารย์ผู้รับผิดชอบ
                ft.Text("อาจารย์ผู้รับผิดชอบ", size=16, weight="bold", color="black"),
                create_row("ประธานกรรมการสอบ:", chair_val),
                create_row("อาจารย์ที่ปรึกษาหลัก:", main_advisor_val),
                create_row("อาจารย์ที่ปรึกษาร่วม 1:", co_advisor_val),
            ]
        )
    )

    # โหลดข้อมูล
    load_data()

    return ft.View(
        route=f"/form3/{submission_id}",
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
                            "แบบเสนอหัวข้อ\nและเค้าโครงวิทยานิพนธ์ เล่ม 1", 
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
                    ft.Container(padding=20),
                ]
            )
        ]
    )