import flet as ft
from src.core.real_api_client import RealApiClient

def LoginScreen(page: ft.Page):
    
    api_client = RealApiClient()

    logo_image = ft.Image(
        src="logo_1.jpeg",
        width=150,
        height=150,
        fit=ft.ImageFit.CONTAIN,
        border_radius=ft.border_radius.all(75) 
    )

    email_field = ft.TextField(
        label="E-mail Account",
        border_radius=10,
        bgcolor="white",
        border_color="transparent",
        height=50,
        text_size=14
    )
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        border_radius=10,
        bgcolor="white",
        border_color="transparent",
        height=50,
        text_size=14
    )
    
    def do_login(e):
        email = email_field.value
        password = password_field.value
        response = api_client.post(
            endpoint="/login",
            data={"email": email, "password": password}
        )

        if response.status_code == 200:
            user_data = response.json()
            page.user_data = user_data
            page.go("/profile")
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("E-mail หรือ Password ไม่ถูกต้อง!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()

    login_button = ft.ElevatedButton(
        text="Login",
        bgcolor="#e91e63",
        color="white",
        width=300,
        height=50,
        on_click=do_login
    )

    top_content = ft.Container(
        height=250,
        alignment=ft.alignment.center,
        content=logo_image
    )

    bottom_content = ft.Container(
        expand=True,
        bgcolor="#fce4ec",
        border_radius=ft.border_radius.vertical(top=30),
        padding=ft.padding.only(top=40),
        alignment=ft.alignment.top_center,
        content=ft.Container(
            width=350,
            bgcolor="#e0e0e0",
            border_radius=20,
            padding=30,
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Text("ยืนยันตัวตนด้วยบริการของสถาบันฯ", size=16, weight=ft.FontWeight.BOLD, color="black"),
                    ft.Text("โดยใช้ E-mail Account ของสถาบันฯ", size=12, color="black"),
                    email_field,
                    password_field,
                    ft.Container(height=10), 
                    login_button,
                ]
            )
        )
    )

    return ft.View(
        route="/login",
        padding=0,
        bgcolor="white",
        appbar=ft.AppBar(
            leading=ft.IconButton(
                icon="arrow_back",
                on_click=lambda _: page.go("/")
            ),
            title=ft.Text("KMITL"),
            center_title=True,
            bgcolor="white"
        ),
        controls=[
            ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    top_content,
                    bottom_content
                ]
            )
        ]
    )

