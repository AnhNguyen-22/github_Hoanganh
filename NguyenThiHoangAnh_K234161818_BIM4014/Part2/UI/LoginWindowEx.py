from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import Qt
from Connectors.Connector import Connector
from UI.LoginWindow import Ui_LoginWindow


class LoginWindowEx(QDialog, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Biến đếm số lần đăng nhập sai
        self.failed_attempts = 0
        self.max_attempts = 3
        self.is_locked = False
        
        # Kết nối database
        self.conn = Connector(
            server="localhost",
            port=3306,
            database="um3la",
            username="root",
            password="Hoanganh22",
        )
        self.conn.connect()
        if self.conn.conn is None:
            QMessageBox.critical(
                self, 
                "Lỗi kết nối", 
                "Không thể kết nối đến database!\nVui lòng kiểm tra lại cấu hình."
            )
        
        # Thông tin user sau khi đăng nhập thành công
        self.current_user = None
        
        # Kết nối sự kiện
        self.setup_connections()
        
    def setup_connections(self):
        """Thiết lập kết nối các sự kiện"""
        self.btnLogin.clicked.connect(self.handle_login)
        self.btnCancel.clicked.connect(self.reject)
        
        # Cho phép Enter để đăng nhập
        self.txtPassword.returnPressed.connect(self.handle_login)
        self.txtEmail.returnPressed.connect(lambda: self.txtPassword.setFocus())
        
    def handle_login(self):
        """Xử lý sự kiện đăng nhập"""
        # Kiểm tra nếu đã bị khóa
        if self.is_locked:
            QMessageBox.warning(
                self,
                "Đã khóa",
                f"Bạn đã đăng nhập sai {self.max_attempts} lần!\n"
                f"Chức năng đăng nhập đã bị khóa.\n"
                f"Vui lòng khởi động lại ứng dụng."
            )
            return
        
        # Lấy thông tin từ form
        email = self.txtEmail.text().strip()
        password = self.txtPassword.text().strip()
        
        # Kiểm tra input
        if not email or not password:
            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng nhập đầy đủ Email và Mật khẩu!"
            )
            return
        
        # Kiểm tra kết nối database
        if self.conn.conn is None:
            QMessageBox.critical(
                self,
                "Lỗi",
                "Không thể kết nối đến database!"
            )
            return
        
        # Kiểm tra thông tin đăng nhập
        try:
            sql = """
                SELECT EmployeeID, Name, Email, Password, Role 
                FROM employee 
                WHERE Email = %s AND Password = %s
            """
            cursor = self.conn.conn.cursor()
            cursor.execute(sql, (email, password))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                # Đăng nhập thành công
                self.current_user = {
                    'EmployeeID': result[0],
                    'Name': result[1],
                    'Email': result[2],
                    'Password': result[3],
                    'Role': result[4]
                }
                
                # Reset số lần thử sai
                self.failed_attempts = 0
                self.lblAttempts.setText("")
                
                QMessageBox.information(
                    self,
                    "Đăng nhập thành công",
                    f"Chào mừng {self.current_user['Name']}!\n"
                    f"Role: {self.current_user['Role'].upper()}"
                )
                
                # Đóng dialog và trả về Accepted
                self.accept()
                
            else:
                # Đăng nhập thất bại
                self.failed_attempts += 1
                remaining = self.max_attempts - self.failed_attempts
                
                if remaining > 0:
                    self.lblAttempts.setText(
                        f"⚠️ Đăng nhập sai! Còn {remaining} lần thử."
                    )
                    QMessageBox.warning(
                        self,
                        "Đăng nhập thất bại",
                        f"Email hoặc mật khẩu không đúng!\n"
                        f"Còn {remaining} lần thử."
                    )
                else:
                    # Đã hết số lần thử
                    self.is_locked = True
                    self.lblAttempts.setText(
                        f"❌ Đã khóa! Đăng nhập sai {self.max_attempts} lần."
                    )
                    self.btnLogin.setEnabled(False)
                    self.txtEmail.setEnabled(False)
                    self.txtPassword.setEnabled(False)
                    
                    QMessageBox.critical(
                        self,
                        "Đã khóa",
                        f"Bạn đã đăng nhập sai {self.max_attempts} lần!\n"
                        f"Chức năng đăng nhập đã bị khóa.\n"
                        f"Vui lòng khởi động lại ứng dụng."
                    )
                    
        except Exception as e:
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Đã xảy ra lỗi khi kiểm tra đăng nhập:\n{str(e)}"
            )
    
    def get_user_info(self):
        """Trả về thông tin user sau khi đăng nhập thành công"""
        return self.current_user
    
    def closeEvent(self, event):
        """Xử lý khi đóng cửa sổ"""
        if self.conn.conn:
            self.conn.disConnect()
        event.accept()

