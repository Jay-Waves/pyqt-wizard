import sys
import json
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtNetwork import QTcpServer, QHostAddress, QTcpSocket


class Server(QTcpServer):
    def __init__(self):
        super().__init__()
        self.newConnection.connect(self.on_new_connection)

    def start(self):
        self.listen(QHostAddress.SpecialAddress.LocalHost, 5555)

    def on_new_connection(self):
        self.client_socket = self.nextPendingConnection()
        self.client_socket.readyRead.connect(self.on_ready_read)

    def on_ready_read(self):
        message = self.client_socket.readAll().data()
        data = json.loads(message.decode())

        response = {'status': 'received', 'message': message}
        self.client_socket.write(json.dumps(response).encode())

        show_dialog(f"Received JSON data: {data}")


        self.client_socket.disconnectFromHost()
        self.close()

def show_dialog(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setText(message)
    msg.setWindowTitle("Server")
    msg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = Server()
    server.start()
    sys.exit(app.exec())
