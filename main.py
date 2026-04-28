import sys
import os
from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow

app = QApplication(sys.argv)

style_path = os.path.join(os.path.dirname(__file__), "styles/style.qss")

if os.path.exists(style_path):
    with open(style_path, "r") as f:
        app.setStyleSheet(f.read())

window = MainWindow()
window.show()

sys.exit(app.exec())