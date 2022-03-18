#Coded by Yashraj Singh Chouhan
import socket, threading
nickname = input("Choose your nickname: ")
utf8 = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect(('127.0.0.1', 7976))                             #connecting client to server

def receive():
    while True:                                                 #making valid connection
        try:
            message = client.recv(1024).decode(utf8)
            if message == 'USERNAME?':
                client.send(nickname.encode(utf8))
            else:
                print(message)
        except:                                                 #case on wrong ip/port details
            print("An error occured!")
            client.close()
            break
def write():
    while True:                                                 #message layout
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode(utf8))

receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages
write_thread.start()