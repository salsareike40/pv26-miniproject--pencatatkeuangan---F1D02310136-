from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QHBoxLayout
)
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from views.dialog_form import FormDialog
from controllers.transaksi_controller import TransaksiController
from models.transaksi import Transaksi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pencatat Keuangan")

        self.controller = TransaksiController()

        layout = QVBoxLayout()

        self.btn_tambah = QPushButton("Tambah Data")
        self.btn_edit = QPushButton("Edit Data")
        self.btn_hapus = QPushButton("Hapus Data")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_tambah)
        button_layout.addWidget(self.btn_edit)
        button_layout.addWidget(self.btn_hapus)
        button_layout.setSpacing(10)

        layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tanggal", "Kategori", "Jumlah", "Keterangan", "Tipe"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        self.label_saldo = QLabel("Total Saldo: 0")
        layout.addWidget(self.label_saldo)

        self.label = QLabel("Nama: Salsa Reike Maharani | NIM: F1D02310136")
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.btn_tambah.clicked.connect(self.buka_form)
        self.btn_edit.clicked.connect(self.edit_data)
        self.btn_hapus.clicked.connect(self.hapus_data)

        self.load_data()
        self.create_menu()

    def create_menu(self):
        menu = self.menuBar()
        about = menu.addMenu("Tentang")
        action = about.addAction("Tentang Aplikasi")
        action.triggered.connect(self.show_about)

    def show_about(self):
        QMessageBox.information(
            self, "Tentang", "Aplikasi Pencatat Keuangan\nBy Salsa"
        )

    def buka_form(self):
        dialog = FormDialog()
        dialog.btn_simpan.clicked.connect(lambda: self.simpan_data(dialog))
        dialog.exec()

    def simpan_data(self, dialog):
        data = Transaksi(
            dialog.tanggal.date().toString("yyyy-MM-dd"),
            dialog.kategori.currentText(),
            dialog.jumlah.text(),
            dialog.keterangan.text(),
            dialog.tipe.currentText(),
        )

        self.controller.tambah_data(data)

        QMessageBox.information(self, "Sukses", "Data berhasil disimpan")
        dialog.close()
        self.load_data()

    def load_data(self):
        data = self.controller.ambil_data()
        self.table.setRowCount(len(data))

        total = 0

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

            try:
                jumlah = int(row_data[3])
            except:
                jumlah = 0

            tipe = row_data[5]

            if tipe == "Pemasukan":
                total += jumlah
                for col in range(6):
                    item = self.table.item(row_idx, col)
                    item.setBackground(QColor(34, 139, 34))  
                    item.setForeground(Qt.white)
            else:
                total -= jumlah
                for col in range(6):
                    item = self.table.item(row_idx, col)
                    item.setBackground(QColor(178, 34, 34))  
                    item.setForeground(Qt.white)

        self.label_saldo.setText(f"Total Saldo: {total}")

    def hapus_data(self):
        selected = self.table.currentRow()

        if selected < 0:
            QMessageBox.warning(self, "Warning", "Silakan pilih data yang ingin dihapus!")
            return

        id_data = self.table.item(selected, 0).text()

        konfirmasi = QMessageBox.question(
            self,
            "Konfirmasi",
            f"Yakin ingin menghapus data ID {id_data}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if konfirmasi == QMessageBox.Yes:
            self.controller.hapus_data(id_data)
            QMessageBox.information(self, "Sukses", "Data berhasil dihapus")
            self.load_data()

    def edit_data(self):
        selected = self.table.currentRow()

        if selected < 0:
            QMessageBox.warning(self, "Warning", "Pilih data dulu!")
            return

        data = []
        for col in range(6):
            data.append(self.table.item(selected, col).text())

        dialog = FormDialog(data)
        dialog.btn_simpan.clicked.connect(
            lambda: self.update_data(dialog, data[0])
        )
        dialog.exec()

    def update_data(self, dialog, id):
        data = Transaksi(
            dialog.tanggal.date().toString("yyyy-MM-dd"),
            dialog.kategori.currentText(),
            dialog.jumlah.text(),
            dialog.keterangan.text(),
            dialog.tipe.currentText(),
        )

        self.controller.update_data(id, data)

        QMessageBox.information(self, "Sukses", "Data berhasil diupdate")
        dialog.close()
        self.load_data()