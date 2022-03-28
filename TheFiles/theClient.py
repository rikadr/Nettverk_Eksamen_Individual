import socket
import threading
import bots
import argparse
import random
import sys

# The help documentation
# DESCRIPTION
# parser = argparse.ArgumentParser(description="This chat client connects to a chat server and "
#                                             "lets a bot of your choosing reply to messages in the chat. It takes"
#                                             "three command line parameters: IP, PORT and BOT.")
# parser.add_argument('IP', type=str, help="The IP address you want to connect to.")  # IP parameter
# parser.add_argument('PORT', type=str, help="The PORT you want to connect to.")      # PORT parameter
# parser.add_argument('BOT', type=str, help="The BOT you want to run.")               # BOT parameter
# args = parser.parse_args()

#####################################################################################
# Start: Setup

# defining encoding standard
utf8 = "utf-8"

if input("Setup mode: (0) Normal, (1) Auto") == "1":
    print("Auto setup")
    IP = "127.0.0.1"
    PORT = 7975
else:
    print("Manual Setup")
    # Getting command line parameters
    IP = input("What IP do you want to connect to? > ")
    PORT = input("At what port? > ")
    print(f"{IP}:{PORT} confirmed\n")

# creating client socket
c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# tries to connect, exits if unable to connect
try:
    c_socket.connect((IP, PORT))
    print("Connection successful!")
except:
    sys.exit("Unable to connect")


# End: Setup
#####################################################################################
# Start: Bot choice

# getting the list of all available bots from the bots.py file
bot_username_list = bots.run_bot(None, None, True)
client_is_bot = None    # currently unknown

while True:  # Loop to request bot choice
    bot_list_output = "Available bots: 0=[Manual input] "    # String to add all bot names to
    for idx, item in enumerate(bot_username_list):
        bot_list_output += f"{idx + 1}={item}  "    # adds each bot name to string

    while True:
        try:
            print(bot_list_output)
            bot_ID = int(input("Choose bot number > "))  # asks for bot name input
            break
        except:
            print("Not valid input. Only numbers please. Try again.\n")

    if len(bot_username_list) > bot_ID - 1 >= 0:  # checks if input is within range of bots
        print(f"You selected bot {bot_ID}: {bot_username_list[bot_ID - 1]}")
        client_is_bot = True
        break  # stops loop after a bot is chosen
    elif bot_ID == 0:
        client_is_bot = False  # If input is 0 client is not set as a bot
        break  # stops loop when manual input is chosen

    # Prints if user input is not valid
    print(f"{str(bot_ID)} is not an available choice. Please try again.\n")

# End: Bot choice
#####################################################################################
# Start: Sending/Receiving


def receive_from_server(client_username):
    # print("Receiving now <<<")
    while True:
        try:
            # print("Going to receive new message")
            message = c_socket.recv(1024).decode(utf8)
            # print(f"I GOT *{message}*")

            if message == "USERNAMEREQUEST":  # If received message is a username request
                # print("SENDING USERNAME")
                send_to_server(client_username)
            else:  # If received message is a normal message
                print(message)
                # replies to message if client is a bot and sender is not a bot
                # print("I just printed the message above. Now going to check if a should reply")
                if client_is_bot and check_to_reply(message):
                    # print(f"I WILL REPLY TO THIS: *{message}*")
                    bot_reply_message = bots.run_bot(message, bot_ID, False)    # prepares reply string
                    # print(f"I WILL SEND THIS^{bot_reply_message}^")
                    send_to_server(bot_reply_message)   # sends message to server
                    print(f"You: {bot_reply_message}")


        except:
            print("An error occured! You disconnected from the server")
            c_socket.close()
            break


def type_message():
    while True:
        message = input("")
        send_to_server(message)


def send_to_server(message):
    # print(f"Sending {message} now >>>")
    c_socket.send(message.encode(utf8))


# End: Sending/Receiving
#####################################################################################


def check_to_reply(message):
    # print(f"Gonna fetch list of bot usernames")
    try:
        # print(f"in tryyyyy with ^{message}^")
        # print(f"This is the bot username list: {bot_username_list}")
        for name in bot_username_list:
            if name in message:
                # print(f"Bot should not reply. {name} is a bot")
                return False  # False means bot should not reply

        # print(f"Bot SHOULD reply. NOT bot")
        return True  # True means bot should reply

    except:
        print("Failed to check for names")
        return False


#####################################################################################
# Start: Program ...


# Defining username
if client_is_bot:
    username = bot_username_list[bot_ID - 1]    # gets username of chosen bot from list
else:
    username = input("Type your username: ")    # asks input for username if manual input is chosen

# receiving messages with following thread
# print(f"Starting receive thread for *{username}*")
receive_from_server_thread = threading.Thread(target=receive_from_server, args=(username,))
receive_from_server_thread.start()

# Taking input for messages with following thread if client is not set at a bot
if not client_is_bot:
    type_message_thread = threading.Thread(target=type_message)
    type_message_thread.start()

# print("ALL THROUGH")
# run_bot([random.choice(action_list), random.choice(action_list), random.choice(action_list)])



