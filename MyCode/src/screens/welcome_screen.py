# src/login_screen.py
import flet as ft

# LoginScreen function
def WelcomeScreen(page: ft.Page):

    def show_login_sheet(e):
        print("WELCOME button is pressed!")
        # open ButtomSheet (coming)

    
    welcome_view = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                margin=ft.margin.only(left=23, right=23),
                content=ft.Image(src="logo.png")
            ),
            ft.Container(
                margin=ft.margin.only(bottom=150, top=70),
                content=ft.ElevatedButton(
                    text="WELCOME",
                    bgcolor=ft.Colors.PINK_300,
                    width=150,
                    height=65,
                    on_click=lambda _: page.go("/login"),
                ),
            ),
            ft.Container(
                width=306,
                margin=ft.margin.only(bottom=20),
                alignment=ft.alignment.center,
                content=ft.Text("Graduate Student Tracking System", color=ft.Colors.PINK_400, size=18)
            )
        ]
    )


    return ft.View(
        route="/",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.END,
        bgcolor=ft.Colors.WHITE,
        controls=[
            welcome_view
            ]
    )
