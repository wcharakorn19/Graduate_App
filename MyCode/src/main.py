# src/main.py
import flet as ft
from screens.login_screen import LoginScreen


# Setup App 
def main(page: ft.Page):
    page.title = "Graduate Student Tracking System"
    page.window.width = 430
    page.window.height = 832

    # Setup Navigation and Routing
    def route_change(route):
        page.views.clear()


        if page.route == "/login":
            page.views.append(LoginScreen(page))


        page.update()

    page.on_route_change = route_change

    page.go("/login")




ft.app(target=main, assets_dir="assets")