import socket
import sys
import time
from datetime import datetime

class TimeClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.connection = None

    def connect_to_server(self):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.settimeout(5)  # 5 detik timeout
            self.connection.connect((self.server_host, self.server_port))
            return True
        except socket.error as e:
            print(f"❌ Gagal terhubung ke server: {e}", file=sys.stderr)
            return False

    def send_command(self, command):
        try:
            message = f"{command}\r\n"
            self.connection.sendall(message.encode('utf-8'))

            if command == "QUIT":
                return None

            response = self.connection.recv(1024).decode('utf-8').strip()
            return response
        except socket.error as e:
            print(f"⚠️ Terjadi kesalahan saat mengirim/terima data: {e}", file=sys.stderr)
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()


def request_current_time(host, port):
    client = TimeClient(host, port)

    if not client.connect_to_server():
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Tidak dapat menghubungi server.")
        return

    try:
        response = client.send_command("TIME")
        if response:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Respon: {response}")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Tidak ada respon dari server.")
        client.send_command("QUIT")
    finally:
        client.close_connection()


def main():
    SERVER_HOST = '172.16.16.101'
    SERVER_PORT = 45000

    while True:
        user_input = input("\nKetik perintah (TIME untuk waktu, QUIT untuk keluar): ").strip().upper()

        if user_input == "TIME":
            print("\n⏱️ Memulai permintaan waktu sebanyak 5 kali...\n")
            for i in range(5):
                print(f"🔁 Permintaan ke-{i + 1}")
                request_current_time(SERVER_HOST, SERVER_PORT)
                time.sleep(1)
            print("\n✅ Selesai mengirim permintaan.\n")

        elif user_input == "QUIT":
            print("👋 Terima kasih telah menggunakan TimeClient. Keluar dari program.")
            break

        else:
            print("❓ Perintah tidak dikenal. Silakan coba lagi.")


if __name__ == "__main__":
    main()
