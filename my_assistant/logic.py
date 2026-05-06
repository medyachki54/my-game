import sqlite3

class AssistantCore:
    def __init__(self, db_name="assistant_data.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        # Создаем таблицу для истории, если её нет
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS history 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             role TEXT, 
                             content TEXT)''')

    def save_message(self, role, content):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO history (role, content) VALUES (?, ?)", (role, content))

    def get_history(self):
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute("SELECT role, content FROM history").fetchall()

    def get_response(self, user_input: str) -> str:
        # Сохраняем то, что сказал пользователь
        self.save_message("user", user_input)
        
        # Простая логика ответа (потом заменим на нейросеть)
        user_text = user_input.lower()
        if "привет" in user_text:
            ans = "Привет! Я твой будущий Android-ассистент. Я тебя слышу!"
        elif "как дела" in user_text:
            ans = "Отлично, обживаюсь в твоем телефоне. База данных готова!"
        else:
            ans = f"Я запомнил твое сообщение: {user_input}"
        
        # Сохраняем ответ ассистента
        self.save_message("assistant", ans)
        return ans

