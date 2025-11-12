# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by ChatGPT based on Qt Designer structure
# Compatible with: PyQt6

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 720)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout_0 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_0.setObjectName("verticalLayout_0")

        # Tabs
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        # ---------------- TAB 0: CRUD EMPLOYEE ----------------
        self.tabEmployee = QtWidgets.QWidget()
        self.tabEmployee.setObjectName("tabEmployee")
        self.horizontalLayout_employee = QtWidgets.QHBoxLayout(self.tabEmployee)
        self.horizontalLayout_employee.setObjectName("horizontalLayout_employee")

        # Left panel: Form
        self.groupEmployeeForm = QtWidgets.QGroupBox(parent=self.tabEmployee)
        self.groupEmployeeForm.setTitle("Employee Information")
        self.groupEmployeeForm.setObjectName("groupEmployeeForm")
        self.formLayoutEmployee = QtWidgets.QFormLayout(self.groupEmployeeForm)
        self.formLayoutEmployee.setObjectName("formLayoutEmployee")

        self.lblEmployeeID = QtWidgets.QLabel(parent=self.groupEmployeeForm)
        self.lblEmployeeID.setText("Employee ID:")
        self.txtEmployeeID = QtWidgets.QLineEdit(parent=self.groupEmployeeForm)
        self.txtEmployeeID.setEnabled(False)
        self.txtEmployeeID.setPlaceholderText("Auto-generated")
        self.txtEmployeeID.setObjectName("txtEmployeeID")
        self.formLayoutEmployee.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lblEmployeeID)
        self.formLayoutEmployee.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtEmployeeID)

        self.lblEmployeeName = QtWidgets.QLabel(parent=self.groupEmployeeForm)
        self.lblEmployeeName.setText("Name:")
        self.txtEmployeeName = QtWidgets.QLineEdit(parent=self.groupEmployeeForm)
        self.txtEmployeeName.setPlaceholderText("Nhập tên")
        self.txtEmployeeName.setObjectName("txtEmployeeName")
        self.formLayoutEmployee.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lblEmployeeName)
        self.formLayoutEmployee.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtEmployeeName)

        self.lblEmployeeEmail = QtWidgets.QLabel(parent=self.groupEmployeeForm)
        self.lblEmployeeEmail.setText("Email:")
        self.txtEmployeeEmail = QtWidgets.QLineEdit(parent=self.groupEmployeeForm)
        self.txtEmployeeEmail.setPlaceholderText("Nhập email")
        self.txtEmployeeEmail.setObjectName("txtEmployeeEmail")
        self.formLayoutEmployee.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lblEmployeeEmail)
        self.formLayoutEmployee.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtEmployeeEmail)

        self.lblEmployeePassword = QtWidgets.QLabel(parent=self.groupEmployeeForm)
        self.lblEmployeePassword.setText("Password:")
        self.txtEmployeePassword = QtWidgets.QLineEdit(parent=self.groupEmployeeForm)
        self.txtEmployeePassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txtEmployeePassword.setPlaceholderText("Nhập mật khẩu")
        self.txtEmployeePassword.setObjectName("txtEmployeePassword")
        self.formLayoutEmployee.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lblEmployeePassword)
        self.formLayoutEmployee.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtEmployeePassword)

        self.lblEmployeeRole = QtWidgets.QLabel(parent=self.groupEmployeeForm)
        self.lblEmployeeRole.setText("Role:")
        self.cboEmployeeRole = QtWidgets.QComboBox(parent=self.groupEmployeeForm)
        self.cboEmployeeRole.addItems(["admin", "technical", "reporter"])
        self.cboEmployeeRole.setObjectName("cboEmployeeRole")
        self.formLayoutEmployee.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lblEmployeeRole)
        self.formLayoutEmployee.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cboEmployeeRole)

        self.btnEmployeeCreate = QtWidgets.QPushButton(parent=self.groupEmployeeForm)
        self.btnEmployeeCreate.setText("Create")
        self.btnEmployeeCreate.setObjectName("btnEmployeeCreate")
        self.btnEmployeeUpdate = QtWidgets.QPushButton(parent=self.groupEmployeeForm)
        self.btnEmployeeUpdate.setText("Update")
        self.btnEmployeeUpdate.setObjectName("btnEmployeeUpdate")
        self.formLayoutEmployee.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.btnEmployeeCreate)
        self.formLayoutEmployee.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.btnEmployeeUpdate)

        self.btnEmployeeDelete = QtWidgets.QPushButton(parent=self.groupEmployeeForm)
        self.btnEmployeeDelete.setText("Delete")
        self.btnEmployeeDelete.setObjectName("btnEmployeeDelete")
        self.btnEmployeeClear = QtWidgets.QPushButton(parent=self.groupEmployeeForm)
        self.btnEmployeeClear.setText("Clear")
        self.btnEmployeeClear.setObjectName("btnEmployeeClear")
        self.formLayoutEmployee.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.btnEmployeeDelete)
        self.formLayoutEmployee.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.btnEmployeeClear)

        self.horizontalLayout_employee.addWidget(self.groupEmployeeForm)

        # Right panel: Table
        self.verticalLayout_employeeRight = QtWidgets.QVBoxLayout()
        self.verticalLayout_employeeRight.setObjectName("verticalLayout_employeeRight")
        self.lblEmployeeTitle = QtWidgets.QLabel(parent=self.tabEmployee)
        self.lblEmployeeTitle.setText("Employee List")
        self.lblEmployeeTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lblEmployeeTitle.setObjectName("lblEmployeeTitle")
        self.verticalLayout_employeeRight.addWidget(self.lblEmployeeTitle)

        self.tableEmployee = QtWidgets.QTableWidget(parent=self.tabEmployee)
        self.tableEmployee.setMinimumSize(QtCore.QSize(600, 400))
        self.tableEmployee.setObjectName("tableEmployee")
        self.verticalLayout_employeeRight.addWidget(self.tableEmployee)

        self.horizontalLayout_employee.addLayout(self.verticalLayout_employeeRight)
        self.tabWidget.addTab(self.tabEmployee, "👥 CRUD Employee")

        # ---------------- TAB 1: Statistics ----------------
        self.tabStatistics = QtWidgets.QWidget()
        self.tabStatistics.setObjectName("tabStatistics")
        self.horizontalLayout_tab1 = QtWidgets.QHBoxLayout(self.tabStatistics)
        self.horizontalLayout_tab1.setObjectName("horizontalLayout_tab1")

        # Left group: functions
        self.groupStatFunctions = QtWidgets.QGroupBox(parent=self.tabStatistics)
        self.groupStatFunctions.setTitle("Functions")
        self.verticalLayout_statLeft = QtWidgets.QVBoxLayout(self.groupStatFunctions)

        # Label tiêu đề
        lblTitle = QtWidgets.QLabel("📊 Phần thống kê")
        lblTitle.setStyleSheet("font-weight: bold; font-size: 12pt;")
        self.verticalLayout_statLeft.addWidget(lblTitle)

        self.btnMaxInvoiceNo = QtWidgets.QPushButton("InvoiceNo lớn nhất")
        self.btnMaxInvoiceNo.setObjectName("btnMaxInvoiceNo")
        self.verticalLayout_statLeft.addWidget(self.btnMaxInvoiceNo)

        self.btnTopNCustomers = QtWidgets.QPushButton("TOP N CustomerID")
        self.btnTopNCustomers.setObjectName("btnTopNCustomers")
        self.verticalLayout_statLeft.addWidget(self.btnTopNCustomers)

        self.btnOrdersByYearCountry = QtWidgets.QPushButton("Phân bố đơn hàng theo năm/quốc gia")
        self.btnOrdersByYearCountry.setObjectName("btnOrdersByYearCountry")
        self.verticalLayout_statLeft.addWidget(self.btnOrdersByYearCountry)

        spacer1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_statLeft.addItem(spacer1)
        self.horizontalLayout_tab1.addWidget(self.groupStatFunctions)

        # Right layout
        self.verticalLayout_statRight = QtWidgets.QVBoxLayout()
        self.lblChartTitle = QtWidgets.QLabel("Chart Visualization")
        self.lblChartTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout_statRight.addWidget(self.lblChartTitle)

        self.chartFrame = QtWidgets.QFrame()
        self.chartFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.chartFrame.setMinimumSize(QtCore.QSize(600, 400))
        self.verticalLayout_statRight.addWidget(self.chartFrame)

        self.tableStats = QtWidgets.QTableWidget()
        self.tableStats.setMinimumSize(QtCore.QSize(600, 150))
        self.verticalLayout_statRight.addWidget(self.tableStats)

        self.horizontalLayout_tab1.addLayout(self.verticalLayout_statRight)
        self.tabWidget.addTab(self.tabStatistics, "📊 Statistics")

        # ---------------- TAB 2: Machine Learning ----------------
        self.tabML = QtWidgets.QWidget()
        self.tabML.setObjectName("tabML")
        self.horizontalLayout_tab2 = QtWidgets.QHBoxLayout(self.tabML)

        # Left panel: Controls
        self.verticalLayout_mlLeft = QtWidgets.QVBoxLayout()
        
        # Group: Clustering
        self.groupCluster = QtWidgets.QGroupBox("Customer Clustering (K-Means)")
        self.horizontalLayout_cluster = QtWidgets.QHBoxLayout(self.groupCluster)
        self.formCluster = QtWidgets.QFormLayout()

        self.lblK = QtWidgets.QLabel("Number of Clusters (k):")
        self.spinK = QtWidgets.QSpinBox(parent=self.groupCluster)
        self.spinK.setMinimum(2)
        self.spinK.setMaximum(10)
        self.spinK.setValue(3)
        self.spinK.setSingleStep(1)  # Tăng/giảm 1 đơn vị mỗi lần
        self.spinK.setEnabled(True)  # Đảm bảo được bật
        self.spinK.setWrapping(False)  # Không wrap khi đạt min/max
        self.spinK.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)  # Hiển thị mũi tên lên/xuống
        self.formCluster.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lblK)
        self.formCluster.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spinK)

        self.btnShowElbow = QtWidgets.QPushButton("Hiển thị Elbow Method")
        self.formCluster.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.btnShowElbow)

        self.btnClusterTrain = QtWidgets.QPushButton("Train K-Means")
        self.formCluster.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.btnClusterTrain)

        self.btnClusterVisual = QtWidgets.QPushButton("Visualize Clusters")
        self.formCluster.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.btnClusterVisual)

        self.lblClusterID = QtWidgets.QLabel("Cluster ID:")
        self.spinClusterID = QtWidgets.QSpinBox(parent=self.groupCluster)
        self.spinClusterID.setMinimum(0)
        self.spinClusterID.setMaximum(9)
        self.spinClusterID.setValue(0)
        self.spinClusterID.setSingleStep(1)  # Tăng/giảm 1 đơn vị mỗi lần
        self.spinClusterID.setEnabled(True)  # Đảm bảo được bật
        self.spinClusterID.setWrapping(False)  # Không wrap khi đạt min/max
        self.spinClusterID.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)  # Hiển thị mũi tên lên/xuống
        self.formCluster.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lblClusterID)
        self.formCluster.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spinClusterID)

        self.btnGetCustomersByCluster = QtWidgets.QPushButton("Lấy Customers theo Cluster")
        self.formCluster.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.btnGetCustomersByCluster)

        self.horizontalLayout_cluster.addLayout(self.formCluster)
        self.verticalLayout_mlLeft.addWidget(self.groupCluster)

        spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_mlLeft.addItem(spacer2)
        self.horizontalLayout_tab2.addLayout(self.verticalLayout_mlLeft)

        # Right panel: Chart and Table
        self.verticalLayout_mlRight = QtWidgets.QVBoxLayout()
        
        self.lblChartTitleML = QtWidgets.QLabel("Chart & Data Visualization")
        self.lblChartTitleML.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout_mlRight.addWidget(self.lblChartTitleML)

        self.chartFrameML = QtWidgets.QFrame()
        self.chartFrameML.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.chartFrameML.setMinimumSize(QtCore.QSize(600, 400))
        self.verticalLayout_mlRight.addWidget(self.chartFrameML)

        self.tableML = QtWidgets.QTableWidget()
        self.tableML.setMinimumSize(QtCore.QSize(600, 150))
        self.verticalLayout_mlRight.addWidget(self.tableML)

        self.horizontalLayout_tab2.addLayout(self.verticalLayout_mlRight)
        self.tabWidget.addTab(self.tabML, "🤖 Machine Learning")

        # ---------------- Add Tabs to main layout ----------------
        self.verticalLayout_0.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Retail Analytics & Machine Learning App"))
