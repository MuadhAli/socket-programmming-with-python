from socket import *
from threading import *
from tkinter import *

clients = set()

def clientThread(clientSocket, clientAddress):
    while True:
        message = clientSocket.recv(1024).decode("utf-8")
        print(clientAddress[0] + ":" + str(clientAddress[1]) +" says: "+ message)
        for client in clients:
            if client is not clientSocket:
                client.send((clientAddress[0] + ":" + str(clientAddress[1]) +" says: "+ message).encode("utf-8"))

        if not message:
            clients.remove(clientSocket)
            print(clientAddress[0] + ":" + str(clientAddress[1]) +" disconnected")
            break

    clientSocket.close()

hostSocket = socket(AF_INET, SOCK_STREAM)
hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)

hostIp = "127.0.0.1"
portNumber = 7500
hostSocket.bind((hostIp, portNumber))
hostSocket.listen()
print ("Waiting for connection...")

window = Tk()
window.title("Server: Waiting for connection on " + hostIp + ":" + str(portNumber))
window.geometry("500x500")

txtMessages = Text(window, width=50)
txtMessages.pack(fill=BOTH, padx=10, pady=10, expand=True)

scrollbar = Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y)
txtMessages.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=txtMessages.yview)

def updateTitle():
    connectedClients = len(clients)
    window.title("Server: " + str(connectedClients) + " client(s) connected on " + hostIp + ":" + str(portNumber))
    window.after(1000, updateTitle)

updateTitle()

while True:
    clientSocket, clientAddress = hostSocket.accept()
    clients.add(clientSocket)
    print ("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
    txtMessages.insert(END, "Connection established with: " + clientAddress[0] + ":" + str(clientAddress[1]) + "\n")
    thread = Thread(target=clientThread, args=(clientSocket, clientAddress, ))
    thread.start()

window.mainloop()
