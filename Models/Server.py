import socket
import threading

from Controllers.RoomController import RoomController
from Views.Menu import MenuView
from Models.User import User
from Models.Room import Room

HOST = '127.0.0.1'
PORT = 12347


class Server:
    room = 0
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(5)
        self.room_controller = RoomController()
        
        # Create default 3 rooms
        for room in ['Room1', 'Room2', 'Room3']:
            self.room_controller.create_room(room)
        
        print("Server is running...")
        
        
    def run(self):
        while True:
            client_socket, addr = self.server.accept()
            print(f"{addr} sa pripojil.")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()



    def handle_client(self,client_socket):
        """Spracováva prichádzajúce správy od klienta."""
        room_name = None  
        try:
            # Send startup message
            client_socket.send(MenuView.startup_message().encode())
            
            # LOG-IN
            client_socket.send(MenuView.username_message().encode())
            username = client_socket.recv(1024).decode().strip()
            client_socket.send(MenuView.password_message().encode())
            password = client_socket.recv(1024).decode().strip()
            
            user = User(client_socket,username,password)
            
            # User chooses a room
            while True:
                room_list = MenuView.show_room_list(self.room_controller.room_status()).encode()
                client_socket.send(room_list)
                room_name = client_socket.recv(1024).decode().strip()

                # Check if the room is valid
                if room_name in self.room_controller.rooms:  # Check if room exists
                    self.room_controller.add_user_to_room(client_socket, user, room_name)
                    client_socket.send(MenuView.join_server_message(room_name).encode())
                    break  # Valid room, exit the loop and join the room
                else:
                    client_socket.send("Invalid room choice. Please choose a valid room.\n".encode())
                    continue  # Continue the loop to ask again for a valid room

                
            
            # Room process
            while True:
                try:
                    message = client_socket.recv(1024)
                    if message:
                        message_str = message.decode().strip()
                        # Commands!
                        if message_str.upper() == "DISCONNECT":
                            break
                        elif message_str.upper() == "LEAVE":  # User wants to leave the room
                            self.room_controller.remove_user_from_room(client_socket, room_name)
                            client_socket.send("You have left the room.\n".encode())
                            
                            # After leaving, allow them to join another room
                            client_socket.send(MenuView.show_room_list(self.room_controller.room_status()).encode())
                            room_name = client_socket.recv(1024).decode().strip()
                            
                            if self.room_controller.add_user_to_room(client_socket, user, room_name):
                                client_socket.send(MenuView.join_server_message(room_name).encode())
                            else:
                                client_socket.send("Invalid room choice.\n".encode())
                            
                        else: # No command - message
                            formatted_message = f"{username}: {message_str}\n"
                            print(f"Received message: {formatted_message}")
                            self.room_controller.broadcast_to_room(formatted_message, client_socket, room_name)
                    else:
                        print("No message received. Disconnecting...")
                        break
                except Exception as e:
                    print(f"Error occurred: {e}")
                    break
        # Close connection in the end of all
        finally:
            self.room_controller.remove_user_from_room(client_socket, room_name)
            client_socket.close()

            
        