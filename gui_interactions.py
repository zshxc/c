import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import InteractionManager, ClientManager

class InteractionForm(tk.Toplevel):
    def __init__(self, parent, client_id=None):
        super().__init__(parent)
        self.title("Новое взаимодействие")
        self.geometry("400x300")
        
        self.client_manager = ClientManager()
        self.interaction_manager = InteractionManager()
        self.client_id = client_id
        
        self._create_widgets()
        self._setup_layout()
        self._load_data()

    def _create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.lbl_client = ttk.Label(self.main_frame, text="Клиент:")
        self.client_combo = ttk.Combobox(self.main_frame, state="readonly")
        
        self.lbl_contact = ttk.Label(self.main_frame, text="Контактное лицо:")
        self.entry_contact = ttk.Entry(self.main_frame)
        
        self.lbl_type = ttk.Label(self.main_frame, text="Тип:")
        self.type_combo = ttk.Combobox(self.main_frame, values=['call', 'meeting'], state="readonly")
        
        self.lbl_date = ttk.Label(self.main_frame, text="Дата:")
        self.entry_date = ttk.Entry(self.main_frame)
        
        self.lbl_content = ttk.Label(self.main_frame, text="Содержание:")
        self.entry_content = ttk.Entry(self.main_frame)
        
        self.btn_save = ttk.Button(self.main_frame, text="Сохранить", command=self.save)
        self.btn_cancel = ttk.Button(self.main_frame, text="Отмена", command=self.destroy)

    def _setup_layout(self):
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        rows = [
            (self.lbl_client, self.client_combo),
            (self.lbl_contact, self.entry_contact),
            (self.lbl_type, self.type_combo),
            (self.lbl_date, self.entry_date),
            (self.lbl_content, self.entry_content)
        ]
        
        for row, (label, field) in enumerate(rows):
            label.grid(row=row, column=0, sticky='e', padx=5, pady=5)
            field.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        
        self.btn_save.grid(row=5, column=1, sticky='e', padx=5, pady=10)
        self.btn_cancel.grid(row=5, column=0, sticky='e', padx=5, pady=10)

    def _load_data(self):
        if self.client_id:
            clients = self.client_manager.get_all_clients()
            for idx, c in enumerate(clients):
                if c['ClientID'] == self.client_id:
                    self.client_combo.current(idx)
                    self.client_combo.config(state='disabled')
                    break
        else:
            self.client_combo['values'] = [
                f"{c['FirstName']} {c['LastName']}" 
                for c in self.client_manager.get_all_clients()
            ]
        
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))

    def save(self):
        try:
            data = {
                'client_id': self.client_id or self.client_manager.get_all_clients()[self.client_combo.current()]['ClientID'],
                'contact_person': self.entry_contact.get(),
                'interaction_type': self.type_combo.get(),
                'interaction_date': self.entry_date.get(),
                'content': self.entry_content.get()
            }
            
            if not all(data.values()):
                raise ValueError("Все поля обязательны для заполнения")
                
            self.interaction_manager.create_interaction(**data)
            messagebox.showinfo("Успех", "Взаимодействие сохранено")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

class InteractionsView(tk.Toplevel):
    def __init__(self, parent, client_id=None):
        super().__init__(parent)
        self.title("История взаимодействий")
        self.geometry("800x400")
        
        self.interaction_manager = InteractionManager()
        self.client_id = client_id
        
        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('date', 'type', 'contact', 'content'), show='headings')
        self.tree.heading('date', text='Дата')
        self.tree.heading('type', text='Тип')
        self.tree.heading('contact', text='Контакт')
        self.tree.heading('content', text='Содержание')
        
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        btn_frame = ttk.Frame(self)
        btn_new = ttk.Button(btn_frame, text="Добавить", command=self.add_interaction)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        btn_frame.pack(pady=5)
        btn_new.pack()

    def _load_data(self):
        interactions = self.interaction_manager.get_interactions(self.client_id)
        for interaction in interactions:
            self.tree.insert('', 'end', values=(
                interaction['InteractionDate'].strftime("%Y-%m-%d %H:%M"),
                'Звонок' if interaction['InteractionType'] == 'call' else 'Встреча',
                interaction['ContactPerson'],
                interaction['Content'][:50] + '...'  # Обрезка длинного текста
            ))

    def add_interaction(self):
        InteractionForm(self, self.client_id)
        self._load_data()