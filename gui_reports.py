import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import ReportManager

class AverageCheckReport(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Отчет: Средний чек")
        self.geometry("500x300")
        
        self.report_manager = ReportManager()
        
        self._create_widgets()
        self._setup_layout()
        self._set_default_dates()

    def _create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Поля ввода дат
        self.lbl_start = ttk.Label(self.main_frame, text="Дата начала:")
        self.entry_start = ttk.Entry(self.main_frame)
        
        self.lbl_end = ttk.Label(self.main_frame, text="Дата окончания:")
        self.entry_end = ttk.Entry(self.main_frame)
        
        # Кнопки
        self.btn_generate = ttk.Button(
            self.main_frame, 
            text="Сформировать отчет", 
            command=self.generate_report
        )
        
        # Область результатов
        self.result_frame = ttk.LabelFrame(self.main_frame, text="Результаты")
        self.lbl_total_deals = ttk.Label(self.result_frame, text="Всего сделок:")
        self.lbl_total_amount = ttk.Label(self.result_frame, text="Общая сумма:")
        self.lbl_avg_check = ttk.Label(self.result_frame, text="Средний чек:")
        
        self.val_total_deals = ttk.Label(self.result_frame, text="0")
        self.val_total_amount = ttk.Label(self.result_frame, text="0.00 ₽")
        self.val_avg_check = ttk.Label(self.result_frame, text="0.00 ₽")

    def _setup_layout(self):
        # Поля ввода
        self.lbl_start.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.entry_start.grid(row=0, column=1, padx=5, pady=5)
        
        self.lbl_end.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_end.grid(row=1, column=1, padx=5, pady=5)
        
        self.btn_generate.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Результаты
        self.result_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=10)
        
        self.lbl_total_deals.grid(row=0, column=0, sticky='e', padx=5)
        self.val_total_deals.grid(row=0, column=1, sticky='w', padx=5)
        
        self.lbl_total_amount.grid(row=1, column=0, sticky='e', padx=5)
        self.val_total_amount.grid(row=1, column=1, sticky='w', padx=5)
        
        self.lbl_avg_check.grid(row=2, column=0, sticky='e', padx=5)
        self.val_avg_check.grid(row=2, column=1, sticky='w', padx=5)
        
        # Настройка колонок
        self.main_frame.columnconfigure(1, weight=1)
        self.result_frame.columnconfigure(1, weight=1)

    def _set_default_dates(self):
        today = datetime.today().strftime("%Y-%m-%d")
        self.entry_start.insert(0, today)
        self.entry_end.insert(0, today)

    def generate_report(self):
        try:
            start_date = datetime.strptime(self.entry_start.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.entry_end.get(), "%Y-%m-%d")
            
            if start_date > end_date:
                raise ValueError("Дата начала не может быть позже даты окончания")
                
            report = self.report_manager.get_average_check(start_date, end_date)
            
            self.val_total_deals.config(text=f"{report['total_deals']}")
            self.val_total_amount.config(text=f"{report['total_amount']:.2f} ₽")
            self.val_avg_check.config(text=f"{report['avg_check']:.2f} ₽")
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка получения данных: {str(e)}")