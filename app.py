import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from database import init_db
from calendar_tab import CalendarTab
from water_tab import WaterTab
from mood_tab import MoodTab
from checklist_tab import ChecklistTab
from notes_tab import NotesTab
from recommendations_tab import RecommendationsTab
from settings_tab import SettingsTab

class Planner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Digital Planner')
        self.resize(800, 600)
        tabs = QTabWidget()
        tabs.addTab(CalendarTab(), 'Calendar')
        tabs.addTab(WaterTab(), 'Water Intake')
        tabs.addTab(MoodTab(), 'Mood Tracker')
        tabs.addTab(ChecklistTab(), 'Checklist')
        tabs.addTab(NotesTab(), 'Free Area')
        tabs.addTab(RecommendationsTab(), 'Recommendations')
        tabs.addTab(SettingsTab(), 'Settings')
        self.setCentralWidget(tabs)

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    win = Planner()
    win.show()
    sys.exit(app.exec_())

