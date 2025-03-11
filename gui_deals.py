# gui_deals.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import DealManager, DealItemManager, ClientManager, ManagerManager

class DealForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Новая сделка")
        self.geometry("800x600")
        
        # Инициализация менеджеров БД
        self.deal_manager = DealManager()
        self.client_manager = ClientManager()
        self.manager_manager = ManagerManager()
        self.items = []
        
        # Загрузка данных
        self.clients = self.client_manager.get_all_clients()
        self.managers = self.manager_manager.get_all_managers()
        
        # Создание виджетов
        self._create_widgets()
        self._setup_layout()
        self._center_window()
        self.btn_payments = ttk.Button(btn_frame, text="Платежи", command=self._show_payments)



    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def _create_widgets(self):
        # Основной контейнер
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Выбор клиента
        self.lbl_client = ttk.Label(self.main_frame, text="Клиент:")
        self.client_combo = ttk.Combobox(self.main_frame, state="readonly")
        self.client_combo['values'] = [
            f"{c['FirstName']} {c['LastName']} (ID: {c['ClientID']})" 
            for c in self.clients
        ]

        # Выбор менеджера
        self.lbl_manager = ttk.Label(self.main_frame, text="Менеджер:")
        self.manager_combo = ttk.Combobox(self.main_frame, state="readonly")
        self.manager_combo['values'] = [
            f"{m['FirstName']} {m['LastName']} (ID: {m['ManagerID']})" 
            for m in self.managers
        ]

        # Название сделки
        self.lbl_deal_name = ttk.Label(self.main_frame, text="Название сделки:")
        self.entry_deal_name = ttk.Entry(self.main_frame, width=40)

        # Поля для ввода позиции
        self.input_frame = ttk.Frame(self.main_frame)
        
        # Наименование
        self.lbl_item = ttk.Label(self.input_frame, text="Наименование:")
        self.entry_item = ttk.Entry(self.input_frame, width=25)
        
        # Количество
        self.lbl_quantity = ttk.Label(self.input_frame, text="Количество:")
        self.entry_quantity = ttk.Entry(self.input_frame, width=10)
        
        # Цена
        self.lbl_price = ttk.Label(self.input_frame, text="Цена:")
        self.entry_price = ttk.Entry(self.input_frame, width=15)
        
        # Кнопка добавления
        self.btn_add_item = ttk.Button(
            self.input_frame, 
            text="Добавить позицию", 
            command=self.add_item
        )

        # Таблица позиций
        self.columns = ('name', 'quantity', 'price', 'total')
        self.tree = ttk.Treeview(
            self.main_frame, 
            columns=self.columns, 
            show='headings',
            height=8
        )
        self.tree.heading('name', text='Наименование')
        self.tree.heading('quantity', text='Количество')
        self.tree.heading('price', text='Цена за ед.')
        self.tree.heading('total', text='Сумма')

        # Итоговая сумма
        self.lbl_total = ttk.Label(self.main_frame, text="Общая сумма:")
        self.lbl_total_value = ttk.Label(
            self.main_frame, 
            text="0.00", 
            font=('Arial', 12, 'bold')
        )

        # Кнопки управления
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_save = ttk.Button(
            self.btn_frame, 
            text="Сохранить сделку", 
            command=self.save_deal,
            style='Primary.TButton'
        )
        self.btn_cancel = ttk.Button(
            self.btn_frame, 
            text="Отмена", 
            command=self.destroy
        )

    def _setup_layout(self):
        # Настройка сетки основного фрейма
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

        # Название сделки
        self.lbl_deal_name.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.entry_deal_name.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        row += 1

        # Поля ввода позиции
        self.input_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=10)
        self.lbl_item.grid(row=0, column=0, padx=2)
        self.entry_item.grid(row=0, column=1, padx=2)
        self.lbl_quantity.grid(row=0, column=2, padx=2)
        self.entry_quantity.grid(row=0, column=3, padx=2)
        self.lbl_price.grid(row=0, column=4, padx=2)
        self.entry_price.grid(row=0, column=5, padx=2)
        self.btn_add_item.grid(row=0, column=6, padx=5)
        row += 1

        # Таблица позиций
        self.tree.grid(row=row, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        row += 1

        # Итоговая сумма
        self.lbl_total.grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.lbl_total_value.grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1

        # Кнопки управления
        self.btn_frame.grid(row=row, column=0, columnspan=2, pady=20, sticky='e')
        self.btn_save.pack(side=tk.RIGHT, padx=5)
        self.btn_cancel.pack(side=tk.RIGHT, padx=5)

        # Настройка растягивания
        self.main_frame.rowconfigure(4, weight=1)

    def add_item(self):
        try:
            # Получение данных из полей ввода
            item_name = self.entry_item.get().strip()
            quantity = self.entry_quantity.get().strip()
            price = self.entry_price.get().strip()

            # Валидация ввода
            if not item_name:
                raise ValueError("Введите наименование позиции")
            if not quantity.isdigit():
                raise ValueError("Количество должно быть целым числом")
            if not self._is_valid_price(price):
                raise ValueError("Некорректный формат цены")

            # Преобразование данных
            quantity = int(quantity)
            price = float(price)
            
            if quantity <= 0:
                raise ValueError("Количество должно быть больше 0")
            if price <= 0:
                raise ValueError("Цена должна быть больше 0")

            # Добавление в таблицу
            total = quantity * price
            self.tree.insert('', 'end', values=(
                item_name,
                quantity,
                f"{price:.2f}",
                f"{total:.2f}"
            ))
            
            # Сохранение в списке
            self.items.append({
                'name': item_name,
                'quantity': quantity,
                'price': price
            })
            
            # Обновление итоговой суммы
            self._update_total()
            
            # Очистка полей ввода
            self.entry_item.delete(0, tk.END)
            self.entry_quantity.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_item.focus_set()

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))

    def _is_valid_price(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _update_total(self):
        total = sum(item['quantity'] * item['price'] for item in self.items)
        self.lbl_total_value.config(text=f"{total:.2f}")

    def save_deal(self):
        try:
            # Проверка обязательных полей
            if self.client_combo.current() == -1:
                raise ValueError("Выберите клиента")
            if self.manager_combo.current() == -1:
                raise ValueError("Выберите менеджера")
            if not self.entry_deal_name.get().strip():
                raise ValueError("Введите название сделки")
            if not self.items:
                raise ValueError("Добавьте хотя бы одну позицию")

            # Получение данных
            client_id = self.clients[self.client_combo.current()]['ClientID']
            manager_id = self.managers[self.manager_combo.current()]['ManagerID']
            deal_name = self.entry_deal_name.get().strip()
            total_amount = sum(item['quantity'] * item['price'] for item in self.items)

            # Сохранение сделки
            deal_id = self.deal_manager.create_deal(
                client_id=client_id,
                manager_id=manager_id,
                deal_name=deal_name,
                total_amount=total_amount
            )

            # Сохранение позиций
            item_manager = DealItemManager()
            for item in self.items:
                item_manager.create_item(
                    deal_id=deal_id,
                    item_name=item['name'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            messagebox.showinfo("Успех", "Сделка успешно сохранена!")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")

        def _show_payments(self):
            PaymentsViewer(self, self.deal_id)
        def _setup_ui(self):
            self.btn_payments.pack(side=tk.LEFT, padx=5)
    def _create_recommendations_section(self):
        # Панель рекомендаций
        self.recommendation_frame = ttk.LabelFrame(self.main_frame, text="Рекомендуемые товары")
        self.recommendation_frame.grid(row=0, column=2, rowspan=7, padx=10, sticky='ns')
        
        self.recommendation_list = ttk.Treeview(self.recommendation_frame, 
                                              columns=('item', 'count'), 
                                              show='headings',
                                              height=15)
        self.recommendation_list.heading('item', text='Товар')
        self.recommendation_list.heading('count', text='Заказов')
        self.recommendation_list.column('item', width=150)
        self.recommendation_list.column('count', width=50, anchor='center')
        
        scroll = ttk.Scrollbar(self.recommendation_frame, 
                             orient="vertical", 
                             command=self.recommendation_list.yview)
        self.recommendation_list.configure(yscrollcommand=scroll.set)
        
        self.recommendation_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Обработчик двойного клика для добавления товара
        self.recommendation_list.bind("<Double-1>", self._add_recommended_item)

    def _load_recommendations(self):
        client_id = self.clients[self.client_combo.current()]['ClientID']
        recommendations = self.deal_manager.get_recommended_items(client_id)
        
        for item in self.recommendation_list.get_children():
            self.recommendation_list.delete(item)
            
        for item in recommendations:
            self.recommendation_list.insert('', 'end', 
                                          values=(item['ItemName'], item['order_count']),
                                          tags=('recommended',))
            
        self.recommendation_list.tag_configure('recommended', background='#f0fff0')

    def _add_recommended_item(self, event):
        selected = self.recommendation_list.selection()
        if selected:
            item = self.recommendation_list.item(selected[0])['values'][0]
            self.item_name.insert(0, item)
            self.quantity.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    DealForm(root)
    root.mainloop()