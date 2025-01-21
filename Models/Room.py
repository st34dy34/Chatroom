class Room:
    def __init__(self, name):
        self.name = name
        self.users = []
        
    def remove_user_by_socket(self, client_socket):
        """Remove a user by their socket."""
        self.users = [user for user in self.users if user.client_socket != client_socket]
    
    def get_username_from_socket(self, sender_socket):
        """Get username associated with a socket."""
        for user in self.users:
            if user.client_socket == sender_socket:
                return user.username
        return None

    def broadcast(self, message, sender_socket):
        """Broadcast a message to all users in the room except the sender."""
        for user in self.users:
            if user.client_socket != sender_socket:
                try:
                    # If message is bytes, decode it
                    if isinstance(message, bytes):
                        message = message.decode()
                    user.client_socket.send(message.encode())
                except Exception as e:
                    print(f"Error sending message to {user.username}: {e}")
                    try:
                        user.client_socket.close()
                    except:
                        pass
                    self.users.remove(user)
    
    
        