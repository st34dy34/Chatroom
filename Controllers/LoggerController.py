from Models.Logger import Logger
from Views.Menu import MenuView


class LoggerController:
    @staticmethod
    def handle(context, arg):
        if arg == 1:
            # Task 1: Get users in a specific room
            print(MenuView.show_room_list(context.room_controller.room_status()))
            room = input("\nWhat room do you want to search user activity in? ")
            return Logger.get_users_and_count_in_room(room)

        elif arg == 2:
            # Task 2: Count distinct users in a specific room
            print(MenuView.show_room_list(context.room_controller.room_status()))
            room = input("\nWhat room do you want to search number of total users in? ")
            return Logger.get_users_and_count_in_room(room)

        elif arg == 3:
            # Task 3: Find rooms where a specific user sent messages
            user = input("\nWhat user do you want to spy on? ")
            return Logger.get_activity(username=user)

        elif arg == 4:
            # Task 4: Count messages sent by each user
            return Logger.get_activity()

        elif arg == 5:
            # Task 5: Count total messages in each room
            return Logger.get_activity(room_name="all")  # Use "all" to indicate all rooms

        else:
            return "Invalid option. Please choose a valid task (1-5)."