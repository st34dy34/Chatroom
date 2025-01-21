from Models.Server import Server

def main():
    """Hlavná funkcia na spustenie servera."""
    server_instance = Server()  # Rename the variable for consistency
    server_instance.run()
    
if __name__ == "__main__":
    main()
