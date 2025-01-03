import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent, QFont, QKeySequence, QPalette, QColor, QTextCursor
from datetime import datetime
import time

def yyyy_mm_dd_hh_mm_ss():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def writefile(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def readfile(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

last_bak = 0.0

class TypewriterEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Courier", 12))

        # Load initial content
        try:
            initial_content = readfile('start.txt')
            self.setPlainText(initial_content)
        except:
            pass  # If file doesn't exist, start empty

        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                border: none;
            }
        """)

        self.setTextInteractionFlags(Qt.TextEditorInteraction)

        # Setup autosave timer
        self.save_timer = QTimer()
        self.save_timer.timeout.connect(self.save_to_file)
        self.save_timer.start(1000)  # Save every 1000ms (1 second)

    def save_to_file(self):
        global last_bak
        content = self.toPlainText()
        if time.time() - last_bak > 120:
            last_bak = time.time()
            writefile(f'baks/{yyyy_mm_dd_hh_mm_ss()}.txt', content)
        writefile('file.txt', content)


    def keyPressEvent(self, e: QKeyEvent):
        if e.key() in (Qt.Key_Backspace, Qt.Key_Delete):
            return

        if e.matches(QKeySequence.Paste):
            return

        self.moveCursor(QTextCursor.End)
        super().keyPressEvent(e)

    def mousePressEvent(self, e):
        e.ignore()

    def mouseReleaseEvent(self, e):
        e.ignore()

    def mouseMoveEvent(self, e):
        e.ignore()

class TypewriterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.time_remaining = 5 * 60  # 5 minutes in seconds
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Typewriter')
        self.setStyleSheet("background-color: #1e1e1e;")

        # Create main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Create timer label
        self.timer_label = QLabel()
        self.timer_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-family: Courier;
                font-size: 14px;
                padding: 10px;
            }
        """)
        self.update_timer_display()

        # Setup countdown timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)  # Update every second

        # Create editor
        self.editor = TypewriterEditor()

        # Add widgets to layout
        layout.addWidget(self.timer_label)
        layout.addWidget(self.editor)

        # Set layout margins
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Set the layout
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Show in fullscreen
        self.showFullScreen()

    def update_countdown(self):

        if self.time_remaining <= 0:
            self.editor.save_to_file()
            # self.close()
        else:
            self.update_timer_display()
            self.time_remaining -= 1

    def update_timer_display(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label.setText(f"Time remaining: {minutes:02d}:{seconds:02d}")

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.key() == Qt.Key_Escape:
            self.editor.save_to_file()
            self.close()
        else:
            super().keyPressEvent(a0)

def main():
    app = QApplication(sys.argv)

    # Set dark theme for the entire application
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(0, 255, 0))
    palette.setColor(QPalette.Text, QColor(0, 255, 0))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)

    window = TypewriterWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
