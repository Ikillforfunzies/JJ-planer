from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
import sqlite3
from datetime import date
from database import DB_FILE

class MoodTab(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(DB_FILE)
        layout = QHBoxLayout(self)
        self.buttons = []
        for mood in ['🙂', '😐', '☹️']:
            btn = QPushButton(mood)
            btn.clicked.connect(self.set_mood)
            self.buttons.append(btn)
            layout.addWidget(btn)
        self.load_mood()

    def load_mood(self):
        today = date.today().isoformat()
        cur = self.conn.cursor()
        cur.execute('SELECT mood FROM mood WHERE day=?', (today,))
        row = cur.fetchone()
        if row:
            for b in self.buttons:
                b.setDisabled(False)
            # highlight selected mood
            for b in self.buttons:
                if b.text() == row[0]:
                    b.setDisabled(True)
                    break

    def set_mood(self):
        mood = self.sender().text()
        today = date.today().isoformat()
        cur = self.conn.cursor()
        cur.execute('INSERT OR REPLACE INTO mood (day, mood) VALUES (?, ?)', (today, mood))
        self.conn.commit()
        self.load_mood()

