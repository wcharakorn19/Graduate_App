# src/login_screen.py
import flet as ft

# LoginScreen function
def LoginScreen(page: ft.Page):

    def show_login_sheet(e):
        print("WELCOME button is pressed!")
        # open ButtomSheet (coming)

    
    welcome_view = ft.Container(
        bgcolor=ft.Colors.AMBER,
        width=400,
        height=500,
        content=ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
            controls=[
                ft.Image(src="logo.png"),
                ft.ElevatedButton(
                    bgcolor=ft.Colors.PINK_400,
                    on_click=show_login_sheet,
                    text="WELCOME",
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLACK87
                    )
                ),
                ft.Text(
                    "Graduate Student Tracking System",
                    size=30,
                    color=ft.Colors.PINK_200

                )
            ]
        )
    )


    return ft.View(
        route="/login",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.END,
        bgcolor=ft.Colors.WHITE,
        controls=[
            welcome_view
        ]
    )