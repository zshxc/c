# gui_tasks.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import TaskManager, ClientManager, ProjectManager, ManagerManager

class TaskForm(tk.Toplevel):
    def __init__(self, parent, task_id=None):
        super().__init__(parent)
        self.task_id = task_id
        self.title("Новая задача" if not task_id else "Редактирование задачи")
        self.geometry("600x500")
        
        self.task_manager = TaskManager()
        self.client_manager = ClientManager()
        self.project_manager = ProjectManager()
        self.manager_manager = ManagerManager()
        
        self._create_widgets()
        self._setup_layout()
        self._load_initial_data()
        
        if task_id:
            self._load_task_data()

    def _create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Клиент
        self.lbl_client = ttk.Label(self.main_frame, text="Клиент:")
        self.client_combo = ttk.Combobox(self.main_frame, state="readonly")
        self.client_combo.bind("<<ComboboxSelected>>", self._load_projects)
        
        # Проект
        self.lbl_project = ttk.Label(self.main_frame, text="Проект:")
        self.project_combo = ttk.Combobox(self.main_frame, state="readonly")
        
        # Ответственный
        self.lbl_manager = ttk.Label(self.main_frame, text="Ответственный:")
        self.manager_combo = ttk.Combobox(self.main_frame, state="readonly")
        
        # Название задачи
        self.lbl_name = ttk.Label(self.main_frame, text="Название задачи:")
        self.entry_name = ttk.Entry(self.main_frame)
        
        # Описание
        self.lbl_desc = ttk.Label(self.main_frame, text="Описание:")
        self.text_desc = tk.Text(self.main_frame, height=5, width=40)
        
        # Срок выполнения
        self.lbl_due = ttk.Label(self.main_frame, text="Срок (ГГГГ-ММ-ДД):")
        self.entry_due = ttk.Entry(self.main_frame)
        
        # Статус
        self.lbl_status = ttk.Label(self.main_frame, text="Статус:")
        self.status_combo = ttk.Combobox(self.main_frame, 
                                       values=['todo', 'in_progress', 'done'], 
                                       state="readonly")
        
        # Кнопки
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_save = ttk.Button(self.btn_frame, text="Сохранить", command=self._save)
        self.btn_cancel = ttk.Button(self.btn_frame, text="Отмена", command=self.destroy)

    def _setup_layout(self):
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        row = 0
        # Клиент
        self.lbl_client.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.client_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Проект
        self.lbl_project.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.project_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Ответственный
        self.lbl_manager.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.manager_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Название задачи
        self.lbl_name.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.entry_name.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Описание
        self.lbl_desc.grid(row=row, column=0, sticky='ne', padx=5, pady=5)
        self.text_desc.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Срок выполнения
        self.lbl_due.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.entry_due.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Статус
        self.lbl_status.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.status_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Кнопки
        self.btn_frame.grid(row=row, column=0, columnspan=2, pady=10)
        self.btn_save.pack(side=tk.RIGHT, padx=5)
        self.btn_cancel.pack(side=tk.RIGHT, padx=5)

    def _load_initial_data(self):
        # Загрузка клиентов
        clients = self.client_manager.get_all_clients()
        self.client_combo['values'] = [
            f"{c['FirstName']} {c['LastName']}" 
            for c in clients
        ]
        
        # Загрузка менеджеров
        managers = self.manager_manager.get_all_managers()
        self.manager_combo['values'] = [
            f"{m['FirstName']} {m['LastName']}" 
            for m in managers
        ]
        
        # Установка статуса по умолчанию
        self.status_combo.set('todo')

    def _load_projects(self, event=None):
        client_idx = self.client_combo.current()
        if client_idx == -1:
            return
            
        client_id = self.client_manager.get_all_clients()[client_idx]['ClientID']
        projects = self.project_manager.get_projects_by_client(client_id)
        self.project_combo['values'] = [
            f"{p['ProjectName']}" 
            for p in projects
        ]

    def _load_task_data(self):
        # Реализуйте метод получения данных задачи по ID
        pass

    def _save(self):
        try:
            # Проверка обязательных полей
            if self.client_combo.current() == -1:
                raise ValueError("Выберите клиента")
                
            if self.manager_combo.current() == -1:
                raise ValueError("Выберите ответственного менеджера")
                
            if not self.entry_name.get().strip():
                raise ValueError("Введите название задачи")

            # Сбор данных
            data = {
                'client_id': self.client_manager.get_all_clients()[self.client_combo.current()]['ClientID'],
                'manager_id': self.manager_manager.get_all_managers()[self.manager_combo.current()]['ManagerID'],
                'task_name': self.entry_name.get().strip(),
                'description': self.text_desc.get("1.0", tk.END).strip(),
                'due_date': datetime.strptime(self.entry_due.get(), "%Y-%m-%d").date(),
                'status': self.status_combo.get(),
                'project_id': None
            }

            # Обработка проекта
            if self.project_combo.current() != -1:
                client_id = data['client_id']
                projects = self.project_manager.get_projects_by_client(client_id)
                data['project_id'] = projects[self.project_combo.current()]['ProjectID']

            # Сохранение задачи
            if self.task_id:
                self.task_manager.update_task(self.task_id, **data)
            else:
                self.task_manager.create_task(**data)

            messagebox.showinfo("Успех", "Задача сохранена!")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")

class TasksViewer(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Список задач")
        self.geometry("1200x600")
        
        self.task_manager = TaskManager()
        self._create_widgets()
        self._load_tasks()

    def _create_widgets(self):
        # Treeview для отображения задач
        self.tree = ttk.Treeview(self, columns=('client', 'project', 'task', 'due', 'status', 'manager'), show='headings')
        
        # Настройка колонок
        self.tree.heading('client', text='Клиент')
        self.tree.heading('project', text='Проект')
        self.tree.heading('task', text='Задача')
        self.tree.heading('due', text='Срок')
        self.tree.heading('status', text='Статус')
        self.tree.heading('manager', text='Ответственный')
        
        # Полосы прокрутки
        scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Кнопки
        btn_frame = ttk.Frame(self)
        self.btn_new = ttk.Button(btn_frame, text="Новая задача", command=self._new_task)
        self.btn_edit = ttk.Button(btn_frame, text="Редактировать", command=self._edit_task)
        
        # Размещение элементов
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        btn_frame.pack(pady=10)
        self.btn_new.pack(side=tk.LEFT, padx=5)
        self.btn_edit.pack(side=tk.LEFT, padx=5)

    def _load_tasks(self):
        # Очистка текущих данных
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Загрузка задач
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            self.tree.insert('', 'end', values=(
                f"{task.get('ClientFirstName', '')} {task.get('ClientLastName', '')}",
                task.get('ProjectName', ''),
                task['TaskName'],
                task['DueDate'].strftime("%Y-%m-%d"),
                task['Status'],
                f"{task.get('ManagerFirstName', '')} {task.get('ManagerLastName', '')}"
            ))

    def _new_task(self):
        TaskForm(self)
        self._load_tasks()

    def _edit_task(self):
        selected = self.tree.selection()
        if selected:
            task_id = self.tree.item(selected[0])['values'][0]
            TaskForm(self, task_id=task_id)
            self._load_tasks()