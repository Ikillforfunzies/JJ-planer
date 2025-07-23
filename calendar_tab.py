from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QListWidget, QPushButton, QHBoxLayout, QLineEdit, QColorDialog
from PyQt5.QtCore import QDate
import sqlite3
from database import DB_FILE

class CalendarTab(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(DB_FILE)
        self.layout = QVBoxLayout(self)
        self.calendar = QCalendarWidget()
        self.events_list = QListWidget()

        self.input_line = QLineEdit()
        self.add_btn = QPushButton("Add Event")
        self.add_btn.clicked.connect(self.add_event)

        top = QHBoxLayout()
        top.addWidget(self.input_line)
        top.addWidget(self.add_btn)

        self.layout.addWidget(self.calendar)
        self.layout.addLayout(top)
        self.layout.addWidget(self.events_list)

        self.calendar.selectionChanged.connect(self.load_events)
        self.load_events()

    def add_event(self):
        text = self.input_line.text().strip()
        if not text:
            return
        date = self.calendar.selectedDate().toString('yyyy-MM-dd')
        cur = self.conn.cursor()
        cur.execute('INSERT INTO events (title, start, end, color) VALUES (?, ?, ?, ?)',
                    (text, date, date, '#c2e33d'))
        self.conn.commit()
        self.input_line.clear()
        self.load_events()

    def load_events(self):
        self.events_list.clear()
        date = self.calendar.selectedDate().toString('yyyy-MM-dd')
        cur = self.conn.cursor()
        cur.execute('SELECT title FROM events WHERE date(start)=?', (date,))
        for row in cur.fetchall():
            self.events_list.addItem(row[0])

