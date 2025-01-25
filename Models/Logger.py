import sqlite3
from config import LOG_PATH


class Logger:
    @staticmethod
    def create_tables():
        with sqlite3.connect(LOG_PATH) as conn:
                cur = conn.cursor()

                # Create Users table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(100) NOT NULL UNIQUE
                );
                """)

                # Create Messages table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS Messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_name VARCHAR(100) NOT NULL,
                    user_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                );
                """)

    @staticmethod
    def log(room_name, username, message):
        """Logs a message to the database."""
        try:
            Logger.create_tables() 
            with sqlite3.connect(LOG_PATH) as conn:
                cur = conn.cursor()

                # Insert user (if already exist, do nothing)
                cur.execute("""
                INSERT OR IGNORE INTO Users (username)
                VALUES (?);
                """, (username,))

                # Get the user_id
                cur.execute("""
                SELECT id FROM Users WHERE username = ?;
                """, (username,))
                user_id = cur.fetchone()[0]

                # Insert the message
                cur.execute("""
                INSERT INTO Messages (room_name, user_id, message)
                VALUES (?, ?, ?);
                """, (room_name, user_id, message))
                conn.commit()
                print(f"        Message logged: Room='{room_name}', User='{username}', Message='{message}'.")
        except sqlite3.Error as e:
            print(f"Database error in log method: {e}")
        except Exception as e:
            print(f"Unexpected error in log method: {e}")

            
    @staticmethod       
    def get_logs(room):
        conn = None
        try:
            conn = sqlite3.connect(LOG_PATH)
            cur = conn.cursor()
            cur.execute("""
            SELECT Users.username, Messages.message
            FROM Messages
            JOIN Users ON Messages.user_id = Users.id
            WHERE Messages.room_name = ?;
            """)
            users = cur.fetchall()
            return users
        finally:
            conn.close()
            
            
    # ADMIN SECTION
    @staticmethod
    def get_users_and_count_in_room(room_name):
        """Retrieves users and counts distinct users who sent messages to a specific room."""
        try:
            with sqlite3.connect(LOG_PATH) as conn:
                cur = conn.cursor()

                # Get distinct users in the room
                cur.execute("""
                SELECT DISTINCT Users.username
                FROM Messages
                JOIN Users ON Messages.user_id = Users.id
                WHERE Messages.room_name = ?;
                """, (room_name,))

                users = cur.fetchall()
                users_list = [user[0] for user in users]  # Extract usernames from tuples

                # Count distinct users in the room
                cur.execute("""
                SELECT COUNT(DISTINCT Users.username) AS user_count
                FROM Messages
                JOIN Users ON Messages.user_id = Users.id
                WHERE Messages.room_name = ?;
                """, (room_name,))

                user_count = cur.fetchone()[0]  # Fetch the count

                # Format the results
                if not users_list:
                    return f"No users found in room '{room_name}'."
                else:
                    user_list_formatted = "\n".join(users_list)
                    return (
                        f"Users who have sent messages in {room_name}:\n"
                        f"=====\n"
                        f"{user_list_formatted}\n"
                        f"=====\n"
                        f"Total distinct users: {user_count}"
                    )

        except sqlite3.Error as e:
            return f"Database error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"
        
    @staticmethod
    def get_activity(room_name=None, username=None):
        """
        Retrieves activity based on the provided parameters:
        - If `room_name` is provided, retrieves the total number of messages in that room.
        - If `username` is provided, retrieves the rooms where the user sent messages.
        - If neither is provided, retrieves the message count for each user.
        """
        try:
            with sqlite3.connect(LOG_PATH) as conn:
                cur = conn.cursor()

                if room_name:
                    if room_name == "all":
                        # Count total messages in each room
                        cur.execute("""
                        SELECT room_name, COUNT(id) AS message_count
                        FROM Messages
                        GROUP BY room_name;
                        """)

                        results = cur.fetchall()
                        if not results:
                            return "No messages found in any room."
                        else:
                            room_counts_formatted = "\n".join(
                                f"{room}: {count} messages" for room, count in results
                            )
                            return f"Total messages per room:\n=====\n{room_counts_formatted}\n====="
                    else:
                        # Count total messages in a specific room
                        cur.execute("""
                        SELECT COUNT(id) AS message_count
                        FROM Messages
                        WHERE room_name = ?;
                        """, (room_name,))

                        result = cur.fetchone()
                        if not result or result[0] == 0:
                            return f"No messages found in room '{room_name}'."
                        else:
                            return f"Total messages in {room_name}:\n=====\n- {result[0]} messages\n====="

                elif username:
                    # Task 3: Find rooms where a specific user sent messages
                    cur.execute("""
                    SELECT DISTINCT Messages.room_name
                    FROM Messages
                    JOIN Users ON Messages.user_id = Users.id
                    WHERE Users.username = ?;
                    """, (username,))

                    rooms = cur.fetchall()
                    rooms_list = [room[0] for room in rooms]  # Extract room names from tuples
                    if not rooms_list:
                        return f"User '{username}' has no known messages!"
                    else:
                        rooms_list_formatted = "\n".join(rooms_list)
                        return f"{username} has sent messages in:\n=====\n{rooms_list_formatted}\n====="

                else:
                    # Task 4: Count messages sent by each user
                    cur.execute("""
                    SELECT Users.username, COUNT(Messages.id) AS message_count
                    FROM Messages
                    JOIN Users ON Messages.user_id = Users.id
                    GROUP BY Users.username;
                    """)

                    results = cur.fetchall()
                    if not results:
                        return "No messages found for any user."
                    else:
                        message_counts_formatted = "\n".join(
                            f"{user}: {count} messages" for user, count in results
                        )
                        return f"Message counts per user:\n=====\n{message_counts_formatted}\n====="

        except sqlite3.Error as e:
            return f"Database error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"
                
    