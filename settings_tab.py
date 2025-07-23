from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QSpinBox
import sqlite3
from database import DB_FILE

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(DB_FILE)
        layout = QVBoxLayout(self)
        self.dark_mode_cb = QCheckBox('Dark mode')
        self.dark_mode_cb.stateChanged.connect(self.save)
        layout.addWidget(self.dark_mode_cb)

        self.water_goal = QSpinBox()
        self.water_goal.setRange(1, 20)
        layout.addWidget(QLabel('Daily water goal'))
        layout.addWidget(self.water_goal)
        self.water_goal.valueChanged.connect(self.save)

        self.load()

    def load(self):
        cur = self.conn.cursor()
        cur.execute('SELECT value FROM settings WHERE key=?', ('dark_mode',))
        row = cur.fetchone()
        if row:
            self.dark_mode_cb.setChecked(row[0]=='1')
        cur.execute('SELECT value FROM settings WHERE key=?', ('water_goal',))
        row = cur.fetchone()
        if row:
            self.water_goal.setValue(int(row[0]))

    def save(self):
        cur = self.conn.cursor()
        cur.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', ('dark_mode', '1' if self.dark_mode_cb.isChecked() else '0'))
        cur.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', ('water_goal', str(self.water_goal.value())))
        self.conn.commit()

