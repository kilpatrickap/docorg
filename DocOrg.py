import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QListView, QLineEdit, QFileDialog, QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Construction Bid Management')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        # Home Screen
        home_label = QLabel('Home Screen - Central Repository')
        main_layout.addWidget(home_label)

        # Upload Button
        upload_button = QPushButton('Upload Document')
        upload_button.clicked.connect(self.upload_document)
        main_layout.addWidget(upload_button)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search...')
        main_layout.addWidget(self.search_bar)

        # Sidebar (Categories)
        self.sidebar = QTreeView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Categories'])
        self.sidebar.setModel(self.model)
        main_layout.addWidget(self.sidebar)

        # File List
        self.file_list = QListView()
        main_layout.addWidget(self.file_list)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def upload_document(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Upload Document', '', 'All Files (*);;Text Files (*.txt)')
        if file:
            self.add_document(file)

    def add_document(self, file):
        item = QStandardItem(file)
        self.model.appendRow(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
