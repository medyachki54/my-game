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
        height=400,          # Добавили фиксированную высоту, чтобы не растягивалось
        bgcolor="#1A1A1B",   
        padding=40,
        border_radius=30,
        alignment=ft.alignment.center, # Центрируем содержимое внутри карточки
        content=ft.Column(
            [
                # Иконка
                ft.Icon(
                    "pets", 
                    color=ft.colors.WHITE, # Поменял на белый, чтобы было видно на темном
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
            alignment=ft.MainAxisAlignment.CENTER, # Центрируем элементы в колонке
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

