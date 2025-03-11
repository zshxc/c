import tkinter as tk
from tkinter import ttk, messagebox
from database import DeduplicationManager

class DeduplicationView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Дедупликация клиентов")
        self.geometry("1000x600")
        
        self.deduplication_manager = DeduplicationManager()
        
        self._create_widgets()
        self._setup_layout()
        self.load_duplicates()

    def _create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Таблица дубликатов
        self.tree = ttk.Treeview(self.main_frame, 
                               columns=('type', 'client1', 'client2', 'matches'), 
                               show='headings')
        self.tree.heading('type', text='Тип совпадения')
        self.tree.heading('client1', text='Клиент 1')
        self.tree.heading('client2', text='Клиент 2')
        self.tree.heading('matches', text='Совпадающие поля')
        
        # Полоса прокрутки
        self.scroll = ttk.Scrollbar(self.main_frame, 
                                  orient="vertical", 
                                  command=self.tree.yview)
        
        # Кнопки управления
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_refresh = ttk.Button(self.btn_frame, 
                                    text="Обновить", 
                                    command=self.load_duplicates)
        self.btn_merge = ttk.Button(self.btn_frame, 
                                  text="Объединить", 
                                  command=self.merge_selected)

    def _setup_layout(self):
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Таблица
        self.tree.grid(row=0, column=0, sticky='nsew', pady=5)
        self.scroll.grid(row=0, column=1, sticky='ns')
        
        # Кнопки
        self.btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        self.btn_merge.pack(side=tk.LEFT, padx=5)
        
        # Настройка столбцов
        self.tree.column('type', width=100, anchor='center')
        self.tree.column('client1', width=200)
        self.tree.column('client2', width=200)
        self.tree.column('matches', width=300)
        
        self.tree.configure(yscrollcommand=self.scroll.set)

    def load_duplicates(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            duplicates = self.deduplication_manager.find_duplicates()
            if not duplicates:
                messagebox.showinfo("Информация", "Дубликаты не найдены")
                return
                
            for dup in duplicates:
                client1 = f"{dup['details']['names'][0]} | {dup['details']['emails'][0]} | {dup['details']['phones'][0]}"
                client2 = f"{dup['details']['names'][1]} | {dup['details']['emails'][1]} | {dup['details']['phones'][1]}"
                matches = self._get_match_details(dup)
                
                self.tree.insert('', 'end', values=(
                    dup['type'].capitalize(),
                    client1,
                    client2,
                    ', '.join(matches)
                ), tags=('duplicate',))
                
            self.tree.tag_configure('duplicate', background='#ffe6e6')
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _get_match_details(self, duplicate):
        matches = []
        details = duplicate['details']
        
        if details['emails'][0] == details['emails'][1] and details['emails'][0]:
            matches.append("Email")
        if details['phones'][0] == details['phones'][1] and details['phones'][0]:
            matches.append("Телефон")
        if details['names'][0] == details['names'][1]:
            matches.append("Имя")
            
        return matches

    def merge_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите запись для объединения")
            return
            
        # Реализация объединения записей
        # (дополнительный функционал может быть добавлен по необходимости)
        messagebox.showinfo("Информация", "Функция объединения в разработке")

if __name__ == "__main__":
    root = tk.Tk()
    DeduplicationView(root)
    root.mainloop()