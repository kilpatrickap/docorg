import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QTreeView, QMenu, QSplitter
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QPoint, QModelIndex

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Bid Manager')
        self.setGeometry(100, 100, 800, 600)  # Adjusted width for two columns

        main_layout = QHBoxLayout()  # Main layout as a horizontal layout

        # Initialize the model first
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['File List'])

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left Column (File List)
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        # Home Screen
        home_label = QLabel('Home Screen - Central Repository')
        left_layout.addWidget(home_label)

        # Upload Button
        upload_button = QPushButton('Upload Document')
        upload_button.clicked.connect(self.upload_document)
        left_layout.addWidget(upload_button)

        # File List
        self.file_list = QTreeView()
        self.file_list.setModel(self.model)
        self.file_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.open_context_menu)
        left_layout.addWidget(self.file_list)

        # Search Bar and Button
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search...')
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.search_documents)
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(search_button)
        left_layout.addLayout(search_layout)

        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)

        # Right Column (Empty for future use)
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        empty_label = QLabel('Right Column - Empty for future use')
        right_layout.addWidget(empty_label)
        right_widget.setLayout(right_layout)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

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

    def open_context_menu(self, position: QPoint):
        index = self.file_list.indexAt(position)
        if not index.isValid():
            return
        item = self.model.itemFromIndex(index)
        file_path = item.text()

        menu = QMenu()
        open_action = menu.addAction("Open")
        delete_action = menu.addAction("Delete")

        action = menu.exec(self.file_list.viewport().mapToGlobal(position))
        if action == open_action:
            self.open_file(file_path)
        elif action == delete_action:
            self.delete_document(index)

    def open_file(self, file_path):
        os.startfile(file_path)  # This is for Windows. Use 'open' for macOS and 'xdg-open' for Linux.

    def delete_document(self, index: QModelIndex):
        self.model.removeRow(index.row())

    def search_documents(self):
        query = self.search_bar.text()
        print(f"Search query: {query}")  # Placeholder for actual search functionality

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
