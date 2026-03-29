import customtkinter as ctk
from logic import DataManager

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.dm = DataManager()
        
        self.title("AI Tutor - Метод Аналогий")
        self.geometry("800x600")

        # Настройка сетки
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Боковая панель управления
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="📚 MathSteps", font=("Arial", 24, "bold"))
        self.logo.pack(pady=20, padx=10)

        # Выпадающие списки
        self.grade_cb = self.create_menu("Выбери класс", self.dm.get_grades(), self.update_subjects)
        self.subject_cb = self.create_menu("Выбери предмет", [], self.update_books)
        self.book_cb = self.create_menu("Выбери учебник", [], self.update_topics)
        self.topic_cb = self.create_menu("Выбери тему", [], self.update_exercises)
        self.ex_cb = self.create_menu("Выбери задание", [], self.show_result)

        # Основная область
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.title_label = ctk.CTkLabel(self.main_content, text="Инструкция", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=(0, 10), anchor="w")

        self.info_text = ctk.CTkTextbox(self.main_content, font=("Arial", 16), corner_radius=10)
        self.info_text.pack(fill="both", expand=True)
        self.info_text.insert("0.0", "Привет! Выбери параметры в меню слева, чтобы получить разбор аналогичного задания.")

    def create_menu(self, placeholder, values, command):
        menu = ctk.CTkOptionMenu(self.sidebar, values=values, command=command)
        menu.set(placeholder)
        menu.pack(pady=10, padx=20, fill="x")
        return menu

    # Логика каскадного обновления
    def update_subjects(self, val):
        subjects = self.dm.get_subjects(val)
        self.subject_cb.configure(values=subjects)
        self.subject_cb.set("Выбери предмет")

    def update_books(self, val):
        books = self.dm.get_books(self.grade_cb.get(), val)
        self.book_cb.configure(values=books)
        self.book_cb.set("Выбери учебник")

    def update_topics(self, val):
        topics = self.dm.get_topics(self.grade_cb.get(), self.subject_cb.get(), val)
        self.topic_cb.configure(values=topics)
        self.topic_cb.set("Выбери тему")

    def update_exercises(self, val):
        exs = self.dm.get_exercises(self.grade_cb.get(), self.subject_cb.get(), self.book_cb.get(), val)
        self.ex_cb.configure(values=exs)
        self.ex_cb.set("Выбери задание")

    def show_result(self, val):
        data = self.dm.get_details(
            self.grade_cb.get(), self.subject_cb.get(), 
            self.book_cb.get(), self.topic_cb.get(), val
        )
        
        res = f"ТВОЕ ЗАДАНИЕ: {data['original']}\n"
        res += "─" * 30 + "\n"
        res += f"РАЗБИРАЕМ АНАЛОГИЧНЫЙ ПРИМЕР: {data['analogy_task']}\n\n"
        res += "\n".join(data['steps'])
        res += "\n\n" + "─" * 30 + "\n"
        res += "Теперь попробуй решить свой пример по этому же алгоритму!"
        
        self.title_label.configure(text=f"Разбор: {val}")
        self.info_text.delete("0.0", "end")
        self.info_text.insert("0.0", res)

app = App()
app.mainloop()