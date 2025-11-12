import pandas as pd
from datetime import datetime, date
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QTableWidgetItem,
    QInputDialog,
)
from PyQt6 import QtGui

from UI.MainWindow import Ui_MainWindow
from UI.ChartCanvas import ChartCanvas
from Connectors.Connector import Connector
from Models.Clustering import Clustering
from Models.EmployeeModel import EmployeeModel
from Models.TransactionStatistic import TransactionStatistic


class MainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self, user_info=None):
        super().__init__()
        self.setupUi(self)
        
        # Lưu thông tin user đã đăng nhập
        self.user_info = user_info
        self.user_role = user_info.get('Role', '').lower() if user_info else ''
        if user_info:
            # Cập nhật tiêu đề cửa sổ với thông tin user
            role_display = user_info.get('Role', 'Unknown').upper()
            name_display = user_info.get('Name', 'User')
            self.setWindowTitle(
                f"Retail Analytics & Machine Learning App - "
                f"User: {name_display} ({role_display})"
            )

        # Giao diện pastel - sử dụng đường dẫn tuyệt đối để đảm bảo hoạt động khi di chuyển thư mục
        # Lấy đường dẫn thư mục gốc của dự án (thư mục chứa app.py)
        project_root = Path(__file__).parent.parent
        theme_path = project_root / "UI" / "theme.qss"
        if theme_path.exists():
            with open(theme_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            # Fallback nếu không tìm thấy file
            print(f"Warning: Không tìm thấy file theme tại {theme_path}")

        # Kết nối CSDL um3la (cho Employee, Statistics và Clustering)
        self.conn_um3la = Connector(
            server="localhost",
            port=3306,
            database="um3la",
            username="root",
            password="Hoanganh22",
        )
        self.conn_um3la.connect()
        if self.conn_um3la.conn is None:
            QMessageBox.critical(self, "Error", "Không thể kết nối CSDL um3la!")

        # Models
        self.cluster = Clustering(self.conn_um3la) if self.conn_um3la.conn else None
        self.employee_model = EmployeeModel(self.conn_um3la) if self.conn_um3la.conn else None
        self.trans_stat = TransactionStatistic(self.conn_um3la) if self.conn_um3la.conn else None

        # Thêm matplotlib vào chartFrame (Statistics tab)
        self.chart = ChartCanvas(self.chartFrame)
        layout = QVBoxLayout(self.chartFrame)
        layout.addWidget(self.chart)
        
        # Thêm matplotlib vào chartFrameML (Machine Learning tab)
        self.chartML = ChartCanvas(self.chartFrameML)
        layoutML = QVBoxLayout(self.chartFrameML)
        layoutML.addWidget(self.chartML)

        # --- Gán sự kiện cho CRUD Employee ---
        if hasattr(self, 'btnEmployeeCreate'):
            self.btnEmployeeCreate.clicked.connect(self.create_employee)
            self.btnEmployeeUpdate.clicked.connect(self.update_employee)
            self.btnEmployeeDelete.clicked.connect(self.delete_employee)
            self.btnEmployeeClear.clicked.connect(self.clear_employee_form)
            self.tableEmployee.cellClicked.connect(self.on_employee_table_clicked)
            self.load_employee_list()

        # --- Gán sự kiện cho các nút Statistics (um3la) ---
        if hasattr(self, 'btnMaxInvoiceNo'):
            self.btnMaxInvoiceNo.clicked.connect(self.show_max_invoice_no)
            self.btnTopNCustomers.clicked.connect(self.show_top_n_customers)
            self.btnOrdersByYearCountry.clicked.connect(self.show_orders_by_year_country)

        # --- Machine Learning Tab ---
        self.btnShowElbow.clicked.connect(self.show_elbow_method)
        self.btnClusterTrain.clicked.connect(self.train_cluster)
        self.btnClusterVisual.clicked.connect(self.show_cluster)
        self.btnGetCustomersByCluster.clicked.connect(self.get_customers_by_cluster)
        
        # Hiển thị/ẩn tab theo role
        self.setup_role_based_ui()

    # ===================== Statistics Tab =====================
    def show_table(self, df):
        """Hiển thị dataframe vào bảng tableStats"""
        # DEBUG: In thông tin DataFrame
        print(f"[DEBUG] show_table called - df is None: {df is None}, df.empty: {df.empty if df is not None else 'N/A'}")
        if df is not None:
            print(f"[DEBUG] DataFrame shape: {df.shape}, columns: {list(df.columns)}")
            if not df.empty:
                print(f"[DEBUG] First row sample: {df.iloc[0].to_dict() if len(df) > 0 else 'No rows'}")
        
        if df is None or df.empty:
            self.tableStats.setRowCount(0)
            self.tableStats.setColumnCount(0)
            return
        
        # Reset table
        self.tableStats.clear()
        self.tableStats.setRowCount(0)
        self.tableStats.setColumnCount(0)
        
        # Lấy số hàng và cột
        num_rows = len(df)
        num_cols = len(df.columns)
        
        print(f"[DEBUG] Setting table: {num_rows} rows, {num_cols} cols")
        
        if num_rows == 0 or num_cols == 0:
            print("[DEBUG] No rows or cols, returning")
            return
        
        # Set số hàng và cột
        self.tableStats.setRowCount(num_rows)
        self.tableStats.setColumnCount(num_cols)
        
        # Set headers
        column_names = [str(col) for col in df.columns]
        self.tableStats.setHorizontalHeaderLabels(column_names)
        print(f"[DEBUG] Headers set: {column_names}")
        
        # Fill data - sử dụng iloc thay vì iat để tránh vấn đề
        dark_color = QtGui.QColor("#000000")  # Màu đen rõ ràng để debug
        for i in range(num_rows):
            for j in range(num_cols):
                try:
                    value = df.iloc[i, j]
                    # Xử lý các kiểu dữ liệu khác nhau
                    if pd.isna(value):
                        text = ""
                    elif value is None:
                        text = ""
                    elif isinstance(value, (pd.Timestamp,)):
                        text = str(value)
                    elif isinstance(value, (datetime, date)):
                        text = str(value)
                    else:
                        text = str(value)
                    
                    # DEBUG: In một vài giá trị đầu tiên
                    if i < 2 and j < 2:
                        print(f"[DEBUG] Setting item[{i},{j}] = '{text}'")
                    
                    item = QTableWidgetItem(text)
                    # Đặt màu chữ đen rõ ràng để đảm bảo thấy được
                    item.setForeground(dark_color)
                    # Đặt background trắng để đảm bảo tương phản
                    item.setBackground(QtGui.QColor("#FFFFFF"))
                    self.tableStats.setItem(i, j, item)
                except Exception as e:
                    # Nếu có lỗi, đặt giá trị rỗng
                    print(f"[DEBUG] Error at [{i},{j}]: {e}")
                    item = QTableWidgetItem("ERROR")
                    item.setForeground(QtGui.QColor("#FF0000"))  # Màu đỏ để thấy lỗi
                    self.tableStats.setItem(i, j, item)
        
        self.tableStats.resizeColumnsToContents()
        print(f"[DEBUG] Table populated. Row count: {self.tableStats.rowCount()}, Col count: {self.tableStats.columnCount()}")

    # ===================== Machine Learning Tab =====================
    def show_elbow_method(self):
        """Hiển thị biểu đồ Elbow Method để chọn số cluster K phù hợp"""
        try:
            # Load dữ liệu nếu chưa có
            if self.cluster.df_features is None or self.cluster.df_features.empty:
                self.cluster.load_customer_features()
            
            # Lấy giá trị k_max từ spinK (tối đa 10, tối thiểu 2)
            k_max = min(max(self.spinK.maximum(), 2), 10)
            
            # Tính toán elbow method và lấy dữ liệu
            result = self.cluster.elbow_method(
                columns=["TotalOrders", "TotalProducts", "TotalSpending"],
                k_max=k_max,
                return_data=True
            )
            
            if result is None:
                QMessageBox.warning(
                    self, "Thông báo", 
                    "Không thể tính toán Elbow Method. Vui lòng kiểm tra dữ liệu."
                )
                return
            
            k_values, inertias = result
            
            # Kiểm tra dữ liệu trước khi vẽ
            if not k_values or not inertias or len(k_values) != len(inertias):
                QMessageBox.warning(
                    self, "Thông báo", 
                    "Dữ liệu Elbow Method không hợp lệ. Vui lòng thử lại."
                )
                return
            
            # Chuyển đổi sang list nếu là numpy array
            if hasattr(k_values, 'tolist'):
                k_values = k_values.tolist()
            if hasattr(inertias, 'tolist'):
                inertias = inertias.tolist()
            
            # Hiển thị biểu đồ trong chart canvas của tab Machine Learning
            self.chartML.plot_elbow(
                k_values, 
                inertias, 
                title="Elbow Method - Chọn số cluster K phù hợp"
            )
            
            print(f"[DEBUG] Elbow Method chart displayed: k from 1 to {k_max}, {len(k_values)} points")
            
        except Exception as e:
            print(f"[DEBUG] Error in show_elbow_method: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self, "Lỗi", 
                f"Đã xảy ra lỗi khi hiển thị Elbow Method:\n{str(e)}\n\n"
                f"Vui lòng kiểm tra console để xem chi tiết lỗi."
            )

    def train_cluster(self):
        k = self.spinK.value()
        self.cluster.load_customer_features()
        self.cluster.train_kmeans(
            ["TotalOrders", "TotalProducts", "TotalSpending"], n_clusters=k
        )
        QMessageBox.information(self, "KMeans", f"Huấn luyện KMeans (k={k}) hoàn tất!")

    def show_cluster(self):
        """Hiển thị biểu đồ cluster 2D trong chart canvas"""
        if self.cluster.df_clustered is None:
            QMessageBox.warning(self, "Thông báo", "Hãy train model trước!")
            return
        
        # Hiển thị biểu đồ trong chart canvas của tab Machine Learning
        self.chartML.plot_cluster_2d(
            df=self.cluster.df_clustered,
            x_col="TotalOrders",
            y_col="TotalSpending",
            cluster_col="Cluster",
            title="Customer Clusters — TotalOrders vs TotalSpending"
        )

    def get_customers_by_cluster(self):
        """Yêu cầu 8: Lấy tất cả customers từ một cluster cụ thể"""
        if self.cluster.df_clustered is None:
            QMessageBox.warning(self, "Thông báo", "Hãy train model trước!")
            return
        cluster_id = self.spinClusterID.value()
        df = self.cluster.get_customers_by_cluster(cluster_id)
        if df is None or df.empty:
            QMessageBox.warning(
                self, "Thông báo", f"Không có customers trong cluster {cluster_id}!"
            )
            return
        
        # Sắp xếp lại thứ tự cột: CustomerID ở đầu, Cluster ở cuối
        if "CustomerID" in df.columns:
            cols = ["CustomerID"]
            # Thêm các cột khác (trừ CustomerID và Cluster)
            for col in df.columns:
                if col not in ["CustomerID", "Cluster"]:
                    cols.append(col)
            # Thêm Cluster ở cuối
            if "Cluster" in df.columns:
                cols.append("Cluster")
            # Chỉ giữ các cột có trong df
            cols = [c for c in cols if c in df.columns]
            df = df[cols]
        
        # Sắp xếp theo TotalSpending giảm dần để dễ xem
        if "TotalSpending" in df.columns:
            df = df.sort_values("TotalSpending", ascending=False)
        
        # Hiển thị bảng với tất cả khách hàng trong tab Machine Learning
        self.show_table_ml(df)
        
        # Hiển thị thông tin tổng hợp
        total_customers = len(df)
        total_spending = df["TotalSpending"].sum() if "TotalSpending" in df.columns else 0
        avg_spending = df["TotalSpending"].mean() if "TotalSpending" in df.columns else 0
        
        QMessageBox.information(
            self, "Kết quả", 
            f"Tìm thấy {total_customers} khách hàng trong cluster {cluster_id}\n\n"
            f"Tổng chi tiêu: {total_spending:,.0f}\n"
            f"Chi tiêu trung bình: {avg_spending:,.0f}\n\n"
            f"Danh sách đầy đủ đã được hiển thị trong bảng bên dưới."
        )
    
    def show_table_ml(self, df):
        """Hiển thị dataframe vào bảng tableML (tab Machine Learning)"""
        if df is None or df.empty:
            self.tableML.setRowCount(0)
            self.tableML.setColumnCount(0)
            return
        
        # Reset table
        self.tableML.clear()
        self.tableML.setRowCount(0)
        self.tableML.setColumnCount(0)
        
        # Lấy số hàng và cột
        num_rows = len(df)
        num_cols = len(df.columns)
        
        if num_rows == 0 or num_cols == 0:
            return
        
        # Set số hàng và cột
        self.tableML.setRowCount(num_rows)
        self.tableML.setColumnCount(num_cols)
        
        # Set headers
        column_names = [str(col) for col in df.columns]
        self.tableML.setHorizontalHeaderLabels(column_names)
        
        # Fill data
        dark_color = QtGui.QColor("#000000")
        for i in range(num_rows):
            for j in range(num_cols):
                try:
                    value = df.iloc[i, j]
                    # Xử lý các kiểu dữ liệu khác nhau
                    if pd.isna(value):
                        text = ""
                    elif value is None:
                        text = ""
                    elif isinstance(value, (pd.Timestamp,)):
                        text = str(value)
                    elif isinstance(value, (datetime, date)):
                        text = str(value)
                    else:
                        text = str(value)
                    
                    item = QTableWidgetItem(text)
                    item.setForeground(dark_color)
                    item.setBackground(QtGui.QColor("#FFFFFF"))
                    self.tableML.setItem(i, j, item)
                except Exception as e:
                    item = QTableWidgetItem("")
                    self.tableML.setItem(i, j, item)
        
        self.tableML.resizeColumnsToContents()


    # ===================== Role-Based UI Setup =====================
    def setup_role_based_ui(self):
        """Ẩn/hiện tab và chức năng theo role"""
        if not self.user_role:
            return
        
        # Admin: có tất cả (CRUD Employee, Statistics, ML)
        # Technical: chỉ có ML
        # Reporter: chỉ có Statistics
        
        # Tìm index của các tab
        employee_index = -1
        statistics_index = -1
        ml_index = -1
        
        for i in range(self.tabWidget.count()):
            tab_text = self.tabWidget.tabText(i)
            if "CRUD Employee" in tab_text:
                employee_index = i
            elif "Statistics" in tab_text:
                statistics_index = i
            elif "Machine Learning" in tab_text:
                ml_index = i
        
        # Ẩn/hiện tab theo role
        if self.user_role == "admin":
            # Admin: hiển thị tất cả
            if employee_index >= 0:
                self.tabWidget.setTabVisible(employee_index, True)
            if statistics_index >= 0:
                self.tabWidget.setTabVisible(statistics_index, True)
            if ml_index >= 0:
                self.tabWidget.setTabVisible(ml_index, True)
        elif self.user_role == "technical":
            # Technical: chỉ ML
            if employee_index >= 0:
                self.tabWidget.setTabVisible(employee_index, False)
            if statistics_index >= 0:
                self.tabWidget.setTabVisible(statistics_index, False)
            if ml_index >= 0:
                self.tabWidget.setTabVisible(ml_index, True)
        elif self.user_role == "reporter":
            # Reporter: chỉ Statistics
            if employee_index >= 0:
                self.tabWidget.setTabVisible(employee_index, False)
            if statistics_index >= 0:
                self.tabWidget.setTabVisible(statistics_index, True)
            if ml_index >= 0:
                self.tabWidget.setTabVisible(ml_index, False)

    # ===================== CRUD Employee Tab =====================
    def load_employee_list(self):
        """Load danh sách employee vào bảng"""
        if not self.employee_model:
            return
        
        try:
            df = self.employee_model.get_all_employees()
            if df is None or df.empty:
                self.tableEmployee.setRowCount(0)
                self.tableEmployee.setColumnCount(0)
                return
            
            # Set số hàng và cột
            num_rows = len(df)
            num_cols = len(df.columns)
            self.tableEmployee.setRowCount(num_rows)
            self.tableEmployee.setColumnCount(num_cols)
            
            # Set headers
            column_names = [str(col) for col in df.columns]
            self.tableEmployee.setHorizontalHeaderLabels(column_names)
            
            # Fill data
            for i in range(num_rows):
                for j in range(num_cols):
                    value = df.iloc[i, j]
                    text = "" if pd.isna(value) else str(value)
                    item = QTableWidgetItem(text)
                    self.tableEmployee.setItem(i, j, item)
            
            self.tableEmployee.resizeColumnsToContents()
        except Exception as e:
            print(f"Error loading employee list: {e}")
            QMessageBox.warning(self, "Lỗi", f"Không thể load danh sách employee:\n{str(e)}")
    
    def on_employee_table_clicked(self, row, col):
        """Khi click vào bảng employee, load thông tin vào form"""
        try:
            employee_id = self.tableEmployee.item(row, 0).text()
            if employee_id:
                employee = self.employee_model.get_employee_by_id(int(employee_id))
                if employee:
                    self.txtEmployeeID.setText(str(employee['EmployeeID']))
                    self.txtEmployeeName.setText(employee['Name'])
                    self.txtEmployeeEmail.setText(employee['Email'])
                    self.txtEmployeePassword.setText(employee['Password'])
                    # Set role trong combobox
                    role_index = self.cboEmployeeRole.findText(employee['Role'])
                    if role_index >= 0:
                        self.cboEmployeeRole.setCurrentIndex(role_index)
        except Exception as e:
            print(f"Error loading employee to form: {e}")
    
    def create_employee(self):
        """Tạo employee mới"""
        if not self.employee_model:
            QMessageBox.warning(self, "Lỗi", "Không thể kết nối database!")
            return
        
        name = self.txtEmployeeName.text().strip()
        email = self.txtEmployeeEmail.text().strip()
        password = self.txtEmployeePassword.text().strip()
        role = self.cboEmployeeRole.currentText()
        
        if not name or not email or not password:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Kiểm tra email đã tồn tại chưa
        if self.employee_model.check_email_exists(email):
            QMessageBox.warning(self, "Lỗi", "Email đã tồn tại!")
            return
        
        employee_id = self.employee_model.create_employee(name, email, password, role)
        if employee_id:
            QMessageBox.information(self, "Thành công", f"Đã tạo employee mới với ID: {employee_id}")
            self.clear_employee_form()
            self.load_employee_list()
        else:
            QMessageBox.warning(self, "Lỗi", "Không thể tạo employee!")
    
    def update_employee(self):
        """Cập nhật employee"""
        if not self.employee_model:
            QMessageBox.warning(self, "Lỗi", "Không thể kết nối database!")
            return
        
        employee_id = self.txtEmployeeID.text().strip()
        if not employee_id:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn employee để cập nhật!")
            return
        
        name = self.txtEmployeeName.text().strip()
        email = self.txtEmployeeEmail.text().strip()
        password = self.txtEmployeePassword.text().strip()
        role = self.cboEmployeeRole.currentText()
        
        if not name or not email or not password:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Kiểm tra email đã tồn tại chưa (trừ employee hiện tại)
        if self.employee_model.check_email_exists(email, exclude_id=int(employee_id)):
            QMessageBox.warning(self, "Lỗi", "Email đã được sử dụng bởi employee khác!")
            return
        
        success = self.employee_model.update_employee(int(employee_id), name, email, password, role)
        if success:
            QMessageBox.information(self, "Thành công", "Đã cập nhật employee!")
            self.clear_employee_form()
            self.load_employee_list()
        else:
            QMessageBox.warning(self, "Lỗi", "Không thể cập nhật employee!")
    
    def delete_employee(self):
        """Xóa employee"""
        if not self.employee_model:
            QMessageBox.warning(self, "Lỗi", "Không thể kết nối database!")
            return
        
        employee_id = self.txtEmployeeID.text().strip()
        if not employee_id:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn employee để xóa!")
            return
        
        # Xác nhận xóa
        reply = QMessageBox.question(
            self, "Xác nhận", 
            f"Bạn có chắc chắn muốn xóa employee ID {employee_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.employee_model.delete_employee(int(employee_id))
            if success:
                QMessageBox.information(self, "Thành công", "Đã xóa employee!")
                self.clear_employee_form()
                self.load_employee_list()
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể xóa employee!")
    
    def clear_employee_form(self):
        """Xóa form employee"""
        self.txtEmployeeID.clear()
        self.txtEmployeeName.clear()
        self.txtEmployeeEmail.clear()
        self.txtEmployeePassword.clear()
        self.cboEmployeeRole.setCurrentIndex(0)

    # ===================== Statistics Tab (um3la) =====================
    def show_max_invoice_no(self):
        """Hiển thị InvoiceNo có giá trị lớn nhất"""
        if not self.trans_stat:
            QMessageBox.warning(self, "Lỗi", "Không thể kết nối database!")
            return
        
        df = self.trans_stat.get_max_invoice_no()
        if df is None or df.empty:
            QMessageBox.warning(self, "Thông báo", "Không có dữ liệu!")
            return
        
        self.show_table(df)
        QMessageBox.information(
            self, "Kết quả",
            f"InvoiceNo lớn nhất: {df.iloc[0]['InvoiceNo']}\n"
            f"Giá trị: {df.iloc[0]['Value']}"
        )
    
    def show_top_n_customers(self):
        """Hiển thị TOP N CustomerID có giá trị giao dịch lớn nhất"""
        try:
            if not self.trans_stat:
                QMessageBox.warning(self, "Lỗi", "Không thể kết nối database!")
                return
            
            # Nhập N
            n, ok = QInputDialog.getInt(self, "Nhập N", "Số lượng CustomerID (N):", 10, 1, 100, 1)
            if not ok:
                return
            
            # Nhập khoảng thời gian
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDateTimeEdit, QPushButton, QHBoxLayout
            from PyQt6.QtCore import QDateTime
            
            dialog = QDialog(self)
            dialog.setWindowTitle("Chọn khoảng thời gian")
            dialog.setModal(True)  # Đảm bảo dialog là modal
            layout = QVBoxLayout()
            
            layout.addWidget(QLabel("Từ ngày:"))
            date_from = QDateTimeEdit()
            date_from.setCalendarPopup(True)
            date_from.setDisplayFormat("dd/MM/yyyy HH:mm")
            # Set ngày mặc định
            try:
                default_from = QDateTime.fromString("01/01/2010 00:00", "dd/MM/yyyy HH:mm")
                if default_from.isValid():
                    date_from.setDateTime(default_from)
                else:
                    date_from.setDateTime(QDateTime.currentDateTime().addYears(-10))
            except:
                date_from.setDateTime(QDateTime.currentDateTime().addYears(-10))
            layout.addWidget(date_from)
            
            layout.addWidget(QLabel("Đến ngày:"))
            date_to = QDateTimeEdit()
            date_to.setCalendarPopup(True)
            date_to.setDisplayFormat("dd/MM/yyyy HH:mm")
            date_to.setDateTime(QDateTime.currentDateTime())
            layout.addWidget(date_to)
            
            btn_ok = QPushButton("OK")
            btn_cancel = QPushButton("Hủy")
            btn_layout = QHBoxLayout()
            btn_layout.addWidget(btn_ok)
            btn_layout.addWidget(btn_cancel)
            layout.addLayout(btn_layout)
            
            # Lưu reference để không bị garbage collected
            def on_ok():
                dialog.accept()
            
            def on_cancel():
                dialog.reject()
            
            btn_ok.clicked.connect(on_ok)
            btn_cancel.clicked.connect(on_cancel)
            dialog.setLayout(layout)
            
            # Chạy dialog và kiểm tra kết quả
            result = dialog.exec()
            if result != QDialog.DialogCode.Accepted:
                return
            
            # Lấy giá trị datetime sau khi dialog đóng
            try:
                # PyQt6: sử dụng toPyDateTime() thay vì toPython()
                date_from_val = date_from.dateTime().toPyDateTime()
                date_to_val = date_to.dateTime().toPyDateTime()
            except Exception as e:
                print(f"Error converting datetime: {e}")
                # Fallback: chuyển đổi thủ công
                try:
                    from datetime import datetime
                    qdt_from = date_from.dateTime()
                    qdt_to = date_to.dateTime()
                    date_from_val = datetime(
                        qdt_from.date().year(),
                        qdt_from.date().month(),
                        qdt_from.date().day(),
                        qdt_from.time().hour(),
                        qdt_from.time().minute()
                    )
                    date_to_val = datetime(
                        qdt_to.date().year(),
                        qdt_to.date().month(),
                        qdt_to.date().day(),
                        qdt_to.time().hour(),
                        qdt_to.time().minute()
                    )
                except Exception as e2:
                    print(f"Error in fallback conversion: {e2}")
                    QMessageBox.warning(self, "Lỗi", f"Lỗi khi chuyển đổi ngày tháng:\n{str(e)}\n{str(e2)}")
                    return
            
            # Gọi hàm thống kê
            df = self.trans_stat.get_top_n_customers(n, date_from_val, date_to_val)
            if df is None or df.empty:
                QMessageBox.warning(self, "Thông báo", "Không có dữ liệu trong khoảng thời gian này!")
                return
            
            # Hiển thị kết quả
            self.show_table(df)
            
            # Vẽ biểu đồ
            if len(df) > 0:
                try:
                    self.chart.plot_bar(
                        df["CustomerID"].astype(str),
                        df["TotalTransactionValue"],
                        f"TOP {n} CustomerID có giá trị giao dịch lớn nhất",
                        rotation=45,
                        ha="right",
                    )
                except Exception as e:
                    print(f"Error plotting chart: {e}")
                    QMessageBox.warning(self, "Cảnh báo", f"Có lỗi khi vẽ biểu đồ:\n{str(e)}")
                    
        except Exception as e:
            print(f"Error in show_top_n_customers: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self, "Lỗi", 
                f"Đã xảy ra lỗi:\n{str(e)}\n\nVui lòng thử lại."
            )
    
    def show_orders_by_year_country(self):
        """Hiển thị phân bố đơn hàng theo năm và quốc gia"""
        if not self.trans_stat:
            QMessageBox.warning(self, "Lỗi", "Không thể kết nối database!")
            return
        
        df = self.trans_stat.get_orders_by_year_country()
        if df is None or df.empty:
            QMessageBox.warning(self, "Thông báo", "Không có dữ liệu!")
            return
        
        self.show_table(df)
        
        # Vẽ biểu đồ phân bố đơn hàng theo năm ở các quốc gia
        try:
            # Pivot table: Year làm index, Country làm columns
            pivot = df.pivot_table(
                index="Year",
                columns="Country",
                values="OrderCount",
                aggfunc="sum"
            ).fillna(0)
            
            if not pivot.empty:
                self.chart.plot_multi_line(
                    pivot,
                    "Phân bố đơn hàng theo năm ở các quốc gia"
                )
            else:
                QMessageBox.warning(self, "Thông báo", "Không đủ dữ liệu để vẽ biểu đồ!")
        except Exception as e:
            print(f"Error plotting chart: {e}")
            QMessageBox.warning(self, "Cảnh báo", f"Có lỗi khi vẽ biểu đồ:\n{str(e)}")

