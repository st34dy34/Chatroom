import socket
import threading

from Controllers.RoomController import RoomController
from Controllers.LoggerController import LoggerController
from Views.Menu import MenuView
from Views.AdminPanel import AdminPanel
from Models.User import User
from Models.Logger import Logger
from config import *

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
        print(AdminPanel.Popup_message())
        
        
    def run(self):
        # Start the admin panel thread (only once)
        admin_panel = threading.Thread(target=self.handle_admin)
        admin_panel.start()
        # Main loop to handle client connections
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
                        # Commands!!!
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
                        else: # Theres No Command!!! ==> aka. message came
                            formatted_message = f"{username}: {message_str}\n"
                            print(f"        Received message: {formatted_message}")
                            self.room_controller.broadcast_to_room(formatted_message, client_socket, room_name)
                            Logger.log(room_name,username,message_str)
                            
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
            
    def handle_admin(self):
        while True:
            cmd = input("Enter command: ")
            cmd_parsed = cmd.split()
            
            command = cmd_parsed[0].upper()
 
            if command == "LOGS":
                if len(cmd_parsed) > 1:  # Check if there's an argument
                    try:
                        arg = int(cmd_parsed[1])  # Convert argument to integer
                        if 1 <= arg <= 5:  # Validate argument range (1-5)
                            result = LoggerController.handle(self, arg)
                            print(result)
                        else:
                            print("Error: Invalid option. Choose a number between 1 and 5.")
                    except ValueError:
                        print("Error: Argument must be a number (1-5).")
                else:
                    print("Error: Missing argument. Usage: LOGS <option>")
            elif command == "HELP":
                print(AdminPanel.Help_message())
            else:
                print(f"Error: Unknown command '{command}'.")
        