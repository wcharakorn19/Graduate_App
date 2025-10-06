import flet as ft

def ProfileScreen(page: ft.Page):
    
    user_data = getattr(page, "user_data", {})
    print("--- Profile Screen ---")
    print("Data from page attribute:", user_data)

    
    profile_avatar = ft.CircleAvatar(
        foreground_image_src="https://flet.dev/images/user-5.png",
        radius=50
    )
    
    student_id_text = ft.Text(user_data.get("student_id", ""), size=14)
    full_name_text = ft.Text(user_data.get("full_name", ""), size=14)
    education_level_text = ft.Text(user_data.get("education_level", ""), size=14)
    program_text = ft.Text(user_data.get("program", ""), size=14)
    department_text = ft.Text(user_data.get("department", ""), size=14)
    faculty_text = ft.Text(user_data.get("faculty", ""), size=14)
    status_text = ft.Text(user_data.get("status", ""), size=14)
    phone_text = ft.Text(user_data.get("phone", ""), size=14)
    email_text = ft.Text(user_data.get("email", ""), size=14)

    
    def _create_field(label, control):
        control.height = 30
        control.text_align = "start"
        return ft.Column(
            spacing=2,
            controls=[ft.Text(label, size=12, color="pink"), control]
        )
    
    def _create_field_pair(label1, control1, label2, control2):
        control1.height = 30; control2.height = 30
        control1.text_align = "start"; control2.text_align = "start"
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(spacing=2, expand=True, controls=[ft.Text(label1, size=12, color="pink"), control1]),
                ft.Column(spacing=2, expand=True, controls=[ft.Text(label2, size=12, color="pink"), control2]),
            ]
        )
    
    # content main Proile
    profile_content = ft.Container(
        width=400, bgcolor="white", border_radius=25, padding=20,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO, spacing=15,
            controls=[
                ft.Stack(
                    [
                        ft.Row([profile_avatar], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([ft.IconButton(icon="exit_to_app", icon_color="pink", on_click=lambda _: page.go("/"))], alignment=ft.MainAxisAlignment.END),
                    ]
                ),
                ft.Text("Profile", size=24, weight="bold", color="pink"),
                _create_field("รหัสนักศึกษา", student_id_text),
                _create_field("ชื่อ-นามสกุล", full_name_text),
                _create_field_pair("ระดับการศึกษา", education_level_text, "หลักสูตร/สาขา", program_text),
                _create_field_pair("ภาควิชา", department_text, "คณะ", faculty_text),
                _create_field_pair("สถานะ", status_text, "เบอร์โทรศัพท์", phone_text),
                _create_field("อีเมล", email_text),
            ]
        )
    )

    def on_nav_change(e):
        selected_index = e.control.selected_index
        if selected_index == 1: 
            page.go("/home")

        elif selected_index == 2:
            page.go("/coctact")

    bottom_nav_bar = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(icon="person_outline", selected_icon="person", label="Profile"),
            ft.NavigationBarDestination(icon="home_outlined", selected_icon="home", label="Home"),
            ft.NavigationBarDestination(icon="chat_bubble_outline", selected_icon="chat_bubble", label="Contact"),
        ],
        on_change=on_nav_change
    )


    return ft.View(
        route="/profile", bgcolor="#f0f0f0", scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.only(top=50, left=20, right=20, bottom=20),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[profile_content],
        navigation_bar=bottom_nav_bar,
    )

