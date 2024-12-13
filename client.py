'''
Pham Minh Thien
Assignment 4
Prof. Palak Mejpara
'''

#Import functionalities
import socket
import threading
import time

#Import GUI functions
import tkinter as tk

#Initializing detail
HOST = '127.0.0.1' #localhost
PORT = 11111 #port

def client_Side(name):
    #coonectiong to Server
    client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_Socket.connect((HOST, PORT))

    #Clock Sync Request
    def sync_Clock():
        client_Socket.send("SYNC".encode())

    #Sending messages
    def sender():
        message = message_Entry.get()
        message_Entry.delete(0, tk.END)

        #formatting the message Name and Time
        time_Stamp = time.strftime("%H:%M:%S", time.localtime())
        formatted_Message = f"{name} ({time_Stamp}): {message}"

        #Insert the messages
        message_Display.insert(tk.END, formatted_Message + "\n")

        client_Socket.send(formatted_Message.encode())

    #Receiving messages
    def receiver():
        while True:
            try:
                message =  client_Socket.recv(1024).decode()
                if "SYNC|" in message:
                    _, server_time = message.split("|")
                    sync_time.config(text=f"Server Time: {server_time}")
                else:
                    #Insert the messages
                    message_Display.insert(tk.END, message + "\n")
            except:
                print("ERROR: Client Receiver")
                client_Socket.close()
                break

    #Thread for receiving messages
    receiver_Thread = threading.Thread(target=receiver)
    receiver_Thread.start()
    
    #GUI Elements
    root = tk.Tk()
    root.title(f"Chat Box of: {name}")

    #Message Display
    message_Display = tk.Text(root, height=20, width=50,state=tk.NORMAL)
    message_Display.pack()

    #Message Entry
    message_Entry = tk.Entry(root, font=("Helvetica", 16),state=tk.NORMAL)
    message_Entry.pack()

    #send Button
    send_Button = tk.Button(root, text="Send", font=("Helvetica", 16), command=sender)
    send_Button.pack()

    #Time Label
    time_Label = tk.Label(root, text="Local Time: ", font=("Helvetica", 16))
    time_Label.pack()
    sync_time = tk.Label(root, text="Sync Time", font=("Helvetica", 16))
    sync_time.pack()

    #Update Local Clock
    def update_Clock():
        time_Label.config(text=f"Local Time: {time.strftime('%H:%M:%S', time.localtime())}")
        root.after(1000, update_Clock)

    #Clock Drift
    def clock_Drift():
        sync_Clock()
        root.after(1000, clock_Drift) #Request Sync every 1 seconds
    
    #Start Clock Sync process
    update_Clock()
    clock_Drift()

    #Run GUI
    root.mainloop()




    

