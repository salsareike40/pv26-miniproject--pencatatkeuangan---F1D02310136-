from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QComboBox, QDateEdit
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QDate

class FormDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.setWindowTitle("Form Transaksi")

        layout = QFormLayout()

        self.tanggal = QDateEdit()
        self.tanggal.setCalendarPopup(True)
        self.tanggal.setDate(QDate.currentDate())
        self.kategori = QComboBox()
        self.kategori.addItems([
            "Makan",
            "Transport",
            "Belanja",
            "Gaji",
            "Pulsa",
            "Lainnya"
        ])
        self.jumlah = QLineEdit()
        self.jumlah.setValidator(QIntValidator())
        self.keterangan = QLineEdit()
        self.tipe = QComboBox()
        self.tipe.addItems(["Pemasukan", "Pengeluaran"])

        self.btn_simpan = QPushButton("Simpan")

        layout.addRow("Tanggal", self.tanggal)
        layout.addRow("Kategori", self.kategori)
        layout.addRow("Jumlah", self.jumlah)
        layout.addRow("Keterangan", self.keterangan)
        layout.addRow("Tipe", self.tipe)
        layout.addWidget(self.btn_simpan)

        self.setLayout(layout)

        if data:
            self.tanggal.setDate(QDate.fromString(data[1], "yyyy-MM-dd"))
            self.kategori.setCurrentText(data[2])
            self.jumlah.setText(str(data[3]))
            self.keterangan.setText(data[4])
            self.tipe.setCurrentText(data[5])