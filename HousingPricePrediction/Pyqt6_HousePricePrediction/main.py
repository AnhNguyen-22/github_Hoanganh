import sys
import pickle
from PyQt6 import QtWidgets
from ui.house_price_ui import Ui_MainWindow
from FileUtil import FileUtil

class HousePriceApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.predict_button.clicked.connect(self.predict_price)
        # Load model khi khởi chạy
        self.model = FileUtil.loadmodel("model/housingmodel_2024-07-15_13-30-34.pkl")

    def predict_price(self):
        try:
            values = [
                float(self.area_income.text()),
                float(self.house_age.text()),
                float(self.num_rooms.text()),
                float(self.num_bedrooms.text()),
                float(self.population.text())
            ]
            result = self.model.predict([values])
            self.result_label.setText(f"Predicted Price: ${result[0]:,.2f}")
        except Exception as e:
            self.result_label.setText(f"Error: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HousePriceApp()
    window.show()
    sys.exit(app.exec())
