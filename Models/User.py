class User:
    instances = []
    def __init__(self,client_socket,username,password):
        self.client_socket = client_socket
        self.username = username
        self.password = password
        self.instances.append(self)
        
        
    