class AdminPanel:
    @staticmethod
    def Popup_message():
        return (
        "=========================\n"
        "Admin Panel Initialized!\n"
        "Use HELP for guide\n"
        "=========================\n"
        )
    def Help_message():
        return(
                "=========================\n"
                "Available commands:\n"
                "LOGS <option> - Perform a logging task (1-5)\n"
                "HELP - Show this help message\n"
                "\nOptions for LOGS:\n"
                "1 - Get users in a specific room\n"
                "2 - Count distinct users in a specific room\n"
                "3 - Find rooms where a specific user sent messages\n"
                "4 - Count messages sent by each user\n"
                "5 - Count total messages in each room\n"
                "=========================\n"
        )