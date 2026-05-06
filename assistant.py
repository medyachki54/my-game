import subprocess
import json
import sys

def speak(text):
    """Озвучивает текст через динамик телефона"""
    print(f"Ассистент: {text}")
    subprocess.run(["termux-tts-speak", "-l", "ru", text])

def listen():
    """Вызывает голосовой ввод Google и возвращает текст"""
    try:
        # Вызываем окно голосового ввода Android
        result = subprocess.check_output(["termux-speech-to-text"])
        if result:
            text = result.decode("utf-8").lower().strip()
            print(f"Вы сказали: {text}")
            return text
    except Exception:
        print("Ошибка микрофона или ввод отменен.")
    return ""

def execute_command(cmd):
    if not cmd:
        return True

    # --- ГРУППА: УПРАВЛЕНИЕ ЖЕЛЕЗОМ ---
    if "фонарик" in cmd:
        if "включи" in cmd or "вкл" in cmd:
            subprocess.run(["termux-flashlight", "on"])
            speak("Фонарик включен")
        else:
            subprocess.run(["termux-flashlight", "off"])
            speak("Фонарик выключен")

    elif "заряд" in cmd or "батарея" in cmd:
        res = subprocess.check_output(["termux-battery-status"])
        data = json.loads(res)
        speak(f"Заряд батареи {data['percentage']} процентов")

    elif "вибро" in cmd or "вибрируй" in cmd:
        subprocess.run(["termux-vibrate", "-d", "500"])
        speak("Вибрирую")

    # --- ГРУППА: МУЛЬТИМЕДИА И КАМЕРА ---
    elif "фото" in cmd or "сфотографируй" in cmd:
        speak("Внимание, снимаю!")
        subprocess.run(["termux-camera-photo", "-c", "0", "snap.jpg"])
        speak("Фотография сохранена")

    elif "громкость" in cmd:
        # Пример: "громкость 5"
        level = ''.join(filter(str.isdigit, cmd))
        if level:
            subprocess.run(["termux-volume", "music", level])
            speak(f"Уровень громкости изменен на {level}")

    # --- ГРУППА: ИНФОРМАЦИЯ ---
    elif "время" in cmd:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        speak(f"Сейчас {now}")

    elif "где я" in cmd or "локация" in cmd:
        speak("Проверяю координаты, подождите...")
        res = subprocess.check_output(["termux-location"])
        speak("Координаты получены, вывел на экран")
        print(res.decode("utf-8"))

    # --- ВЫХОД ---
    elif "выход" in cmd or "стоп" in cmd:
        speak("До свидания!")
        return False

    elif "помощь" in cmd:
        speak("Я умею управлять фонариком, камерой, проверять заряд и время.")
    
    else:
        speak("Я не знаю такой команды, но я постоянно учусь.")
    
    return True

def main():
    speak("Ассистент запущен. Слушаю вашу команду.")
    
    running = True
    while running:
        # Ждем нажатия Enter в консоли, чтобы начать слушать голос 
        # (это предотвращает бесконечный запуск окна Google)
        input("\nНажмите Enter, чтобы сказать команду...")
        
        user_cmd = listen()
        if user_cmd:
            running = execute_command(user_cmd)

if __name__ == "__main__":
    main()

