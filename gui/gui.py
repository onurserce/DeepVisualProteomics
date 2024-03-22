from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLineEdit, QVBoxLayout, QWidget, \
    QMessageBox, QLabel
from project_utils import create_new_project, load_project_config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Creator & Loader")

        # Setting the window size to half of the screen size
        screen = QApplication.primaryScreen()
        size = screen.size()
        self.resize(size.width() // 2, size.height() // 2)

        # Centering the window on the screen
        rect = self.frameGeometry()
        center_point = screen.availableGeometry().center()
        rect.moveCenter(center_point)
        self.move(rect.topLeft())

        # Class attributes
        self.config = None
        self.selected_directory = None  # To store the selected directory path
        self.project_info_label = QLabel("No project loaded")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(self.project_info_label)

        self.load_project_button = QPushButton("Load Project")
        self.load_project_button.clicked.connect(self.on_load_project)
        layout.addWidget(self.load_project_button)

        self.select_dir_button = QPushButton("Select Project Directory")
        self.select_dir_button.clicked.connect(self.on_select_directory)
        layout.addWidget(self.select_dir_button)

        self.selected_dir_label = QLabel("Selected directory: None")
        layout.addWidget(self.selected_dir_label)

        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Enter project name")
        layout.addWidget(self.project_name_input)

        self.create_project_button = QPushButton("Create New Project")
        self.create_project_button.clicked.connect(self.on_create_new_project)
        layout.addWidget(self.create_project_button)

        # Reset button to re-enable UI for new project creation or loading
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.on_reset)
        layout.addWidget(self.reset_button)

        self.update_ui_state(reset=True)  # Initialize UI state

    def on_select_directory(self):
        project_dir = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if project_dir:
            self.selected_directory = project_dir
            self.selected_dir_label.setText(f"Selected directory: {project_dir}")
            self.update_ui_state(directory_selected=True)

    def on_create_new_project(self):
        if self.selected_directory:
            project_name = self.project_name_input.text()
            if project_name:
                create_new_project(self.selected_directory, project_name)
                show_message(
                    title='Project Created',
                    message=f"Project '{project_name}' has been successfully created at:\n{self.selected_directory}"
                )
                self.update_ui_state(project_loaded=True)
            else:
                QMessageBox.warning(self, "Project Name Required", "Please enter a project name.")

    def on_load_project(self):
        config_path = QFileDialog.getOpenFileName(self, "Select config.yaml", "", "YAML Files (*.yaml *.yml)")[0]
        if config_path:
            self.config = load_project_config(config_path)
            if self.config:
                self.project_name = self.config.get('project_name', 'Unknown Project')
                self.project_directory = self.config.get('project_directory', 'Unknown Directory')
                self.creation_timestamp = self.config.get('creation_timestamp', 'Unknown Timestamp')
                self.selected_directory = self.project_directory
                self.project_info_label.setText(
                    f"Project Name: {self.project_name}\nDirectory: {self.project_directory}\nCreated: {self.creation_timestamp}")
                self.update_ui_state(project_loaded=True)
            else:
                QMessageBox.warning(self, "Load Project", "Failed to load the project configuration.")
        else:
            QMessageBox.warning(self, "Load Project", "No config file selected.")

    def on_reset(self):
        self.selected_directory = None
        self.config = None
        self.update_ui_state(reset=True)

    def update_ui_state(self, reset=False, directory_selected=False, project_loaded=False):
        """Updates the UI state based on the user action."""
        if reset:
            self.project_name_input.clear()
            self.selected_dir_label.setText("Selected directory: None")
            self.project_info_label.setText("No project loaded")
            self.project_name_input.setEnabled(False)
            self.create_project_button.setEnabled(False)
            self.select_dir_button.setEnabled(True)
            self.load_project_button.setEnabled(True)
        elif directory_selected:
            self.project_name_input.setEnabled(True)
            self.create_project_button.setEnabled(True)
            self.select_dir_button.setEnabled(False)  # Optional: disable if you don't want directory reselection
            self.load_project_button.setEnabled(False)
        elif project_loaded:
            self.project_name_input.setEnabled(False)
            self.create_project_button.setEnabled(False)
            self.select_dir_button.setEnabled(False)
            self.load_project_button.setEnabled(False)
            self.reset_button.setEnabled(True)


def show_message(title: str, message: str, icon: QMessageBox.Icon = QMessageBox.Information) -> None:
    """
    Displays a message box with the specified title, message, and icon.

    This function generalizes the message box display, allowing for various types of messages
    including information, warnings, errors, and success notifications, depending on the icon chosen.

    Parameters:
    - title (str): The title of the message box window.
    - message (str): The message to be displayed in the message box.
    - icon (QMessageBox.Icon, optional): The icon to be displayed in the message box. Defaults to
      QMessageBox.Information indicating an informational message. Other options include QMessageBox.Warning,
      QMessageBox.Error, and QMessageBox.Question which can be used to indicate different types of messages.

    Returns:
    - None
    """
    message_box = QMessageBox()
    message_box.setIcon(icon)
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setStandardButtons(QMessageBox.Ok)
    message_box.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
