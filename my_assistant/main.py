import flet as ft

def main(page: ft.Page):
    # Настройки страницы
    page.title = "My Assistant"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#4B0082" 
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Создаем контейнер-карточку
    content_box = ft.Container(
        width=300,           
        bgcolor="#1A1A1B",   
        padding=40,
        border_radius=30,
        content=ft.Column(
            [
                # ИСПРАВЛЕНО: просто строка "pets" без лишних аргументов
                ft.Icon(
                    "pets", 
                    color="black", 
                    size=80
                ),
                # Главный текст
                ft.Text(
                    "BLACK CAT ASSISTANT", 
                    size=20, 
                    weight="bold", 
                    color="grey400",
                    text_align=ft.TextAlign.CENTER
                ),
                # Статус
                ft.Text(
                    "Система активна", 
                    color="grey500"
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

    # Добавляем всё на страницу
    page.add(content_box)

if __name__ == "__main__":
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        port=8550, 
        host="0.0.0.0"
    )

