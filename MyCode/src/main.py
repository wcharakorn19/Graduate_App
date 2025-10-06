import flet as ft
from src.screens.welcome_screen import WelcomeScreen
from src.screens.login_screen import LoginScreen
from src.screens.contact_screen import ContactScreen
from src.screens.profile_screen import ProfileScreen
from src.screens.home_screen import HomeScreen


# Setup App 
def main(page: ft.Page):
    page.title = "Graduate Student Tracking System"
    page.window.width = 430
    page.window.height = 832

    # Setup Navigation and Routing
    def route_change(route):
        t_route = ft.TemplateRoute(page.route)

        if t_route.match("/"):
            page.views.clear()
            page.views.append(WelcomeScreen(page))

        elif t_route.match("/login"):
            page.views.append(LoginScreen(page))

        elif t_route.match("/home"):
            page.views.append(HomeScreen(page))

        elif t_route.match("/contact"):
            page.views.append(ContactScreen(page))

        elif t_route.match("/profile"):
            page.views.append(ProfileScreen(page))
            
        #elif t_route.match("/teacher_dashboard"):
            #page.views.append(TeacherDashboardScreen(page)) #ใส่ไว้รอหน้าจารย์
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/")




ft.app(target=main, assets_dir="assets")