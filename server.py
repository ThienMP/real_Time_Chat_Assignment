'''
Pham Minh Thien
Assignment 4
Prof. Palak Mejpara
'''

# Importing libraries
import socket
import threading
import time

#Initializing detail
HOST = '127.0.0.1' #localhost
PORT = 11111 #port
client_List = []

#Server starter
def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT)) #binding server to host and port
    server.listen() #start listening for clients connections
    print("server lisenning...")

    while True:
        client_Socket, client_Address = server.accept()
        print(f"Client Connected: {client_Address}")

        client_List.append(client_Socket)

        #Thread for each client
        client_Thread = threading.Thread(target=client_Handler, args=(client_Socket,))
        client_Thread.start()

#Client handler
def client_Handler(client_Socket):
    while True:
        try:
            #message from client
            message = client_Socket.recv(1024).decode()

            #Clock Syncronization
            if message == "SYNC":
                server_time = time.strftime("%H:%M:%S", time.localtime())
                client_Socket.send(f"SYNC|{server_time}".encode())

            #broatcoasting the messages to all clients
            else:
                broadcast(message, client_Socket)

        except:
            client_Socket.close()
            client_List.remove(client_Socket)
            break

#Broadcasting messages to all clients
def broadcast(message, sending_Socket=None):
    for client in client_List:
        if client != sending_Socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                client_List.remove(client)

