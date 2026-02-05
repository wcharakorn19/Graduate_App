import flet as ft
import requests

def ExamResultDetailScreen(page: ft.Page, submission_id: str):
    
    token = page.session.get("token")
    
    # --- 1. เตรียมตัวแปร UI ---
    # กลุ่มข้อมูลนักศึกษา
    student_name_val = ft.Text("-", size=14, color="#333333")
    student_id_val = ft.Text("-", size=14, color="#333333")
    degree_val = ft.Text("-", size=14, color="#333333")
    program_val = ft.Text("-", size=14, color="#333333")
    
    # กลุ่มข้อมูลผลสอบ
    doc_type_val = ft.Text("-", size=14, color="#333333") # ประเภทการยื่น (เช่น ภาษาอังกฤษ ป.โท)
    exam_type_val = ft.Text("-", size=14, color="#333333") # ประเภทการสอบ (เช่น TOEIC)
    exam_date_val = ft.Text("-", size=14, color="#333333") # วันที่สอบ
    
    # คะแนนสอบ (เผื่อมี)
    result_val = ft.Text("-", size=14, color="#333333") 

    # กลุ่มไฟล์แนบ (จะใช้ ListView หรือ Column มาเก็บรายการไฟล์)
    file_list_container = ft.Column(spacing=10)

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
                
                # 2.1 Map ข้อมูลนักศึกษา
                prefix = detail.get("prefix_th") or ""
                first = detail.get("first_name_th") or ""
                last = detail.get("last_name_th") or ""
                student_name_val.value = f"{prefix}{first} {last}"
                
                student_id_val.value = detail.get("student_id", "-")
                degree_val.value = detail.get("degree", "-")
                program_val.value = detail.get("program_name", "-")

                # 2.2 Map ข้อมูลผลสอบ
                doc_type_val.value = detail.get("title", "-") # ชื่อหัวข้อเอกสาร
                
                form_details = detail.get("form_details", {})
                
                # ดึงข้อมูลตามประเภท
                exam_type_val.value = form_details.get("exam_type", "-")
                exam_date_val.value = form_details.get("exam_date", "-")
                
                # ดึงผลสอบ/คะแนน (ถ้ามี)
                if "result" in form_details:
                    result_val.value = form_details.get("result", "-")
                elif "total_score" in form_details:
                    result_val.value = str(form_details.get("total_score", "-"))
                else:
                    result_val.value = "-"

                # 2.3 Map ไฟล์แนบ (พร้อมระบบเปิดไฟล์)
                files = form_details.get("files", [])
                file_list_container.controls.clear()
                
                # Base URL ของ Server (สำหรับต่อกับ Path ไฟล์)
                base_url = "http://127.0.0.1:3000"
                
                if files:
                    for f in files:
                        file_name = f.get("name", "Unknown File")
                        file_path = f.get("path", "")
                        
                        # สร้าง Link เต็มๆ
                        full_url = f"{base_url}{file_path}"
                        
                        # สร้าง UI สำหรับแต่ละไฟล์
                        file_row = ft.Container(
                            padding=10,
                            bgcolor="#F9F9F9",
                            border_radius=10,
                            # ✅ คลิกแล้วเปิด Browser
                            on_click=lambda e, url=full_url: page.launch_url(url),
                            content=ft.Row([
                                ft.Icon(ft.icons.INSERT_DRIVE_FILE, color="#5E5CE6", size=30),
                                ft.Column([
                                    ft.Text(file_name, size=14, color="#333333", weight="bold", overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Text("แตะเพื่อเปิดไฟล์", size=12, color="grey")
                                ], spacing=2)
                            ], alignment=ft.MainAxisAlignment.START)
                        )
                        file_list_container.controls.append(file_row)
                else:
                    file_list_container.controls.append(ft.Text("ไม่มีไฟล์แนบ", size=14, color="grey"))

                page.update()
                
        except Exception as e:
            print(f"Error loading exam detail: {e}")

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

    # --- 4. Layout ---
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
            ]
        )
    )

    exam_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#08000000", offset=ft.Offset(0, 4)),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("ข้อมูลผลสอบ", size=16, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                create_row("ประเภทเอกสาร:", doc_type_val),
                create_row("ประเภทการสอบ:", exam_type_val),
                create_row("วันที่สอบ:", exam_date_val),
                create_row("ผลสอบ/คะแนน:", result_val),
            ]
        )
    )

    file_card = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=15, color="#08000000", offset=ft.Offset(0, 4)),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("หลักฐานยื่นสอบ", size=16, weight="bold", color="black"),
                ft.Divider(height=10, color="transparent"),
                file_list_container # รายการไฟล์จะโชว์ตรงนี้
            ]
        )
    )

    load_data()

    return ft.View(
        route=f"/exam_result/{submission_id}",
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
                            "รายละเอียดการยื่นผลสอบ", 
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
                    exam_card,
                    ft.Container(padding=5),
                    file_card,
                    ft.Container(padding=20),
                ]
            )
        ]
    )