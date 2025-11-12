# app.py
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor

from UI.MainWindowEx import MainWindowEx
from UI.LoginWindowEx import LoginWindowEx


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Force light theme palette để đảm bảo hiển thị đúng trên mọi hệ thống
    palette = QPalette()
    
    # Window colors - Light
    palette.setColor(QPalette.ColorRole.Window, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#1A1A1A"))
    
    # Base colors - Light
    palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#F9F9F9"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#1A1A1A"))
    
    # Button colors
    palette.setColor(QPalette.ColorRole.Button, QColor("#9CAFAA"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))
    
    # Highlight colors
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#9CAFAA"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
    
    # Tooltip colors
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#1A1A1A"))
    
    app.setPalette(palette)
    
    # Hiển thị màn hình đăng nhập
    login_window = LoginWindowEx()
    
    if login_window.exec() == login_window.DialogCode.Accepted:
        # Đăng nhập thành công, lấy thông tin user
        user_info = login_window.get_user_info()
        
        if user_info:
            # Hiển thị màn hình chính với thông tin user
            win = MainWindowEx(user_info=user_info)
            win.show()
            sys.exit(app.exec())
        else:
            sys.exit(0)
    else:
        # Người dùng hủy đăng nhập hoặc đóng cửa sổ
        sys.exit(0)
