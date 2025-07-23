from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLineEdit, QListWidgetItem
from PyQt5.QtCore import Qt
import sqlite3
from database import DB_FILE

class ChecklistTab(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(DB_FILE)
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText('Add item')
        self.line_edit.returnPressed.connect(self.add_item)
        self.list_widget.itemChanged.connect(self.save_state)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.line_edit)
        self.load_items()

    def load_items(self):
        cur = self.conn.cursor()
        cur.execute('SELECT id, text, checked FROM checklist WHERE parent_id IS NULL')
        for item_id, text, checked in cur.fetchall():
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, item_id)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if checked else Qt.Unchecked)
            self.list_widget.addItem(item)

    def add_item(self):
        text = self.line_edit.text().strip()
        if not text:
            return
        cur = self.conn.cursor()
        cur.execute('INSERT INTO checklist (text) VALUES (?)', (text,))
        self.conn.commit()
        self.list_widget.clear()
        self.line_edit.clear()
        self.load_items()

    def save_state(self, item):
        checked = 1 if item.checkState() == Qt.Checked else 0
        item_id = item.data(Qt.UserRole)
        cur = self.conn.cursor()
        cur.execute('UPDATE checklist SET checked=? WHERE id=?', (checked, item_id))
        self.conn.commit()

