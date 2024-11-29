import sys
import MySQLdb as sql
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QPushButton, QLabel, QLineEdit, QApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


def toggle_password_visibility(password_input, button):
    """Toggles the visibility of the password."""
    if password_input.echoMode() == QLineEdit.Password:
        password_input.setEchoMode(QLineEdit.Normal)
        button.setIcon(QIcon("./assets/hide.png"))  # Use an icon for "eye closed"
    else:
        password_input.setEchoMode(QLineEdit.Password)
        button.setIcon(QIcon("./assets/view.png"))  # Use an icon for "eye open"


class Auth(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties (frameless and fixed size)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Removes the title bar
        self.setFixedSize(600, 400)  # Fixes the window size

        # Center the window
        self.center_window()

        # Central widget setup
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)  # Margins around the layout

        # Header layout (for the close button)
        header_layout = QHBoxLayout()
        header_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Custom close button
        close_button = QPushButton("X")
        close_button.setFixedSize(30, 30)
        close_button.setFont(QFont("Arial", 12, QFont.Bold))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        close_button.clicked.connect(self.close)
        header_layout.addWidget(close_button)

        main_layout.addLayout(header_layout)

        # Title label
        label = QLabel("Welcome! Please Log In or Sign Up")
        label.setFont(QFont("Arial", 20))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #0077be;")
        main_layout.addWidget(label)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(QFont("Arial", 14))
        self.username_input.setStyleSheet("padding: 10px; background-color: #f0f0f0;")
        main_layout.addWidget(self.username_input)

        # Password input layout with eye toggle
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Arial", 14))
        self.password_input.setStyleSheet("padding: 10px; background-color: #f0f0f0;")
        password_layout = QHBoxLayout()

        toggle_button = QPushButton()
        toggle_button.setIcon(QIcon("eye.png"))
        toggle_button.setFixedSize(30, 30)
        toggle_button.setStyleSheet("border: none;")
        toggle_button.clicked.connect(lambda: toggle_password_visibility(self.password_input, toggle_button))

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(toggle_button)
        main_layout.addLayout(password_layout)

        # Buttons layout
        button_layout = QVBoxLayout()

        login_button = QPushButton("Log In")
        login_button.setFont(QFont("Arial", 14))
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #0077be;
                color: white;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005fa3;
                color: gray;
            }
        """)
        login_button.clicked.connect(self.login)
        button_layout.addWidget(login_button)

        signup_button = QPushButton("Sign Up")
        signup_button.setFont(QFont("Arial", 14))
        signup_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1e7b31;
                color: gray;
            }
        """)
        signup_button.clicked.connect(self.sign_up)  # Connect button to sign_up function
        button_layout.addWidget(signup_button)

        main_layout.addLayout(button_layout)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.central_widget.setLayout(main_layout)

    def connect_db(self):
        """Connect to the MySQL database."""
        try:
            connection = sql.connect(
                host='localhost',
                user='root',
                password='',
                database='user_accounts'
            )
            return connection
        except sql.MySQLError as e:
            QMessageBox.critical(self, "Database Error", f"Failed to connect: {e}")
            return None

    def sign_up(self):
        """Sign up a new user."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password are required!")
            return

        conn = self.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    query = "INSERT INTO user (username, password) VALUES (%s, %s)"
                    cursor.execute(query, (username, password))
                    conn.commit()
                    QMessageBox.information(self, "Success", "User signed up successfully!")
                    self.username_input.clear()
                    self.password_input.clear()
            except sql.MySQLError as e:
                QMessageBox.critical(self, "Sign-Up Error", f"Error during sign-up: {e}")
            finally:
                conn.close()
        else:
            QMessageBox.critical(self, "Connection Error", "Failed to connect to the database.")

    def login(self):
        """Logs in the user by verifying credentials."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password are required!")
            return

        conn = self.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    query = "SELECT * FROM user WHERE username = %s AND password = %s"
                    cursor.execute(query, (username, password))
                    result = cursor.fetchone()

                    if result:
                        QMessageBox.information(self, "Success", "Login successful!")
                        # Clear input fields and proceed to next window if needed
                        self.username_input.clear()
                        self.password_input.clear()
                    else:
                        QMessageBox.warning(self, "Login Failed", "Invalid username or password!")

            except sql.MySQLError as e:
                QMessageBox.critical(self, "Database Error", f"Error during login: {e}")
            finally:
                conn.close()
        else:
            QMessageBox.critical(self, "Connection Error", "Failed to connect to the database.")

    def center_window(self):
        """Centers the window on the screen."""
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen.center())
        self.move(window_geometry.topLeft())


class MainApp:
    def __init__(self):
        pass


def main():
    app = QApplication(sys.argv)
    window = Auth()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
