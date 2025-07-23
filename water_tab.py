from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QVBoxLayout
import sqlite3
from datetime import date
from database import DB_FILE

class WaterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(DB_FILE)
        layout = QVBoxLayout(self)
        self.buttons_layout = QHBoxLayout()
        self.buttons = []
        for i in range(8):
            btn = QPushButton('💧')
            btn.setCheckable(True)
            btn.clicked.connect(self.update_count)
            self.buttons.append(btn)
            self.buttons_layout.addWidget(btn)
        layout.addLayout(self.buttons_layout)
        self.count_label = QLabel()
        layout.addWidget(self.count_label)
        self.load_count()

    def load_count(self):
        cur = self.conn.cursor()
        today = date.today().isoformat()
        cur.execute('SELECT glasses FROM water WHERE day=?', (today,))
        row = cur.fetchone()
        count = row[0] if row else 0
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i < count)
        self.count_label.setText(f"Glasses: {count}")

    def update_count(self):
        count = sum(1 for b in self.buttons if b.isChecked())
        today = date.today().isoformat()
        cur = self.conn.cursor()
        cur.execute('INSERT OR REPLACE INTO water (day, glasses) VALUES (?, ?)', (today, count))
        self.conn.commit()
        self.count_label.setText(f"Glasses: {count}")

