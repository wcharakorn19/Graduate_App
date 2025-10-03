# src/login_screen.py
import flet as ft

# LoginScreen function
def WelcomeScreen(page: ft.Page):

    def show_login_sheet(e):
        print("WELCOME button is pressed!")
        # open ButtomSheet (coming)

    
    welcome_view = ft.Container(
        bgcolor=ft.Colors.AMBER,
        width=500,
        height=750,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=0,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    width=200,
                    margin=ft.margin.only(top=350),

                    content=ft.Image(src="logo.png")
                ),
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    margin=ft.margin.only(top=30),
                    
                    content=ft.ElevatedButton(
                        text="WELCOME",
                        bgcolor=ft.Colors.PINK_300,
                        on_click=lambda _: page.go("/login"),
                        style=ft.ButtonStyle(color=ft.Colors.BLACK87)
                    )
                ),
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    content=ft.Text(
                        "Graduate Student Tracking System",
                        size=20,
                        color=ft.Colors.PINK_300,
                    )
                ),
            ]
        )
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