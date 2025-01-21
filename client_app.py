from Models.Client import Client

def main():
    """Hlavná funkcia na spustenie klienta."""
    client_instance = Client()  
    client_instance.run()
    
if __name__ == "__main__":
    main()
