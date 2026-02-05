import flet as ft
import requests

def FormSixDetailScreen(page: ft.Page, submission_id: str):
    
    token = page.session.get("token")
    
    # --- 1. เตรียมตัวแปร UI ---
    # กลุ่มข้อมูลผู้ยื่นคำร้อง (เยอะหน่อยนะครับฟอร์มนี้)
    student_name_val = ft.Text("-", size=14, color="#333333")
    student_id_val = ft.Text("-", size=14, color="#333333")
    degree_val = ft.Text("-", size=14, color="#333333")
    program_val = ft.Text("-", size=14, color="#333333")
    dept_val = ft.Text("-", size=14, color="#333333")
    
    start_semester_val = ft.Text("-", size=14, color="#333333") # เริ่มต้นภาคเรียนที่
    start_year_val = ft.Text("-", size=14, color="#333333")     # ปีการศึกษา
    phone_val = ft.Text("-", size=14, color="#333333")
    address_val = ft.Text("-", size=14, color="#333333")        # ที่อยู่
    workplace_val = ft.Text("-", size=14, color="#333333")      # ที่ทำงาน
    
    thesis_th_val = ft.Text("-", size=14, color="#333333")
    thesis_en_val = ft.Text("-", size=14, color="#333333")

    # กลุ่มอาจารย์และกรรมการ
    main_advisor_val = ft.Text("-", size=14, color="#333333")
    co_advisor_val = ft.Text("-", size=14, color="#333333")
    
    chair_val = ft.Text("-", size=14, color="#333333")       # ประธาน
    committee_val = ft.Text("-", size=14, color="#333333")   # กรรมการ (ที่ปรึกษาร่วม 2)
    member5_val = ft.Text("-", size=14, color="#333333")     # กรรมการสอบ (คนที่ 5)
    
    reserve_ext_val = ft.Text("-", size=14, color="#333333") # สำรองภายนอก
    reserve_int_val = ft.Text("-", size=14, color="#333333") # สำรองภายใน

    # --- 2. ฟังก์ชันดึงข้อมูล ---
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

                # 2.1 Map ข้อมูลพื้นฐาน
                prefix = detail.get("prefix_th") or ""
                first = detail.get("first_name_th") or ""
                last = detail.get("last_name_th") or ""
                student_name_val.value = f"{prefix}{first} {last}"
                
                student_id_val.value = detail.get("student_id", "-")
                degree_val.value = detail.get("degree", "-")
                program_val.value = detail.get("program_name", "-")
                dept_val.value = detail.get("department_name", "-")
                phone_val.value = detail.get("phone", "-") # เบอร์โทรจาก Profile

                # 2.2 Map ข้อมูลจาก Form Details
                form_details = detail.get("form_details", {})

                # ข้อมูลเพิ่มเติม (บางอันอาจไม่มีใน DB ก็จะโชว์ -)
                # สมมติว่าเก็บใน form_details หรือดึงจาก profile
                start_semester_val.value = str(form_details.get("entry_semester") or detail.get("entry_semester") or "-")
                start_year_val.value = str(form_details.get("entry_year") or detail.get("entry_year") or "-")
                address_val.value = form_details.get("current_address", "-") 
                workplace_val.value = form_details.get("workplace", "-")

                # ชื่อวิทยานิพนธ์
                thesis_th_val.value = form_details.get("thesis_title_th", "-")
                thesis_en_val.value = form_details.get("thesis_title_en", "-")

                # 2.3 Map ข้อมูลคณะกรรมการ
                committee = form_details.get("committee", {})

                # อาจารย์ที่ปรึกษา
                req_main_id = form_details.get("main_advisor_id") or detail.get("main_advisor_id")
                req_co_id = form_details.get("co_advisor_id") or detail.get("co_advisor1_id")
                main_advisor_val.value = get_advisor_name(req_main_id)
                co_advisor_val.value = get_advisor_name(req_co_id)

                # คณะกรรมการสอบ
                chair_val.value = get_advisor_name(committee.get("chair_id"))
                committee_val.value = get_advisor_name(committee.get("co_advisor2_id")) # กรรมการ (ร่วม 2)
                member5_val.value = get_advisor_name(committee.get("member5_id"))

                # กรรมการสำรอง
                reserve_ext_val.value = get_advisor_name(committee.get("reserve_external_id"))
                reserve_int_val.value = get_advisor_name(committee.get("reserve_internal_id"))

                page.update()
                
        except Exception as e:
            print(f"Error loading form 6 detail: {e}")

    # --- 3. UI Helper ---
    def create_row(label, value_control):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    width=130, # ปรับความกว้างนิดหน่อยเพราะชื่อฟิลด์ยาว
                    content=ft.Text(label, size=14, color="#888888")
                ),
                ft.Container(
                    expand=True,
                    content=value_control
                )
            ]
        )

    # --- 4. Layout ---
    
    # Card 1: ข้อมูลผู้ยื่นคำร้อง (ยาวเหยียด)
    info_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#08000000", offset=ft.Offset(0, 4)),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("ข้อมูลผู้ยื่นคำร้อง", size=16, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                create_row("คำนำหน้า-ชื่อ-สกุล:", student_name_val),
                create_row("รหัสประจำตัว:", student_id_val),
                create_row("ระดับปริญญา:", degree_val),
                create_row("หลักสูตร/สาขาวิชา:", program_val),
                create_row("ภาควิชา:", dept_val),
                create_row("เริ่มศึกษาภาคเรียนที่:", start_semester_val),
                create_row("ปีการศึกษา:", start_year_val),
                create_row("เบอร์โทร:", phone_val),
                create_row("ที่อยู่ปัจจุบัน:", address_val),
                create_row("สถานที่ทำงาน:", workplace_val),
                ft.Divider(height=10, color="#EEEEEE"),
                create_row("ชื่อวิทยานิพนธ์ (TH):", thesis_th_val),
                create_row("ชื่อวิทยานิพนธ์ (ENG):", thesis_en_val),
            ]
        )
    )

    # Card 2: คณะกรรมการและที่ปรึกษา
    committee_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#08000000", offset=ft.Offset(0, 4)),
        content=ft.Column(
            spacing=12,
            controls=[
                # ส่วนที่ 1: ที่ปรึกษา
                ft.Text("คณะกรรมการสอบและอาจารย์ที่ปรึกษา", size=16, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                create_row("อาจารย์ที่ปรึกษาหลัก:", main_advisor_val),
                create_row("อาจารย์ที่ปรึกษาร่วม 1:", co_advisor_val),
                
                ft.Divider(height=20, color="#EEEEEE"),
                
                # ส่วนที่ 2: กรรมการสอบ
                ft.Text("คณะกรรมการสอบ", size=15, weight="bold", color="black"),
                create_row("ประธานกรรมการสอบ:", chair_val),
                create_row("กรรมการ (ที่ปรึกษาร่วม 2):", committee_val),
                create_row("กรรมการสอบ (คนที่ 5):", member5_val),

                ft.Divider(height=20, color="#EEEEEE"),

                # ส่วนที่ 3: กรรมการสำรอง
                ft.Text("กรรมการสำรอง", size=15, weight="bold", color="black"),
                create_row("กรรมการสำรอง (ภายนอก):", reserve_ext_val),
                create_row("กรรมการสำรอง (ภายใน):", reserve_int_val),
            ]
        )
    )

    load_data()

    return ft.View(
        route=f"/form6/{submission_id}",
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
                            "บันทึกข้อความ: ขอแต่งตั้งคณะกรรมการ\nสอบวิทยานิพนธ์ขั้นสุดท้าย", 
                            size=18, 
                            weight="bold", 
                            color="black", 
                            text_align="center"
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(padding=5),
                    info_card,
                    ft.Container(padding=5),
                    committee_card,
                    ft.Container(padding=20),
                ]
            )
        ]
    )