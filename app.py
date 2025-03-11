# app.py
import tkinter as tk
from gui_managers import ManagerForm
from gui_clients import ClientForm
from gui_notes import NoteForm, NotesViewer
from gui_deals import DealForm
from gui_projects import ProjectForm, ProjectsViewer
from gui_tasks import TasksViewer
from gui_payments import PaymentForm
from gui_reports import AverageCheckReport
from gui_payments import DealSelector
from gui_deduplication import DeduplicationView
from gui_interactions import InteractionsView

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CRM System")
        self.geometry("300x250")
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        
        buttons = [
            ("Создать менеджера", self.open_manager_form),
            ("Создать клиента", self.open_client_form),
            ("Добавить заметку", self.open_note_form),
            ("Просмотр заметок", self.open_notes_viewer),
            ("Новая сделка", self.open_deal_form),
            ("Создать проект", self.open_project_form),
            ("Средний чек", self.open_avg_check_report),
            ("Дедупликация", self.open_deduplication),
            ("ВЗаимодействия", self.open_interactions_viewer)
        ]
        tk.Button(btn_frame, text="Управление задачами", 
            command=self.open_tasks_viewer).pack(pady=5)

        tk.Button(btn_frame, text="Добавить платеж", 
            command=self.open_payment_form).pack(pady=5)
        
        for text, command in buttons:
            tk.Button(btn_frame, text=text, command=command).pack(pady=3, fill=tk.X)
    
    def open_manager_form(self):
        ManagerForm(self)
    
    def open_client_form(self):
        ClientForm(self)
    
    def open_note_form(self):
        NoteForm(self)
    
    def open_notes_viewer(self):
        NotesViewer(self)
    
    def open_deal_form(self):
        DealForm(self)

    def open_project_form(self):
        ProjectForm(self)
    
    def open_projects_viewer(self):
        pass
    def open_tasks_viewer(self):
        TasksViewer(self)
    def open_payment_form(self):
        DealSelector(self)
    def open_avg_check_report(self):
        AverageCheckReport(self)
    def open_deduplication(self):
        DeduplicationView(self)
    def open_interactions_viewer(self):
        InteractionsView(self)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()