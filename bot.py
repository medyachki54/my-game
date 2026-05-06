import flet as ft
from logic import AssistantCore

def main(page: ft.Page):
    page.title = "AI Assistant"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    core = AssistantCore()
    chat = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)

    def send_message(e):
        if not message_input.value:
            return
        
        # Сообщение пользователя
        chat.controls.append(ft.Text(f"Вы: {message_input.value}", weight="bold"))
        
        # Ответ ассистента
        response = core.get_response(message_input.value)
        chat.controls.append(ft.Text(f"Ассистент: {response}", italic=True))
        
        message_input.value = ""
        page.update()

    message_input = ft.TextField(hint_text="Введите сообщение...", expand=True)
    send_button = ft.IconButton(icon=ft.icons.SEND, on_click=send_message)

    page.add(
        ft.Container(content=chat, expand=True),
        ft.Row([message_input, send_button])
    )

# Для запуска как мобильного приложения используется flet.app(target=main)
if __name__ == "__main__":
    ft.app(target=main)

