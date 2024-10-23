import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTreeView, QFileDialog, QMenu, QSplitter
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QPoint
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the GUI elements."""
        self.setWindowTitle('Local FTP Server')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        # Start Server Button
        start_server_button = QPushButton('Start Server')
        start_server_button.clicked.connect(self.start_server)
        main_layout.addWidget(start_server_button)

        # Upload Folder Button
        upload_folder_button = QPushButton('Upload Folder')
        upload_folder_button.clicked.connect(self.upload_folder)
        main_layout.addWidget(upload_folder_button)

        # File List View
        self.file_list = QTreeView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Shared Files'])
        self.file_list.setModel(self.model)
        self.file_list.setAlternatingRowColors(True)
        main_layout.addWidget(self.file_list)

        # Set the layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def start_server(self):
        """Start the FTP server in a separate thread."""
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def run_server(self):
        """Run the FTP server."""
        authorizer = DummyAuthorizer()
        # Add a user with username 'user' and password '12345'
        authorizer.add_user("user", "12345", "shared", perm="elradfmw")
        handler = FTPHandler
        handler.authorizer = authorizer
        # Start the FTP server on port 21
        server = FTPServer(('192.168.1.48', 21), handler)
        print('Serving on port 21')
        server.serve_forever()

    def upload_folder(self):
        """Prompt the user to select a folder to upload and copy it to the shared directory."""
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder to Share')
        if folder_path:
            dest_path = os.path.join('shared', os.path.basename(folder_path))
            shutil.copytree(folder_path, dest_path, dirs_exist_ok=True)
            self.add_to_model(dest_path)

    def add_to_model(self, path):
        """Add the uploaded folder to the QTreeView model."""
        folder_item = QStandardItem(path)
        folder_item.setFlags(folder_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.model.appendRow(folder_item)

if __name__ == '__main__':
    # Ensure the 'shared' directory exists
    os.makedirs('shared', exist_ok=True)
    # Create the application and main window
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    # Run the application
    sys.exit(app.exec())
