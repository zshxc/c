# gui_managers.py
import tkinter as tk
from tkinter import messagebox
from database import ManagerManager

class ManagerForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Новый менеджер")
        self.manager_manager = ManagerManager()
        
        tk.Label(self, text="Имя:").grid(row=0, column=0, padx=5, pady=5)
        self.first_name = tk.Entry(self)
        self.first_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Фамилия:").grid(row=1, column=0, padx=5, pady=5)
        self.last_name = tk.Entry(self)
        self.last_name.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email = tk.Entry(self)
        self.email.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Телефон:").grid(row=3, column=0, padx=5, pady=5)
        self.phone = tk.Entry(self)
        self.phone.grid(row=3, column=1, padx=5, pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Сохранить", command=self.save).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def save(self):
        data = (
            self.first_name.get(),
            self.last_name.get(),
            self.email.get(),
            self.phone.get()
        )
        self.manager_manager.create_manager(*data)
        messagebox.showinfo("Успех", "Менеджер создан успешно!")
        self.destroy()