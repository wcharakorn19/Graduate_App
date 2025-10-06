import flet as ft

def ContactScreen(page: ft.Page):

    def create_contact_card(icon_widget, label, value, bg_color):
        return ft.Card(
            content=ft.Container(
                padding=ft.padding.all(15),
                bgcolor=bg_color,
                border_radius=ft.border_radius.all(10),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Container(
                            content=icon_widget,
                            alignment=ft.alignment.center,
                            width=60,
                            height=60,
                        ),
                        ft.Container(
                            padding=ft.padding.only(left=10),
                            content=ft.Column(
                                spacing=0,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                controls=[
                                    ft.Text(label, size=14, color="black"),
                                    ft.Text(value, size=16, weight="bold", color="black"),
                                ]
                            )
                        )
                    ]
                )
            )
        )

    # main content contact
    contact = ft.Container(
        bgcolor="white", 
        width=350,
        border_radius=25, 
        padding=20,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.START, 
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
            controls=[
                ft.Container(
                    content=ft.Text("Contact Staff", size=24, weight="bold"),
                    padding=ft.padding.only(left=10)
                ),
                create_contact_card(
                    icon_widget=ft.Container(
                        width=50, height=50, bgcolor="black", border_radius=ft.border_radius.all(10),
                        content=ft.Text("LINE", color="white", weight="bold", size=21),
                        alignment=ft.alignment.center
                    ),
                    label="Line ID:", value="Watcharakorn19", bg_color="#a5d6a7" 
                ),
                create_contact_card(
                    icon_widget=ft.Container(
                        width=50, height=50, bgcolor="#4caf50", shape=ft.BoxShape.CIRCLE,
                        content=ft.Icon(name="call", color="white"),
                        alignment=ft.alignment.center
                    ),
                    label="เบอร์ติดต่อ:", value="000-001-1000", bg_color="#f48fb1" 
                ),
                create_contact_card(
                    icon_widget=ft.Container(
                        width=50, height=50, bgcolor="white", border_radius=ft.border_radius.all(10),
                        content=ft.Icon(name="email", color="black"),
                        alignment=ft.alignment.center
                    ),
                    label="Email:", value="N19@gamil.com", bg_color="#757575" 
                ),
            ]
        )
    )


    def on_nav_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.go("/profile")
        elif selected_index == 1:
            page.go("/home")
        # สามารถเพิ่มเงื่อนไขสำหรับปุ่มอื่นๆ ได้ในอนาคต

    bottom_nav_bar = ft.NavigationBar(
        selected_index=1,
        destinations=[
            ft.NavigationBarDestination(icon="person_outline", selected_icon="person", label="Profile"),
            ft.NavigationBarDestination(icon="home_outlined", selected_icon="home", label="Home"),
            ft.NavigationBarDestination(icon="chat_bubble_outline", selected_icon="chat_bubble", label="Contact"),
        ],
        on_change=on_nav_change
    )

    return ft.View(
        route="/contact",
        bgcolor="#f0f0f0",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.START,
        padding=ft.padding.only(top=50),
        controls=[
            contact
        ],
        navigation_bar=bottom_nav_bar
    )

