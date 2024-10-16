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
        home_label = QLabel('Central Repository')
        left_layout.addWidget(home_label)

        # Upload Folder Button and Upload Document Button
        button_layout = QHBoxLayout()
        upload_folder_button = QPushButton('Upload Folder')
        upload_folder_button.clicked.connect(self.upload_folder)
        button_layout.addWidget(upload_folder_button)

        upload_button = QPushButton('Upload Document')
        upload_button.clicked.connect(self.upload_document)
        button_layout.addWidget(upload_button)
        left_layout.addLayout(button_layout)

        # File List
        self.file_list = QTreeView()
        self.file_list.setModel(self.model)
        self.file_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.open_context_menu)
        self.file_list.setAlternatingRowColors(True)
        self.file_list.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)  # Prevent editing on double-click
        self.file_list.doubleClicked.connect(self.double_click_open)  # Connect double-click to open file
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
            self.add_file(file)

    def add_file(self, file_path):
        file_item = QStandardItem(file_path)
        file_item.setFlags(file_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Prevent editing
        self.model.appendRow(file_item)

    def upload_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.add_folder(folder_path)

    def add_folder(self, folder_path):
        folder_item = QStandardItem(folder_path)
        folder_item.setFlags(folder_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Prevent editing
        for root, dirs, files in os.walk(folder_path):
            root_item = QStandardItem(root)
            root_item.setFlags(root_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Prevent editing
            folder_item.appendRow(root_item)
            for dir_name in dirs:
                dir_item = QStandardItem(os.path.join(root, dir_name))
                dir_item.setFlags(dir_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Prevent editing
                root_item.appendRow(dir_item)
            for file_name in files:
                file_item = QStandardItem(os.path.join(root, file_name))
                file_item.setFlags(file_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Prevent editing
                root_item.appendRow(file_item)
        self.model.appendRow(folder_item)

    def double_click_open(self, index: QModelIndex):
        item = self.model.itemFromIndex(index)
        file_path = item.text()
        self.open_file(file_path)

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
        item = self.model.itemFromIndex(index)
        if os.path.isfile(item.text()):
            os.remove(item.text())
        elif os.path.isdir(item.text()):
            os.rmdir(item.text())
        parent = item.parent()
        if parent:
            parent.removeRow(index.row())
        else:
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
