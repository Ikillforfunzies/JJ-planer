from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLineEdit, QPushButton, QListWidgetItem, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
import sqlite3
from database import DB_FILE

class RecommendationsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(DB_FILE)
        layout = QVBoxLayout(self)
        filter_layout = QHBoxLayout()
        self.category_filter = QComboBox()
        self.category_filter.addItem('All')
        self.category_filter.currentTextChanged.connect(self.load_items)
        filter_layout.addWidget(self.category_filter)
        layout.addLayout(filter_layout)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        input_layout = QHBoxLayout()
        self.input_cat = QLineEdit()
        self.input_cat.setPlaceholderText('category')
        self.input_item = QLineEdit()
        self.input_item.setPlaceholderText('item')
        add_btn = QPushButton('Add')
        add_btn.clicked.connect(self.add_item)
        input_layout.addWidget(self.input_cat)
        input_layout.addWidget(self.input_item)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)
        self.load_items()
        self.load_categories()

    def load_categories(self):
        cur = self.conn.cursor()
        cur.execute('SELECT DISTINCT category FROM recommendations')
        for (cat,) in cur.fetchall():
            if cat not in [self.category_filter.itemText(i) for i in range(self.category_filter.count())]:
                self.category_filter.addItem(cat)

    def add_item(self):
        category = self.input_cat.text().strip()
        item = self.input_item.text().strip()
        if not item:
            return
        cur = self.conn.cursor()
        cur.execute('INSERT INTO recommendations (category, item) VALUES (?, ?)', (category, item))
        self.conn.commit()
        self.input_item.clear()
        self.load_items()
        self.load_categories()

    def load_items(self):
        self.list_widget.clear()
        category = self.category_filter.currentText()
        cur = self.conn.cursor()
        if category == 'All':
            cur.execute('SELECT id, category, item, liked FROM recommendations')
        else:
            cur.execute('SELECT id, category, item, liked FROM recommendations WHERE category=?', (category,))
        for id_, cat, item, liked in cur.fetchall():
            lw_item = QListWidgetItem(f"[{cat}] {item}")
            lw_item.setData(Qt.UserRole, id_)
            lw_item.setFlags(lw_item.flags() | Qt.ItemIsUserCheckable)
            lw_item.setCheckState(Qt.Checked if liked else Qt.Unchecked)
            self.list_widget.addItem(lw_item)
        self.list_widget.itemChanged.connect(self.toggle_like)

    def toggle_like(self, item):
        liked = 1 if item.checkState() == Qt.Checked else 0
        rec_id = item.data(Qt.UserRole)
        cur = self.conn.cursor()
        cur.execute('UPDATE recommendations SET liked=? WHERE id=?', (liked, rec_id))
        self.conn.commit()

