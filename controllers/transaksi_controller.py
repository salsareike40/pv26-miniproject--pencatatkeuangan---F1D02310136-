from database.db import Database

class TransaksiController:
    def __init__(self):
        self.db = Database()

    def tambah_data(self, transaksi):
        self.db.insert((
            transaksi.tanggal,
            transaksi.kategori,
            transaksi.jumlah,
            transaksi.keterangan,
            transaksi.tipe
        ))

    def ambil_data(self):
        return self.db.fetch()

    def hapus_data(self, id):
        self.db.delete(id)

    def update_data(self, id, transaksi):
        self.db.update(id, (
            transaksi.tanggal,
            transaksi.kategori,
            transaksi.jumlah,
            transaksi.keterangan,
            transaksi.tipe
        ))