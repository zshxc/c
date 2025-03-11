# gui_payments.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import PaymentManager, DealManager

# gui_payments.py
class PaymentForm(tk.Toplevel):
    def __init__(self, parent, deal_id):
        super().__init__(parent)
        self.title("Добавление платежа")
        self.geometry("400x300")  # Явно задаем размер окна
        self.deal_id = deal_id
        self.payment_manager = PaymentManager()
        self.deal_manager = DealManager()
        
        self._create_widgets()
        self._setup_layout()
        self._load_deal_info()

    def _create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        # Информация о сделке
        self.lbl_deal = ttk.Label(self.main_frame, text="Сделка:", font=('Arial', 10, 'bold'))
        self.lbl_deal_info = ttk.Label(self.main_frame, wraplength=300)
        
        # Поля ввода
        self.lbl_amount = ttk.Label(self.main_frame, text="Сумма платежа:")
        self.entry_amount = ttk.Entry(self.main_frame)
        
        self.lbl_date = ttk.Label(self.main_frame, text="Дата (ГГГГ-ММ-ДД):")
        self.entry_date = ttk.Entry(self.main_frame)
        
        # Кнопки
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_save = ttk.Button(
            self.btn_frame, 
            text="Сохранить", 
            command=self._save,
            width=12
        )
        self.btn_cancel = ttk.Button(
            self.btn_frame, 
            text="Отмена", 
            command=self.destroy,
            width=12
        )

    def _setup_layout(self):
        # Настройка сетки
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Расположение элементов
        self.lbl_deal.grid(row=0, column=0, sticky='nw', padx=5, pady=5)
        self.lbl_deal_info.grid(row=0, column=1, sticky='nw', padx=5, pady=5)
        
        self.lbl_amount.grid(row=1, column=0, sticky='e', padx=5, pady=10)
        self.entry_amount.grid(row=1, column=1, sticky='ew', padx=5, pady=10)
        
        self.lbl_date.grid(row=2, column=0, sticky='e', padx=5, pady=10)
        self.entry_date.grid(row=2, column=1, sticky='ew', padx=5, pady=10)
        
        # Кнопки внизу формы
        self.btn_frame.grid(row=3, column=0, columnspan=2, pady=15, sticky='e')
        self.btn_save.pack(side=tk.RIGHT, padx=5)
        self.btn_cancel.pack(side=tk.RIGHT, padx=5)

    def _load_deal_info(self):
        deal = self.deal_manager.get_deal_by_id(self.deal_id)
        total_paid = self.payment_manager.get_total_paid(self.deal_id)
        info_text = (
            f"Название: {deal['DealName']}\n"
            f"Общая сумма: {deal['TotalAmount']:.2f}\n"
            f"Оплачено: {total_paid:.2f}"
        )
        self.lbl_deal_info.config(text=info_text)

    def _save(self):
        try:
            amount = float(self.entry_amount.get())
            payment_date = datetime.strptime(self.entry_date.get(), "%Y-%m-%d")
            
            if amount <= 0:
                raise ValueError("Сумма платежа должна быть больше нуля")
                
            self.payment_manager.create_payment(
                deal_id=self.deal_id,
                amount=amount,
                payment_date=payment_date
            )
            
            messagebox.showinfo("Успех", "Платеж успешно добавлен")
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")

class DealSelector(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Выбор сделки")
        self.deal_manager = DealManager()
        self.deals = self.deal_manager.get_all_deals()
        
        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.lbl_info = ttk.Label(self.main_frame, text="Выберите сделку:")
        self.combo = ttk.Combobox(self.main_frame, state="readonly")
        self.btn_proceed = ttk.Button(self.main_frame, text="Выбрать", command=self._proceed)

    def _setup_layout(self):
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.lbl_info.grid(row=0, column=0, pady=5)
        self.combo.grid(row=1, column=0, pady=5, sticky='ew')
        self.btn_proceed.grid(row=2, column=0, pady=10)
        
        # Заполнение данными
        self.combo['values'] = [
            f"{deal['DealName']} (ID: {deal['DealID']})" 
            for deal in self.deals
        ]

    def _proceed(self):
        selected_idx = self.combo.current()
        if selected_idx == -1:
            messagebox.showerror("Ошибка", "Выберите сделку из списка")
            return
            
        selected_deal = self.deals[selected_idx]
        self.destroy()
        PaymentForm(self.master, selected_deal['DealID'])
class DealSelector(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Выбор сделки")
        self.deal_manager = DealManager()
        self.deals = self.deal_manager.get_all_deals()
        
        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.lbl_info = ttk.Label(self.main_frame, text="Выберите сделку:")
        self.combo = ttk.Combobox(self.main_frame, state="readonly")
        self.btn_proceed = ttk.Button(self.main_frame, text="Выбрать", command=self._proceed)

    def _setup_layout(self):
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.lbl_info.grid(row=0, column=0, pady=5)
        self.combo.grid(row=1, column=0, pady=5, sticky='ew')
        self.btn_proceed.grid(row=2, column=0, pady=10)
        
        # Заполнение данными
        self.combo['values'] = [
            f"{deal['DealName']} (ID: {deal['DealID']})" 
            for deal in self.deals
        ]

    def _proceed(self):
        selected_idx = self.combo.current()
        if selected_idx == -1:
            messagebox.showerror("Ошибка", "Выберите сделку из списка")
            return
            
        selected_deal = self.deals[selected_idx]
        self.destroy()
        PaymentForm(self.master, selected_deal['DealID'])