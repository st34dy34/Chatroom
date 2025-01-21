from Models.Room import Room
from Views.Menu import MenuView
import threading

class RoomController:
    def __init__(self):
        self.rooms = {}
        self.lock = threading.Lock()
        
    def create_room(self,room_name):
        with self.lock:
            if room_name not in self.rooms:
                self.rooms[room_name] = Room(room_name)  # Create a new room
                return True
        return False
    
    def add_user_to_room(self,client_socket,user,room_name):
        with self.lock:
            if room_name in self.rooms:
                self.rooms[room_name].users.append(user)  # Add user to the room
                return True
            else:
                # If room doesn't exist, send an error and close the connection
                client_socket.send("Invalid room choice.\n".encode())
                client_socket.close()
                return False
    
    def remove_user_from_room(self, client_socket, room_name):
        if room_name in self.rooms:
            with self.lock:
                self.rooms[room_name].remove_user_by_socket(client_socket)

    
    def broadcast_to_room(self, message, sender_socket, room_name):
        with self.lock:
            if room_name in self.rooms:
                self.rooms[room_name].broadcast(message, sender_socket)
                        
    def room_status(self):
        with self.lock:
            return {room_name: room for room_name, room in self.rooms.items()}
 
