import sys
import json
from PyQt6.QtWidgets import QApplication
from PyQt6.QtNetwork import QTcpSocket


class Client:
    def __init__(self):
        self.socket = QTcpSocket()
        self.socket.connected.connect(self.on_connected)
        self.socket.connectToHost("localhost", 5555)

    def on_connected(self):
        data = {
            'name': 'John Doe',
            'age': 30,
            'city': 'New York'
        }
        message = json.dumps(data).encode()
        self.socket.write(message)
    
    def on_ready_read(self):
        message = self.socket.readAll().data().decode()
        data = json.loads(message)
        show_dialog(f"Received JSON data: {data}")
        
def show_dialog(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setText(message)
    msg.setWindowTitle("Client")
    msg.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec())
