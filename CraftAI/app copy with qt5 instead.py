import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCursor, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QWidget, QFileDialog, QTextEdit, QComboBox, QScrollArea
)
from PyQt5.QtGui import QImageReader


class StartupAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")
        self.label = QLabel("CraftAI", self)
        self.label.setStyleSheet("color: white; font-size: 50px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def showEvent(self, event):
        QTimer.singleShot(2000, self.close)  # Show for 2 seconds, then close.


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121212; color: white;")
        
        # Persistent header
        self.header = QLabel("CraftAI")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.subheader = QLabel("Applications for the lazy")
        self.subheader.setStyleSheet("font-size: 14px; font-style: italic; color: #bbbbbb;")
        
        header_layout = QVBoxLayout()
        header_layout.addWidget(self.header)
        header_layout.addWidget(self.subheader)
        header_layout.setAlignment(Qt.AlignTop)

        # Section 1: Provide Relevant Documents
        doc_section = QVBoxLayout()
        doc_title = QLabel("Provide Relevant Documents (max 4)")
        doc_title.setStyleSheet("font-size: 18px;")

        self.file_preview = QLabel()
        self.file_preview.setFixedSize(150, 150)
        self.file_preview.setStyleSheet(
            "background-color: #333333; border-radius: 10px; border: 1px dashed #444444;"
        )
        self.file_preview.setAlignment(Qt.AlignCenter)
        self.file_preview.setText("No File Selected")

        self.doc_button = QPushButton("Choose File")
        self.doc_button.setStyleSheet(
            "background-color: #1e90ff; color: white; border-radius: 10px; padding: 10px;"
        )
        self.doc_button.clicked.connect(self.load_file_preview)

        doc_section.addWidget(doc_title)
        doc_section.addWidget(self.file_preview, alignment=Qt.AlignLeft)
        doc_section.addWidget(self.doc_button, alignment=Qt.AlignLeft)

        # Section 2: Provide Questions
        question_section = QVBoxLayout()
        question_title = QLabel("Provide Questions")
        question_title.setStyleSheet("font-size: 18px;")

        self.question_mode_dropdown = QComboBox()
        self.question_mode_dropdown.addItems(["Text", "File"])
        self.question_mode_dropdown.setStyleSheet(
            "background-color: #333333; color: white; border: none; padding: 5px; border-radius: 10px;"
        )
        self.question_mode_dropdown.currentIndexChanged.connect(self.update_question_mode)

        self.question_text_box = QTextEdit()
        self.question_text_box.setPlaceholderText("Enter each question on a new line")
        self.question_text_box.setFixedHeight(90)
        self.question_text_box.setStyleSheet(
            "background-color: #333333; color: white; border-radius: 10px; padding: 5px; "
        )
        self.question_text_box.textChanged.connect(self.adjust_question_box_height)

        self.question_file_button = QPushButton("Choose File")
        self.question_file_button.setVisible(False)
        self.question_file_button.setStyleSheet(
            "background-color: #1e90ff; color: white; border-radius: 10px; padding: 10px;"
        )
        self.question_file_button.clicked.connect(self.load_file_preview)

        question_section.addWidget(question_title)
        question_section.addWidget(self.question_mode_dropdown)
        question_section.addWidget(self.question_text_box)
        question_section.addWidget(self.question_file_button)

        # Section 3: Style (optional)
        style_section = QVBoxLayout()
        style_title = QLabel("Style (optional)")
        style_title.setStyleSheet("font-size: 18px;")

        style_dropdown = QComboBox()
        style_dropdown.addItems(["Formal", "Casual"])
        style_dropdown.setStyleSheet(
            "background-color: #333333; color: white; border: none; padding: 5px; border-radius: 10px;"
        )

        style_note = QLabel("Choose how you want the response to sound.")
        style_note.setStyleSheet("font-size: 12px; color: #bbbbbb;")

        style_section.addWidget(style_title)
        style_section.addWidget(style_dropdown)
        style_section.addWidget(style_note)

        # Footer
        next_button = QPushButton("Next")
        next_button.setStyleSheet(
            "background-color: #1e90ff; color: white; font-size: 16px; padding: 10px; border-radius: 10px;"
        )
        next_button.setFixedSize(100, 40)

        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        footer_layout.addWidget(next_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(doc_section)
        main_layout.addSpacing(20)
        main_layout.addLayout(question_section)
        main_layout.addSpacing(20)
        main_layout.addLayout(style_section)
        main_layout.addStretch()
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)

    def load_file_preview(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose File")
        if file_name:
            image_reader = QImageReader(file_name)
            pixmap = QPixmap.fromImageReader(image_reader)
            scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.file_preview.setPixmap(scaled_pixmap)
        else:
            self.file_preview.setText("No File Selected")

    def update_question_mode(self, index):
        if index == 0:  # Text mode
            self.question_text_box.setVisible(True)
            self.question_file_button.setVisible(False)
        elif index == 1:  # File mode
            self.question_text_box.setVisible(False)
            self.question_file_button.setVisible(True)

    def adjust_question_box_height(self):
        document = self.question_text_box.document()
        line_count = document.blockCount()
        self.question_text_box.setFixedHeight(min(90 + (line_count - 3) * 20, 300))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CraftAI")
        self.showFullScreen()

        self.startup = StartupAnimation()
        self.startup.setFixedSize(self.size())

        self.home_page = HomePage()
        self.setCentralWidget(self.startup)
        QTimer.singleShot(2000, self.show_home)

    def show_home(self):
        self.setCentralWidget(self.home_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set dark theme
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(18, 18, 18))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(36, 36, 36))
    dark_palette.setColor(QPalette.AlternateBase, QColor(18, 18, 18))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(36, 36, 36))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)

    app.setPalette(dark_palette)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
