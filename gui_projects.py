# gui_projects.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import ProjectManager, ClientManager, ManagerManager

class ProjectForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Новый проект")
        self.geometry("500x350")
        
        self.project_manager = ProjectManager()
        self.client_manager = ClientManager()
        self.manager_manager = ManagerManager()
        
        self.clients = self.client_manager.get_all_clients()
        self.managers = self.manager_manager.get_all_managers()
        
        self._create_widgets()
        self._setup_layout()
        self._center_window()
        
    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def _create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Клиент
        self.lbl_client = ttk.Label(self.main_frame, text="Клиент:")
        self.client_combo = ttk.Combobox(self.main_frame, state="readonly")
        self.client_combo['values'] = [
            f"{c['FirstName']} {c['LastName']}" 
            for c in self.clients
        ]
        self.client_combo.bind("<<ComboboxSelected>>", self._update_manager)
        # gui_projects.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import ProjectManager, ClientManager, ManagerManager

class ProjectForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Новый проект")
        self.geometry("500x350")
        
        self.project_manager = ProjectManager()
        self.client_manager = ClientManager()
        self.manager_manager = ManagerManager()
        
        self.clients = self.client_manager.get_all_clients()
        self.managers = self.manager_manager.get_all_managers()
        
        self._create_widgets()
        self._setup_layout()
        self._center_window()
        
    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def _create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Клиент
        self.lbl_client = ttk.Label(self.main_frame, text="Клиент:")
        self.client_combo = ttk.Combobox(self.main_frame, state="readonly")
        self.client_combo['values'] = [
            f"{c['FirstName']} {c['LastName']}" 
            for c in self.clients
        ]
        self.client_combo.bind("<<ComboboxSelected>>", self._update_manager)
        
        # Ответственный менеджер
        self.lbl_manager = ttk.Label(self.main_frame, text="Ответственный:")
        self.manager_combo = ttk.Combobox(self.main_frame, state="readonly")
        self.manager_combo['values'] = [
            f"{m['FirstName']} {m['LastName']}" 
            for m in self.managers
        ]
        
        # Название проекта
        self.lbl_name = ttk.Label(self.main_frame, text="Название проекта:")
        self.entry_name = ttk.Entry(self.main_frame)
        
        # Даты
        self.lbl_start = ttk.Label(self.main_frame, text="Дата начала (ГГГГ-ММ-ДД):")
        self.entry_start = ttk.Entry(self.main_frame)
        
        self.lbl_end = ttk.Label(self.main_frame, text="Дата окончания (ГГГГ-ММ-ДД):")
        self.entry_end = ttk.Entry(self.main_frame)
        
        # Кнопки
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_save = ttk.Button(
            self.btn_frame, 
            text="Сохранить", 
            command=self.save_project,
            width=15
        )
        self.btn_cancel = ttk.Button(
            self.btn_frame, 
            text="Отмена", 
            command=self.destroy,
            width=15
        )

    def _setup_layout(self):
        # Настройка сетки
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Расположение элементов
        row = 0
        
        # Клиент
        self.lbl_client.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.client_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Менеджер
        self.lbl_manager.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.manager_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Название проекта
        self.lbl_name.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.entry_name.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Дата начала
        self.lbl_start.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.entry_start.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Дата окончания
        self.lbl_end.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.entry_end.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Кнопки
        self.btn_frame.grid(row=row, column=0, columnspan=2, pady=15, sticky='e')
        self.btn_save.pack(side=tk.RIGHT, padx=5)
        self.btn_cancel.pack(side=tk.RIGHT, padx=5)

        # Настройка растягивания
        self.main_frame.rowconfigure(row, weight=1)

    def _update_manager(self, event):
        client_idx = self.client_combo.current()
        if client_idx == -1:
            return
            
        client_id = self.clients[client_idx]['ClientID']
        manager_id = self.clients[client_idx]['ManagerID']
        
        # Найти менеджера в списке
        for idx, m in enumerate(self.managers):
            if m['ManagerID'] == manager_id:
                self.manager_combo.current(idx)
                break

    def save_project(self):
        try:
            # Проверка выбора клиента и менеджера
            client_idx = self.client_combo.current()
            manager_idx = self.manager_combo.current()
            
            if client_idx == -1:
                raise ValueError("Выберите клиента")
            if manager_idx == -1:
                raise ValueError("Выберите ответственного менеджера")
                
            # Проверка названия проекта
            project_name = self.entry_name.get().strip()
            if not project_name:
                raise ValueError("Введите название проекта")
                
            # Проверка дат
            start_date = datetime.strptime(self.entry_start.get(), "%Y-%m-%d").date()
            end_date = datetime.strptime(self.entry_end.get(), "%Y-%m-%d").date()
            if start_date > end_date:
                raise ValueError("Дата начала не может быть позже даты окончания")

            # Получение ID
            client_id = self.clients[client_idx]['ClientID']
            manager_id = self.managers[manager_idx]['ManagerID']

            # Сохранение проекта
            self.project_manager.create_project(
                client_id=client_id,
                project_name=project_name,
                manager_id=manager_id,
                start_date=start_date,
                end_date=end_date
            )

            messagebox.showinfo("Успех", "Проект успешно создан!")
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")

class ProjectsViewer(tk.Toplevel):
    def __init__(self, parent, client_id):
        super().__init__(parent)
        self.title("Проекты клиента")
        self.geometry("800x600")
        
        self.project_manager = ProjectManager()
        self.projects = self.project_manager.get_projects_by_client(client_id)
        
        self._create_widgets()
        self._setup_layout()
        
    def _create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('name', 'manager', 'start', 'end'), show='headings')
        self.tree.heading('name', text='Название')
        self.tree.heading('manager', text='Ответственный')
        self.tree.heading('start', text='Дата начала')
        self.tree.heading('end', text='Дата окончания')
        
        for p in self.projects:
            manager_name = f"{p['ManagerFirstName']} {p['ManagerLastName']}"
            self.tree.insert('', 'end', values=(
                p['ProjectName'],
                manager_name,
                p['StartDate'].strftime("%Y-%m-%d"),
                p['EndDate'].strftime("%Y-%m-%d")
            ))
        
    def _setup_layout(self):
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # Ответственный менеджер
        self.lbl_manager = ttk.Label(self.main_frame, text="Ответственный:")
        self.manager_combo = ttk.Combobox(self.main_frame, state="readonly")
        self.manager_combo['values'] = [
            f"{m['FirstName']} {m['LastName']}" 
            for m in self.managers
        ]
        
        # Название проекта
        self.lbl_name = ttk.Label(self.main_frame, text="Название проекта:")
        self.entry_name = ttk.Entry(self.main_frame)
        
        # Даты
        self.lbl_start = ttk.Label(self.main_frame, text="Дата начала (ГГГГ-ММ-ДД):")
        self.entry_start = ttk.Entry(self.main_frame)
        
        self.lbl_end = ttk.Label(self.main_frame, text="Дата окончания (ГГГГ-ММ-ДД):")
        self.entry_end = ttk.Entry(self.main_frame)
        
        # Кнопки
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_save = ttk.Button(
            self.btn_frame, 
            text="Сохранить", 
            command=self.save_project,
            width=15
        )
        self.btn_cancel = ttk.Button(
            self.btn_frame, 
            text="Отмена", 
            command=self.destroy,
            width=15
        )

    def _setup_layout(self):
        # Настройка сетки
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Расположение элементов
        row = 0
        
        # Клиент
        self.lbl_client.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.client_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Менеджер
        self.lbl_manager.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.manager_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Название проекта
        self.lbl_name.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.entry_name.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Дата начала
        self.lbl_start.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.entry_start.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Дата окончания
        self.lbl_end.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.entry_end.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Кнопки
        self.btn_frame.grid(row=row, column=0, columnspan=2, pady=15, sticky='e')
        self.btn_save.pack(side=tk.RIGHT, padx=5)
        self.btn_cancel.pack(side=tk.RIGHT, padx=5)

        # Настройка растягивания
        self.main_frame.rowconfigure(row, weight=1)

    def _update_manager(self, event):
        client_idx = self.client_combo.current()
        if client_idx == -1:
            return
            
        client_id = self.clients[client_idx]['ClientID']
        manager_id = self.clients[client_idx]['ManagerID']
        
        # Найти менеджера в списке
        for idx, m in enumerate(self.managers):
            if m['ManagerID'] == manager_id:
                self.manager_combo.current(idx)
                break

    def save_project(self):
        try:
            # Проверка выбора клиента и менеджера
            client_idx = self.client_combo.current()
            manager_idx = self.manager_combo.current()
            
            if client_idx == -1:
                raise ValueError("Выберите клиента")
            if manager_idx == -1:
                raise ValueError("Выберите ответственного менеджера")
                
            # Проверка названия проекта
            project_name = self.entry_name.get().strip()
            if not project_name:
                raise ValueError("Введите название проекта")
                
            # Проверка дат
            start_date = datetime.strptime(self.entry_start.get(), "%Y-%m-%d").date()
            end_date = datetime.strptime(self.entry_end.get(), "%Y-%m-%d").date()
            if start_date > end_date:
                raise ValueError("Дата начала не может быть позже даты окончания")

            # Получение ID
            client_id = self.clients[client_idx]['ClientID']
            manager_id = self.managers[manager_idx]['ManagerID']

            # Сохранение проекта
            self.project_manager.create_project(
                client_id=client_id,
                project_name=project_name,
                manager_id=manager_id,
                start_date=start_date,
                end_date=end_date
            )

            messagebox.showinfo("Успех", "Проект успешно создан!")
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")