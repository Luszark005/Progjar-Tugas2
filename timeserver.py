import socket
import threading
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

class TimeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _handle_client(self, client_socket, client_address):
        logging.info(f"Koneksi diterima dari {client_address}")
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    logging.warning(f"Koneksi dari {client_address} terputus.")
                    break

                request = data.decode('utf-8')
                logging.info(f"Menerima perintah {repr(request)} dari {client_address}")

                if not request.endswith('\r\n'):
                    client_socket.sendall(b"INVALID COMMAND\r\n")
                    continue

                command = request.strip()

                if command == "TIME":
                    sekarang = datetime.now()
                    waktu_format = sekarang.strftime("%H:%M:%S")
                    response = f"JAM {waktu_format}\r\n"
                    client_socket.sendall(response.encode('utf-8'))
                elif command == "QUIT":
                    break
                else:
                    client_socket.sendall(b"INVALID COMMAND\r\n")

        except ConnectionResetError:
            logging.warning(f"Koneksi dari {client_address} direset secara paksa.")
        except Exception as e:
            logging.error(f"Error pada koneksi {client_address}: {e}")
        finally:
            logging.info(f"Menutup koneksi dengan {client_address}")
            client_socket.close()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        logging.info(f"Server berjalan dan mendengarkan di {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            logging.info("Server dihentikan oleh pengguna.")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 45000
    server = TimeServer(HOST, PORT)
    server.start()
