import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            kategori TEXT,
            jumlah INTEGER,
            keterangan TEXT,
            tipe TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert(self, data):
        self.conn.execute(
            "INSERT INTO transaksi (tanggal, kategori, jumlah, keterangan, tipe) VALUES (?, ?, ?, ?, ?)", 
            data
        )
        self.conn.commit()

    def fetch(self):
        return self.conn.execute("SELECT * FROM transaksi").fetchall()

    def delete(self, id):
        self.conn.execute("DELETE FROM transaksi WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, data):
        self.conn.execute("""
            UPDATE transaksi 
            SET tanggal=?, kategori=?, jumlah=?, keterangan=?, tipe=?
            WHERE id=?
        """, (*data, id))
        self.conn.commit()