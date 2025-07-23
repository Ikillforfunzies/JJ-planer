import sys
import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore

DB_NAME = "planner.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # events table
    cur.execute(
        """CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start DATETIME,
            end DATETIME,
            color TEXT
        )"""
    )
    # water intake
    cur.execute(
        """CREATE TABLE IF NOT EXISTS water(
            day DATE PRIMARY KEY,
            glasses INTEGER DEFAULT 0
        )"""
    )
    # mood
    cur.execute(
        """CREATE TABLE IF NOT EXISTS mood(
            day DATE PRIMARY KEY,
            mood TEXT
        )"""
    )
    # checklist
    cur.execute(
        """CREATE TABLE IF NOT EXISTS checklist(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            checked INTEGER DEFAULT 0,
            parent_id INTEGER,
            FOREIGN KEY(parent_id) REFERENCES checklist(id)
        )"""
    )
    # notes
    cur.execute(
        """CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )"""
    )
    # recommendations
    cur.execute(
        """CREATE TABLE IF NOT EXISTS recommendations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            item TEXT,
            liked INTEGER DEFAULT 0
        )"""
    )
    # settings
    cur.execute(
        """CREATE TABLE IF NOT EXISTS settings(
            key TEXT PRIMARY KEY,
            value TEXT
        )"""
    )
    conn.commit()
    conn.close()


class CalendarTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("Calendar view coming soon")
        layout.addWidget(label)


class WaterTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        self.buttons = []
        for i in range(8):
            btn = QtWidgets.QPushButton("\U0001F4A7")  # water drop emoji
            btn.setCheckable(True)
            btn.clicked.connect(self.update_glasses)
            self.buttons.append(btn)
            layout.addWidget(btn)
        self.setLayout(layout)

    def update_glasses(self):
        glasses = sum(1 for b in self.buttons if b.isChecked())
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "REPLACE INTO water(day, glasses) VALUES(date('now'), ?)",
            (glasses,),
        )
        conn.commit()
        conn.close()


class MoodTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        for mood in ["🙂", "😐", "☹️"]:
            btn = QtWidgets.QPushButton(mood)
            btn.clicked.connect(lambda _, m=mood: self.set_mood(m))
            layout.addWidget(btn)
        self.setLayout(layout)

    def set_mood(self, mood):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "REPLACE INTO mood(day, mood) VALUES(date('now'), ?)",
            (mood,),
        )
        conn.commit()
        conn.close()


class ChecklistTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.list_widget = QtWidgets.QListWidget()
        layout.addWidget(self.list_widget)
        self.input = QtWidgets.QLineEdit()
        self.input.setPlaceholderText("Add item...")
        layout.addWidget(self.input)
        self.input.returnPressed.connect(self.add_item)

    def add_item(self):
        text = self.input.text()
        if not text:
            return
        item = QtWidgets.QListWidgetItem(text)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.list_widget.addItem(item)
        self.input.clear()


class NotesTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.text_edit = QtWidgets.QTextEdit()
        layout.addWidget(self.text_edit)


class RecommendationsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Recommendations coming soon"))


class SettingsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Settings coming soon"))


class PlannerApp(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Planner")
        self.resize(800, 600)
        self.addTab(CalendarTab(), "Calendar")
        self.addTab(WaterTab(), "Water")
        self.addTab(MoodTab(), "Mood")
        self.addTab(ChecklistTab(), "Checklist")
        self.addTab(NotesTab(), "Free Area")
        self.addTab(RecommendationsTab(), "Recommend")
        self.addTab(SettingsTab(), "Settings")


def main():
    init_db()
    app = QtWidgets.QApplication(sys.argv)
    planner = PlannerApp()
    planner.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
