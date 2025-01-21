import socket
import threading

HOST = '127.0.0.1'
PORT = 12347

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((HOST, PORT))
            print("Connected to the server.")
        except Exception as e:
            print(f"Unable to connect: {e}")
            return

        self.running = True

    def send_messages(self):
        """Handle sending messages to the server."""
        try:
            while self.running:
                message = input("")
                if message.lower() == "exit":
                    self.running = False
                    self.client.send("DISCONNECT".encode())
                    break
                self.client.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")
        finally:
            self.client.close()

    def receive_messages(self):
        """Handle receiving messages from the server."""
        try:
            while self.running:
                message = self.client.recv(1024).decode()
                if not message:
                    print("Disconnected from server.")
                    break
                print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
        finally:
            self.running = False
            self.client.close()

    def run(self):
        """Start the client."""
        # Create a thread to listen for incoming messages
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()

        # Handle sending messages
        self.send_messages()

