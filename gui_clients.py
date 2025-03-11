# gui_clients.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import ClientManager, ManagerManager

class ClientForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Новый клиент")
        self.client_manager = ClientManager()
        self.manager_manager = ManagerManager()
        
        self.managers = self.manager_manager.get_all_managers()
        manager_names = [f"{m['FirstName']} {m['LastName']}" for m in self.managers]
        
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
        
        tk.Label(self, text="Менеджер:").grid(row=4, column=0, padx=5, pady=5)
        self.manager = ttk.Combobox(self, values=manager_names)
        self.manager.grid(row=4, column=1, padx=5, pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Сохранить", command=self.save).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def save(self):
        manager_index = self.manager.current()
        if manager_index == -1:
            messagebox.showerror("Ошибка", "Выберите менеджера!")
            return
        
        data = (
            self.first_name.get(),
            self.last_name.get(),
            self.email.get(),
            self.phone.get(),
            self.managers[manager_index]['ManagerID']
        )
        self.client_manager.create_client(*data)
        messagebox.showinfo("Успех", "Клиент создан успешно!")
        self.destroy()
        ttk.Button(btn_frame, text="История", 
            command=lambda: InteractionsView(self, client_id)).pack(side=tk.LEFT, padx=5)