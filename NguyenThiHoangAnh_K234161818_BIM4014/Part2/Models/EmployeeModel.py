# Models/EmployeeModel.py
import pandas as pd
import traceback


class EmployeeModel:
    """Model cho CRUD operations trên bảng employee trong database um3la"""
    
    def __init__(self, connector=None):
        self.connector = connector
    
    def get_all_employees(self):
        """Lấy tất cả employees"""
        try:
            sql = "SELECT EmployeeID, Name, Email, Password, Role FROM employee ORDER BY EmployeeID;"
            df = self.connector.queryDataset(sql)
            return df
        except Exception as e:
            print(f"Error in get_all_employees: {e}")
            traceback.print_exc()
            return None
    
    def get_employee_by_id(self, employee_id):
        """Lấy employee theo ID"""
        try:
            sql = f"SELECT EmployeeID, Name, Email, Password, Role FROM employee WHERE EmployeeID = {employee_id};"
            df = self.connector.queryDataset(sql)
            if df is not None and not df.empty:
                return df.iloc[0].to_dict()
            return None
        except Exception as e:
            print(f"Error in get_employee_by_id: {e}")
            traceback.print_exc()
            return None
    
    def create_employee(self, name, email, password, role):
        """Tạo employee mới"""
        try:
            cursor = self.connector.conn.cursor()
            sql = """
                INSERT INTO employee (Name, Email, Password, Role) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (name, email, password, role))
            self.connector.conn.commit()
            employee_id = cursor.lastrowid
            cursor.close()
            return employee_id
        except Exception as e:
            print(f"Error in create_employee: {e}")
            traceback.print_exc()
            self.connector.conn.rollback()
            return None
    
    def update_employee(self, employee_id, name, email, password, role):
        """Cập nhật employee"""
        try:
            cursor = self.connector.conn.cursor()
            sql = """
                UPDATE employee 
                SET Name = %s, Email = %s, Password = %s, Role = %s 
                WHERE EmployeeID = %s
            """
            cursor.execute(sql, (name, email, password, role, employee_id))
            self.connector.conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            return rows_affected > 0
        except Exception as e:
            print(f"Error in update_employee: {e}")
            traceback.print_exc()
            self.connector.conn.rollback()
            return False
    
    def delete_employee(self, employee_id):
        """Xóa employee"""
        try:
            cursor = self.connector.conn.cursor()
            sql = "DELETE FROM employee WHERE EmployeeID = %s"
            cursor.execute(sql, (employee_id,))
            self.connector.conn.commit()
            rows_affected = cursor.rowcount
            cursor.close()
            return rows_affected > 0
        except Exception as e:
            print(f"Error in delete_employee: {e}")
            traceback.print_exc()
            self.connector.conn.rollback()
            return False
    
    def check_email_exists(self, email, exclude_id=None):
        """Kiểm tra email đã tồn tại chưa"""
        try:
            if exclude_id:
                sql = "SELECT COUNT(*) as count FROM employee WHERE Email = %s AND EmployeeID != %s"
                cursor = self.connector.conn.cursor()
                cursor.execute(sql, (email, exclude_id))
            else:
                sql = "SELECT COUNT(*) as count FROM employee WHERE Email = %s"
                cursor = self.connector.conn.cursor()
                cursor.execute(sql, (email,))
            
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0 if result else False
        except Exception as e:
            print(f"Error in check_email_exists: {e}")
            traceback.print_exc()
            return False

