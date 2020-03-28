import socket, threading, datetime
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    def run(self):
        print ("Connection from : ", clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            print(data)
            msg = input()
            if msg=='bye':
              break
            elif(msg.lower() == 'start'):
                questions = open("questions.csv", "r")
                ques = questions.readlines()
                for q in ques:
                    data = q.split(",")
                    msg = data[1] + "\na. " + data[2] + "\nb. " + data[3] + "\nc. " + data[4] + "\nd. " + data[5] 
                    startTime = datetime.datetime.now()
                    self.csocket.send(bytes(msg,'UTF-8'))
                    data = self.csocket.recv(2048)
                    print(str(data))
        print ("Client at ", clientAddress , " disconnected...")
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
server.listen(4)
print("Server started")
print("Waiting for client request..")
while True:
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()