import flet as ft
import requests
import json

def FormFiveDetailScreen(page: ft.Page, submission_id: str):
    
    token = page.session.get("token")
    
    # --- UI Components ---
    student_name_val = ft.Text("-", size=14, color="#333333")
    student_id_val = ft.Text("-", size=14, color="#333333")
    degree_val = ft.Text("-", size=14, color="#333333")
    program_val = ft.Text("-", size=14, color="#333333")
    dept_val = ft.Text("-", size=14, color="#333333")

    approve_date_val = ft.Text("-", size=14, color="#333333")
    title_th_val = ft.Text("-", size=14, color="#333333")
    title_en_val = ft.Text("-", size=14, color="#333333")

    # Checkbox (Read-only)
    check_questionnaire = ft.Checkbox(label="แบบสอบถาม", value=False, disabled=True, label_style=ft.TextStyle(color="black"))
    check_test = ft.Checkbox(label="แบบทดสอบ", value=False, disabled=True, label_style=ft.TextStyle(color="black"))
    check_teaching = ft.Checkbox(label="ทดลองสอน", value=False, disabled=True, label_style=ft.TextStyle(color="black"))
    check_other = ft.Checkbox(label="อื่นๆ:", value=False, disabled=True, label_style=ft.TextStyle(color="black"))
    other_detail_val = ft.Text("", size=14, color="#333333")

    # --- ฟังก์ชันดึงข้อมูล ---
    def load_data():
        if not token: return
        
        try:
            # ใช้ URL ตาม server.js บรรทัด 1475
            api_url = f"http://127.0.0.1:3000/api/submissions/{submission_id}"
            headers = {"Authorization": f"Bearer {token}"}
            res = requests.get(api_url, headers=headers)
            
            if res.status_code == 200:
                data = res.json()
                detail = data.get("documentDetail", {})
                
                # Debug: ปริ้นท์ดูโครงสร้างข้อมูลจริงที่ส่งมาจาก Server
                print(f"--- DEBUG FORM 5 DATA (ID: {submission_id}) ---")
                # print(json.dumps(detail, indent=2, ensure_ascii=False)) 
                
                # 1. Map ข้อมูลนักศึกษา
                prefix = detail.get("prefix_th") or ""
                first = detail.get("first_name_th") or ""
                last = detail.get("last_name_th") or ""
                student_name_val.value = f"{prefix}{first} {last}"
                
                student_id_val.value = detail.get("student_id", "-")
                degree_val.value = detail.get("degree", "-")
                program_val.value = detail.get("program_name", "-")
                dept_val.value = detail.get("department_name", "-")

                # 2. Map ข้อมูลฟอร์ม
                form_details = detail.get("form_details", {})
                
                # print("Form Details:", form_details) # เอาไว้ดูชื่อ Key

                approve_date_val.value = form_details.get("approved_date") or detail.get("updated_at", "-")[:10]
                title_th_val.value = form_details.get("thesis_title_th", "-")
                title_en_val.value = form_details.get("thesis_title_en", "-")

                # --- 3. Logic จัดการ Checkbox (ทำให้ยืดหยุ่นขึ้น) ---
                # พยายามหา Key ที่น่าจะเป็นไปได้ทั้งหมด
                methods = (
                    form_details.get("collection_methods") or 
                    form_details.get("methods") or 
                    form_details.get("collection_type") or 
                    []
                )
                
                # แปลงเป็น String เพื่อเช็คได้ง่ายขึ้น (เผื่อส่งมาเป็น JSON String)
                methods_str = str(methods).lower()
                print(f"Methods Found: {methods_str}") # ดูซิว่าได้ค่าอะไรมา

                # เช็คคำสำคัญ (Keyword Checking) - ปลอดภัยกว่าการเช็ค Key เป๊ะๆ
                # เช็คแบบสอบถาม
                check_questionnaire.value = (
                    "questionnaire" in methods_str or 
                    "แบบสอบถาม" in methods_str
                )
                
                # เช็คแบบทดสอบ
                check_test.value = (
                    "test" in methods_str or 
                    "แบบทดสอบ" in methods_str
                )
                
                # เช็คทดลองสอน
                check_teaching.value = (
                    "teaching" in methods_str or 
                    "experiment" in methods_str or
                    "ทดลองสอน" in methods_str
                )
                
                # เช็คอื่นๆ
                check_other.value = (
                    "other" in methods_str or 
                    "อื่นๆ" in methods_str
                )
                
                if check_other.value:
                    other_detail_val.value = form_details.get("other_method_detail") or form_details.get("other_detail") or "-"

                page.update()
                
        except Exception as e:
            print(f"Error loading form 5 detail: {e}")

    # --- UI Helper ---
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

    # --- Layout ---
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

    permission_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#08000000", offset=ft.Offset(0, 4)),
        content=ft.Column(
            spacing=5,
            controls=[
                ft.Text("รายละเอียดการขออนุญาต", size=16, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                check_questionnaire,
                check_test,
                check_teaching,
                ft.Row([
                    check_other,
                    ft.Container(content=other_detail_val, margin=ft.margin.only(top=2))
                ])
            ]
        )
    )

    load_data()

    return ft.View(
        route=f"/form5/{submission_id}",
        bgcolor="#FFF5F7",
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
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=20, right=20, bottom=10),
                        content=ft.Text(
                            "แบบขอหนังสือขออนุญาตเก็บรวบรวมข้อมูล", 
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
                    permission_card,
                    ft.Container(padding=20),
                ]
            )
        ]
    )