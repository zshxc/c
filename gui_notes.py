# gui_notes.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import NoteManager, ClientManager

class NoteForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Добавить заметку")
        self.note_manager = NoteManager()
        self.client_manager = ClientManager()
        
        self.clients = self.client_manager.get_all_clients()
        if not self.clients:
            messagebox.showerror("Ошибка", "Нет клиентов в базе!")
            self.destroy()
            return
        
        client_names = [f"{c['FirstName']} {c['LastName']} (ID: {c['ClientID']})" 
                      for c in self.clients]
        
        tk.Label(self, text="Клиент:").grid(row=0, column=0, padx=5, pady=5)
        self.client_combo = ttk.Combobox(self, values=client_names, state="readonly")
        self.client_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Текст заметки:").grid(row=1, column=0, padx=5, pady=5)
        self.note_text = tk.Text(self, width=40, height=10)
        self.note_text.grid(row=1, column=1, padx=5, pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Сохранить", command=self.save).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def save(self):
        client_index = self.client_combo.current()
        note_text = self.note_text.get("1.0", tk.END).strip()
        
        if client_index == -1:
            messagebox.showerror("Ошибка", "Выберите клиента!")
            return
        if not note_text:
            messagebox.showerror("Ошибка", "Введите текст заметки!")
            return
            
        client_id = self.clients[client_index]['ClientID']
        self.note_manager.create_note(client_id, note_text)
        messagebox.showinfo("Успех", "Заметка добавлена успешно!")
        self.destroy()

class NotesViewer(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Просмотр заметок")
        self.note_manager = NoteManager()
        self.client_manager = ClientManager()
        
        self.clients = self.client_manager.get_all_clients()
        client_names = [f"{c['FirstName']} {c['LastName']}" for c in self.clients]
        
        tk.Label(self, text="Клиент:").grid(row=0, column=0, padx=5, pady=5)
        self.client_combo = ttk.Combobox(self, values=client_names, state="readonly")
        self.client_combo.grid(row=0, column=1, padx=5, pady=5)
        self.client_combo.bind("<<ComboboxSelected>>", self.load_notes)
        
        self.notes_list = tk.Listbox(self, width=60, height=15)
        self.notes_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
    def load_notes(self, event):
        client_index = self.client_combo.current()
        if client_index == -1:
            return
            
        client_id = self.clients[client_index]['ClientID']
        notes = self.note_manager.get_notes_by_client(client_id)
        self.notes_list.delete(0, tk.END)
        
        for note in notes:
            date = note['CreatedAt'].strftime("%Y-%m-%d %H:%M")
            self.notes_list.insert(tk.END, f"[{date}] {note['NoteText']}")