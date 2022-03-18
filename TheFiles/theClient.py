import socket
import threading
import argparse

# The help documentation
# DESCRIPTION
# parser = argparse.ArgumentParser(description="This chat client connects to a chat server and "
#                                             "lets a bot of your choosing reply to messages in the chat. It takes"
#                                             "three command line parameters: IP, PORT and BOT.")
# parser.add_argument('IP', type=str, help="The IP address you want to connect to.")  # IP parameter
# parser.add_argument('PORT', type=str, help="The PORT you want to connect to.")      # PORT parameter
# parser.add_argument('BOT', type=str, help="The BOT you want to run.")               # BOT parameter
# args = parser.parse_args()

# Getting command line parameters
IP = input("What IP do you want to connect to? > ")
PORT = input("At what port? > ")
print(f"{IP}:{PORT} confirmed\n")

bots = ["Peder", "Fredrik", "Rikard", "Maren"]  # List of available bots to choose from

while True:  # Loop to request bot choice
    botList = "Available bots: "    # String to add all bot names to
    for idx, item in enumerate(bots):
        botList += f"{idx + 1}={item}  "    # adds each bot name to string
    print(botList)

    bot_number = input("Choose bot number > ")  # asks for bot name input
    if len(bots) > int(bot_number) - 1 >= 0:  # checks if input is within range of bots
        print(f"You selected bot {bot_number}: {bots[int(bot_number) - 1]}")
        break  # stops loop after a bot is chosen

    # Prints if user input is not valid
    print(f"{bot_number} is not an available choice. Please try again.\n")


def recieve_from_server():
    print("Recieving now <<<")

    # if recieve "USERNAME?":
        # send_to_server(username)


def send_to_server(message):
    print(f"Sending {message} now >>>")


