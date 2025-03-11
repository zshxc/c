import mysql.connector

class DBConnection:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '13022005Da',
            'database': 'crm_system'
        }
    
    def get_connection(self):
        return mysql.connector.connect(**self.config)

class BaseManager:
    def __init__(self):
        self.db = DBConnection()

class ClientManager(BaseManager):
    def create_client(self, first_name, last_name, email, phone, manager_id):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO Clients (FirstName, LastName, Email, Phone, ManagerID) "
                "VALUES (%s, %s, %s, %s, %s)",
                (first_name, last_name, email, phone, manager_id)
            )
            
            conn.commit()
            print(f"Клиент {first_name} {last_name} успешно создан")
            
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            print(f"Ошибка при создании клиента: {err}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    def get_all_clients(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clients")
        clients = cursor.fetchall()
        cursor.close()
        conn.close()
        return clients
        conn.commit()
        cursor.close()
        conn.close()

class ManagerManager(BaseManager):
    def create_manager(self, first_name, last_name, email, phone):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Managers (FirstName, LastName, Email, Phone) "
            "VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, phone)
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_all_managers(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Managers")
        managers = cursor.fetchall()
        cursor.close()
        conn.close()
        return managers

class NoteManager(BaseManager):
    def create_note(self, client_id, note_text):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ClientNotes (ClientID, NoteText) VALUES (%s, %s)",
            (client_id, note_text)
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_notes_by_client(self, client_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM ClientNotes WHERE ClientID = %s ORDER BY CreatedAt DESC",
            (client_id,)
        )
        notes = cursor.fetchall()
        cursor.close()
        conn.close()
        return notes

class DealManager(BaseManager):
    def create_deal(self, client_id, manager_id, deal_name, total_amount):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Deals (ClientID, ManagerID, DealName, TotalAmount) "
            "VALUES (%s, %s, %s, %s)",
            (client_id, manager_id, deal_name, total_amount)
        )
        deal_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return deal_id

    def get_all_deals(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Deals")
        deals = cursor.fetchall()
        cursor.close()
        conn.close()
        return deals

    def get_deal_by_id(self, deal_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Deals WHERE DealID = %s", (deal_id,))
        deal = cursor.fetchone()
        cursor.close()
        conn.close()
        return deal
    def get_recommended_items(self, client_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT di.ItemName, 
                       COUNT(*) as order_count
                FROM Deals d
                JOIN DealItems di ON d.DealID = di.DealID
                WHERE d.ClientID = %s
                  AND d.CreatedAt >= NOW() - INTERVAL 1 MONTH
                GROUP BY di.ItemName
                ORDER BY order_count DESC
            """, (client_id,))
            
            return cursor.fetchall()
            
        except Exception as e:
            raise ValueError("Ошибка получения рекомендаций") from e
        finally:
            cursor.close()
            conn.close()

class DealItemManager(BaseManager):
    def create_item(self, deal_id, item_name, quantity, price):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO DealItems (DealID, ItemName, Quantity, Price) "
            "VALUES (%s, %s, %s, %s)",
            (deal_id, item_name, quantity, price)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_items_for_deal(self, deal_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM DealItems WHERE DealID = %s",
            (deal_id,)
        )
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return items


class ProjectManager(BaseManager):
    def create_project(self, client_id, project_name, manager_id, start_date, end_date):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Projects 
            (ClientID, ProjectName, ResponsibleManagerID, StartDate, EndDate)
            VALUES (%s, %s, %s, %s, %s)""",
            (client_id, project_name, manager_id, start_date, end_date)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_projects_by_client(self, client_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT p.*, m.FirstName as ManagerFirstName, m.LastName as ManagerLastName 
            FROM Projects p
            JOIN Managers m ON p.ResponsibleManagerID = m.ManagerID
            WHERE p.ClientID = %s""",
            (client_id,)
        )
        projects = cursor.fetchall()
        cursor.close()
        conn.close()
        return projects

# database.py
class TaskManager(BaseManager):
    def create_task(self, client_id, project_id, task_name, description, due_date, manager_id, status='todo'):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Tasks 
            (ClientID, ProjectID, TaskName, Description, DueDate, ResponsibleManagerID, Status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (client_id, project_id, task_name, description, due_date, manager_id, status)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def update_task(self, task_id, **kwargs):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        set_clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])
        values = list(kwargs.values()) + [task_id]
        cursor.execute(
            f"UPDATE Tasks SET {set_clause} WHERE TaskID = %s",
            values
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_tasks(self, client_id=None, project_id=None):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT t.*, c.FirstName as ClientFirstName, c.LastName as ClientLastName FROM Tasks t JOIN Clients c ON t.ClientID = c.ClientID"
        params = []
        if client_id or project_id:
            conditions = []
            if client_id:
                conditions.append("t.ClientID = %s")
                params.append(client_id)
            if project_id:
                conditions.append("t.ProjectID = %s")
                params.append(project_id)
            query += " WHERE " + " AND ".join(conditions)
        cursor.execute(query, params)
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        return tasks

class PaymentManager(BaseManager):
    def create_payment(self, deal_id, amount, payment_date):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Payments (DealID, PaymentAmount, PaymentDate)
            VALUES (%s, %s, %s)""",
            (deal_id, amount, payment_date)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_payments_by_deal(self, deal_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT * FROM Payments 
            WHERE DealID = %s
            ORDER BY PaymentDate DESC""",
            (deal_id,)
        )
        payments = cursor.fetchall()
        cursor.close()
        conn.close()
        return payments

    def get_total_paid(self, deal_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT SUM(PaymentAmount) 
            FROM Payments 
            WHERE DealID = %s""",
            (deal_id,)
        )
        total = cursor.fetchone()[0] or 0.0
        cursor.close()
        conn.close()
        return total

class InteractionManager(BaseManager):
    def create_interaction(self, client_id, contact_person, interaction_type, interaction_date, content):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Interactions 
            (ClientID, ContactPerson, InteractionType, InteractionDate, Content)
            VALUES (%s, %s, %s, %s, %s)""",
            (client_id, contact_person, interaction_type, interaction_date, content)
        )
        conn.commit()
        cursor.close()
        conn.close()

class ReportManager(BaseManager):
    def get_average_check(self, start_date, end_date):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Получаем общую сумму и количество сделок
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_deals,
                    SUM(TotalAmount) as total_amount,
                    SUM(TotalAmount)/COUNT(*) as avg_check
                FROM Deals
                WHERE CreatedAt BETWEEN %s AND %s
            """, (start_date, end_date))
            
            result = cursor.fetchone()
            return {
                'total_deals': result['total_deals'],
                'total_amount': result['total_amount'] or 0.0,
                'avg_check': result['avg_check'] or 0.0
            }
            
        except Exception as e:
            raise ValueError("Ошибка расчета среднего чека") from e
        finally:
            cursor.close()
            conn.close()

class DeduplicationManager(BaseManager):
    def find_duplicates(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Поиск дубликатов по комбинациям полей
            cursor.execute("""
                SELECT 
                    a.ClientID as id1,
                    b.ClientID as id2,
                    CASE 
                        WHEN a.Email = b.Email AND a.Email != '' THEN 'email'
                        WHEN a.Phone = b.Phone AND a.Phone != '' THEN 'phone'
                        WHEN CONCAT(a.FirstName, a.LastName) = CONCAT(b.FirstName, b.LastName) THEN 'name'
                    END as match_type,
                    a.FirstName as name1,
                    b.FirstName as name2,
                    a.Email as email1,
                    b.Email as email2,
                    a.Phone as phone1,
                    b.Phone as phone2
                FROM Clients a
                JOIN Clients b 
                ON 
                    (a.Email = b.Email AND a.Email != '' AND a.ClientID < b.ClientID) OR
                    (a.Phone = b.Phone AND a.Phone != '' AND a.ClientID < b.ClientID) OR
                    (CONCAT(a.FirstName, a.LastName) = CONCAT(b.FirstName, b.LastName) AND a.ClientID < b.ClientID)
            """)
            
            duplicates = []
            for row in cursor:
                duplicates.append({
                    'ids': [row['id1'], row['id2']],
                    'type': row['match_type'],
                    'details': {
                        'names': [row['name1'], row['name2']],
                        'emails': [row['email1'], row['email2']],
                        'phones': [row['phone1'], row['phone2']]
                    }
                })
            
            return duplicates
            
        except Exception as e:
            raise ValueError("Ошибка поиска дубликатов") from e
        finally:
            cursor.close()
            conn.close()

class InteractionManager(BaseManager):
    def create_interaction(self, client_id, contact_person, interaction_type, interaction_date, content):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Interactions 
            (ClientID, ContactPerson, InteractionType, InteractionDate, Content)
            VALUES (%s, %s, %s, %s, %s)""",
            (client_id, contact_person, interaction_type, interaction_date, content)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_interactions_by_client(self, client_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT * FROM Interactions 
            WHERE ClientID = %s
            ORDER BY InteractionDate DESC""",
            (client_id,)
        )
        interactions = cursor.fetchall()
        cursor.close()
        conn.close()
        return interactions

    def get_all_interactions(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Interactions ORDER BY InteractionDate DESC")
        interactions = cursor.fetchall()
        cursor.close()
        conn.close()
        return interactions