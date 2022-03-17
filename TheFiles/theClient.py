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
    botList = "Available bots: "
    for idx, item in enumerate(bots):
        botList += f"{idx + 1}={item}  "
    print(botList)

    BOT = input("Choose bot number > ")  # asks for bot name input

    if len(bots) > int(BOT) - 1 >= 0:  # checks if input is within range of
        print(f"You selected bot {BOT}: {bots[int(BOT) - 1]}")
        break  # stops loop after a match is found

    print(f"{BOT} is not a registered bot. Please try again.\n")


