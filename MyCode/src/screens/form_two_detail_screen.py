import flet as ft
import requests
import json

def FormTwoDetailScreen(page: ft.Page, submission_id: str):
    
    token = page.session.get("token")
    
    # --- 1. สร้างตัวแปร UI รอรับข้อมูล ---
    # กลุ่มข้อมูลนักศึกษา
    student_name_val = ft.Text("-", size=14, color="#333333")
    student_id_val = ft.Text("-", size=14, color="#333333")
    degree_val = ft.Text("-", size=14, color="#333333")
    program_val = ft.Text("-", size=14, color="#333333")
    dept_val = ft.Text("-", size=14, color="#333333")

    # กลุ่มอาจารย์ที่ปรึกษา
    main_advisor_val = ft.Text("-", size=14, color="#333333")
    co_advisor_val = ft.Text("-", size=14, color="#333333")

    # กลุ่มคณะกรรมการสอบ
    chair_val = ft.Text("-", size=14, color="#333333")       # ประธาน
    committee_val = ft.Text("-", size=14, color="#333333")   # กรรมการ (ที่ปรึกษาร่วม 2)
    member5_val = ft.Text("-", size=14, color="#333333")     # กรรมการสอบ (คนที่ 5)

    # กลุ่มคณะกรรมการสำรอง
    reserve_ext_val = ft.Text("-", size=14, color="#333333") # สำรองภายนอก
    reserve_int_val = ft.Text("-", size=14, color="#333333") # สำรองภายใน

    # --- 2. ฟังก์ชันดึงข้อมูลจาก Server ---
    def load_data():
        if not token: return
        
        try:
            # ใช้ API เดียวกับ Form 1 เพราะมันคืนค่า documentDetail ครบถ้วน
            api_url = f"http://127.0.0.1:3000/api/submissions/{submission_id}"
            headers = {"Authorization": f"Bearer {token}"}
            res = requests.get(api_url, headers=headers)
            
            if res.status_code == 200:
                data = res.json()
                detail = data.get("documentDetail", {})
                advisors_list = data.get("advisors", []) # รายชื่ออาจารย์ทั้งหมดเอาไว้เทียบ ID
                
                # ฟังก์ชันแปลง ID เป็นชื่ออาจารย์
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

                # 2.2 Map ข้อมูลฟอร์ม (Committee)
                form_details = detail.get("form_details", {})
                committee = form_details.get("committee", {})

                # อาจารย์ที่ปรึกษา (ดึงจาก Form หรือ Profile)
                req_main_id = form_details.get("main_advisor_id") or detail.get("main_advisor_id")
                req_co_id = form_details.get("co_advisor_id") or detail.get("co_advisor1_id") # บางทีใช้ co_advisor1_id
                
                main_advisor_val.value = get_advisor_name(req_main_id)
                co_advisor_val.value = get_advisor_name(req_co_id)

                # คณะกรรมการสอบ
                chair_val.value = get_advisor_name(committee.get("chair_id"))
                committee_val.value = get_advisor_name(committee.get("co_advisor2_id"))
                member5_val.value = get_advisor_name(committee.get("member5_id"))

                # คณะกรรมการสำรอง
                reserve_ext_val.value = get_advisor_name(committee.get("reserve_external_id"))
                reserve_int_val.value = get_advisor_name(committee.get("reserve_internal_id"))

                page.update()
                
        except Exception as e:
            print(f"Error loading form 2 detail: {e}")

    # --- 3. UI Helper ---
    def create_row(label, value_control):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    width=140, # เพิ่มความกว้าง Label นิดหน่อยสำหรับชื่อยาวๆ
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

    # Card 2: อาจารย์และกรรมการ (ยาวหน่อยตามแบบ)
    committee_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#08000000", offset=ft.Offset(0, 4)),
        content=ft.Column(
            spacing=12,
            controls=[
                # ส่วนที่ 1: ที่ปรึกษา
                ft.Text("อาจารย์ที่ปรึกษาและคณะกรรมการสอบ", size=16, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                create_row("อาจารย์ที่ปรึกษาหลัก:", main_advisor_val),
                create_row("อาจารย์ที่ปรึกษาร่วม:", co_advisor_val),
                
                ft.Divider(height=20, color="#EEEEEE"), # เส้นคั่นบางๆ
                
                # ส่วนที่ 2: กรรมการสอบ
                ft.Text("ชื่อคณะกรรมการสอบ", size=15, weight="bold", color="black"),
                create_row("ประธานกรรมการสอบ:", chair_val),
                create_row("กรรมการ (ที่ปรึกษาร่วม 2):", committee_val),
                create_row("กรรมการสอบ (คนที่ 5):", member5_val),

                ft.Divider(height=20, color="#EEEEEE"), # เส้นคั่นบางๆ

                # ส่วนที่ 3: กรรมการสำรอง
                ft.Text("ชื่อคณะกรรมการสำรอง", size=15, weight="bold", color="black"),
                create_row("กรรมการสำรอง (ภายนอก):", reserve_ext_val),
                create_row("กรรมการสำรอง (ภายใน):", reserve_int_val),
            ]
        )
    )

    load_data()

    return ft.View(
        route=f"/form2/{submission_id}",
        bgcolor="#FFF5F7",
        scroll=ft.ScrollMode.AUTO, # ✅ Scroll ได้ทั้งหน้า
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
                            "แบบเสนอหัวข้อและเค้าโครงวิทยานิพนธ์", 
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
                    committee_card,
                    ft.Container(padding=20),
                ]
            )
        ]
    )