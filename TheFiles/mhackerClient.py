#Coded by Yashraj Singh Chouhan
import socket, threading
nickname = input("Choose your nickname: ")
utf8 = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
# print("trying to connect")
client.connect(('127.0.0.1', 7976))                             #connecting client to server
print("Connected!")


def receive():
    while True:                                                 #making valid connection
        # print("Receiving now")
        try:
            message = client.recv(1024).decode(utf8)
            # print(f"Got the message ''{message}'' now")
            if message == 'USERNAMEREQUEST':
                print("SENDING USERNAME")
                client.send(nickname.encode(utf8))
                #client.close()
                #print("Closed connection")
            else:
                print(message)
        except:                                                 #case on wrong ip/port details
            print("An error occured! You disconnected from the server")
            client.close()
            break


def write():
    while True:                                                 #message layout
        message = input('')
        client.send(message.encode(utf8))


receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages
write_thread.start()
