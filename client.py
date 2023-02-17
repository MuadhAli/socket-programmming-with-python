from socket import *
from threading import *
from tkinter import *

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

hostIp = "172.22.49.66"
portNumber = 7500

clientSocket.connect((hostIp, portNumber))

window = Tk()
window.title("Connected To: "+ hostIp+ ":"+str(portNumber))
window.geometry("500x500")
window.configure(background="black")

messagesFrame = Frame(window)
messagesFrame.pack(fill=BOTH, expand=True)
messagesFrame.grid_columnconfigure(0, weight=1)
messagesFrame.grid_rowconfigure(0, weight=1)

txtMessages = Text(messagesFrame, width=50, bg="black", fg="green")
txtMessages.pack(fill=BOTH, padx=10, pady=10, expand=True)

scrollbar = Scrollbar(messagesFrame)
scrollbar.pack(side=RIGHT, fill=Y)
txtMessages.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=txtMessages.yview)

messageFrame = Frame(window)
messageFrame.pack(fill=X, side=BOTTOM)

txtYourMessage = Entry(messageFrame, width=50)
txtYourMessage.insert(0,"Your message")
txtYourMessage.pack(side=LEFT, padx=10, pady=10, expand=True)

def sendMessage(event=None):
    clientMessage = txtYourMessage.get()
    txtMessages.insert(END, "\n" + "You: "+ clientMessage)
    clientSocket.send(clientMessage.encode("utf-8"))
    txtYourMessage.delete(0, END)

btnSendMessage = Button(messageFrame, text="Send", width=20, command=sendMessage)
btnSendMessage.pack(side=RIGHT, padx=10, pady=10)

txtYourMessage.bind("<Return>", sendMessage)

def recvMessage():
    while True:
        serverMessage = clientSocket.recv(1024).decode("utf-8")
        txtMessages.insert(END, "\n"+"Client: "+serverMessage)

recvThread = Thread(target=recvMessage)
recvThread.daemon = True
recvThread.start()

window.mainloop()
