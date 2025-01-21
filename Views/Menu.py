class MenuView:
    """View for displaying menu and status information"""
    
    @staticmethod
    def startup_message():
        """Display initial welcome message"""
        return (
            "Welcome to Chatroom!\n"
            "=========================\n"
        )
    
    @staticmethod
    def username_message():
        """Display message for username input"""
        return (
            "Choose your username!"
        )
        
    @staticmethod
    def password_message():
        """Display message for password input"""
        return (
            "Choose your Password!"
        )
    @staticmethod
    def join_server_message(room_name):
        return (
            f"Joined {room_name}\n"
            "You can start chatting!\n"
            "type LEAVE to leave the chatroom\n"
            "=========================\n"
        )
    @staticmethod
    def show_room_list(rooms):
        """Display list of available rooms"""
        if not rooms:
            return "No rooms available."
            
        room_list = "Available Rooms:\n"
        room_list += "================\n"
        for room_name, room in rooms.items():  # Access the Room object
            players = len(room.users)  # Now we can access the 'users' attribute of the Room object
            room_list += f"Room: {room_name} | Players: {players}\n"
        return room_list

