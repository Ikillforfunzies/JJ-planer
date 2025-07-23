from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QTimer
import sqlite3
from database import DB_FILE

class NotesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(DB_FILE)
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.save)
        self.timer.start()
        self.load()

    def load(self):
        cur = self.conn.cursor()
        cur.execute('SELECT content FROM notes ORDER BY id DESC LIMIT 1')
        row = cur.fetchone()
        if row:
            self.text_edit.setHtml(row[0])

    def save(self):
        content = self.text_edit.toHtml()
        cur = self.conn.cursor()
        cur.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        self.conn.commit()

