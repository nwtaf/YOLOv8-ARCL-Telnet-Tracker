import socket
import threading
import time

class TelnetServer:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password.encode('utf-8')
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.clients = []

    def start(self):
        self.server.listen(5)
        print(f"Telnet server started on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        client_socket.send(b"Welcome to the Telnet server\nPassword: ")
        password_attempt = client_socket.recv(1024).strip()

        if password_attempt == self.password:
            client_socket.send(b"Login successful\n")
            self.clients.append(client_socket)
            print(f"New connection from {client_socket.getpeername()}")
        else:
            client_socket.send(b"Invalid password. Closing connection.\n")
            client_socket.close()
            return

        try:
            while True:
                client_socket.send(b"park\n")
                time.sleep(0.1)
                
                data = client_socket.recv(1024).strip()
                if not data:
                    break

                command = data.decode('utf-8')
                response = self.handle_command(command)
                client_socket.send(response.encode('utf-8') + b"\n")
        except Exception as e:
            print(f"Error in client thread: {e}")
        finally:
            print(f"Connection from {client_socket.getpeername()} closed.")
            self.clients.remove(client_socket)
            client_socket.close()

    def handle_command(self, command):
        commands = {
            "analogInputList": "Lists the named analog inputs",
            "odometer": "Shows the robot trip odometer",
        }

        return commands.get(command, "Unknown command")

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 7171
    password = '*******' 

    telnet_server = TelnetServer(host, port, password)
    telnet_server.start()
