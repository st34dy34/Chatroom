from Models.Server import Server

def main():
    """Hlavná funkcia na spustenie servera."""
    server_instance = Server()  
    server_instance.run()
    
if __name__ == "__main__":
    main()
