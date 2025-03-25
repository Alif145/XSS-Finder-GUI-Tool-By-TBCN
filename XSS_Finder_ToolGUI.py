import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup

# Load XSS payloads from file
def load_payloads():
    try:
        with open("payload.txt", "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]

xss_payloads = load_payloads()

class XSSFinder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XSS Finder")
        self.setFixedSize(1200, 800)
        self.setStyleSheet(self.get_dark_theme())
        self.setWindowIcon(QIcon("logo.jpg"))
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel("XSS Finder")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter the URL >>>")
        self.url_input.setFont(QFont("Arial", 14))
        layout.addWidget(self.url_input)
        
        self.start_button = QPushButton("Start XSS Scan")
        self.start_button.setFixedHeight(60)
        self.start_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.start_button.clicked.connect(self.start_scan)
        layout.addWidget(self.start_button)
        
        self.clear_button = QPushButton("Clear Results")
        self.clear_button.setFixedHeight(60)
        self.clear_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.clear_button.clicked.connect(lambda: self.results_text.clear())
        layout.addWidget(self.clear_button)
        
        self.results_text = QTextEdit(self)
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("Results will be shown here...")
        self.results_text.setFont(QFont("Arial", 14))
        layout.addWidget(self.results_text)
        
        self.footer_label = QLabel("""
        THIS TOOL MAKE BY TEAM BD CYBER NINJA OFFICIAL
        CREDITS (ZEROX-UCHIHA) WITH (Dark_C0dex)
        JOIN OUR OFFICIAL TELEGRAM CHANNEL - t.me/teambdcyberninjaofc
        Mail - teambdcyberninjaorg@gmail.com/teambdcyberninjaofc@gmail.com
        """)
        self.footer_label.setFont(QFont("Arial", 7, QFont.StyleItalic))
        self.footer_label.setAlignment(Qt.AlignRight)
        self.footer_label.setStyleSheet("color: red;")
        layout.addWidget(self.footer_label)
        
        self.setLayout(layout)

    def start_scan(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a valid URL.")
            return

        self.results_text.clear()
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            
            if not forms:
                self.results_text.setText("No forms found on this page.")
                return

            self.results_text.append(f"Found {len(forms)} forms. Testing for XSS...")
            for form in forms:
                form_action = form.get('action', '')
                test_url = url + form_action
                self.test_xss(test_url)
        except requests.RequestException as e:
            QMessageBox.critical(self, "Request Error", f"Error fetching URL: {e}")

    def test_xss(self, test_url):
        for payload in xss_payloads:
            xss_url = f"{test_url}?test={payload}"
            try:
                response = requests.get(xss_url)
                if payload in response.text:
                    self.results_text.append(f"Possible XSS found: {xss_url}")
            except requests.RequestException:
                self.results_text.append(f"Error testing: {xss_url}")

    def get_dark_theme(self):
        return """
            QWidget { background-color: #1e1e1e; color: #00ff00; }
            QLineEdit, QTextEdit { background-color: #000; color: #00ff00; border: 1px solid #00ff00; font-size: 14pt; }
            QPushButton { background-color: #008000; color: white; border-radius: 5px; height: 60px; font-size: 18pt; }
            QPushButton:hover { background-color: #00b300; }
            QLabel { font-size: 16pt; color: #00ff00; }
        """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = XSSFinder()
    window.show()
    sys.exit(app.exec_())
