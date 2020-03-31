import socket
import threading
import sys
import datetime
import time

HOST = 'localhost'
PORT = int(input("Masukkan port yang akan digunakan: "))

score = [0, 0]
totalQuestions = int(input("Jumlah pertanyaan yang ingin dijawab: "))
t = [0, 0]
filename = input("Masukkan nama file quiz : ")
f = open(filename, 'r')

flag = [False] *totalQuestions

def askQuestion(connlist, playerNo, ques, ans, questionNo):
    connlist[playerNo].send(ques.encode())
    time.sleep(0.1)

    data = connlist[playerNo].recv(PORT).decode()
    t[playerNo] = datetime.datetime.now()                    #receive answer
    if ans.rstrip() == data :
        if flag[questionNo] == False :
            score[playerNo]+=10
            flag[questionNo] = True
            connlist[playerNo].send(("Jawaban Benar!").encode())
            time.sleep(0.1)
        else :
            connlist[playerNo].send(("Kurang beruntung :(").encode())
            time.sleep(0.1)
    else :
        connlist[playerNo].send(("Jawaban Salah!").encode())
        time.sleep(0.1)

def sendallScore(connlist):
    global score
    for i, conn in enumerate(connlist):
        conn.send("S".encode())
        time.sleep(0.1)
        ket = "Player "+str(i+1)+", skor kamu adalah: "+str(score[i])
        conn.send(ket.encode())
        time.sleep(0.1)

def scoreFinal() :
    if score[0]>score[1]:
        print ("Player 1 menang, dengan skor: ", score)
        conn1.send("MENANG".encode())
        time.sleep(0.1)
        conn2.send("KALAH".encode())
        time.sleep(0.1)
    elif score[0]<score[1]:
        print ("Player 2 menang, dengan skor: ", score)
        conn2.send("MENANG".encode())
        time.sleep(0.1)
        conn1.send("KALAH".encode())
        time.sleep(0.1)
    else:
        print ("Skor seimbang, dengan skor: ", score)
        conn1.send("TIE".encode())
        time.sleep(0.1)
        conn2.send("TIE".encode())
        time.sleep(0.1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(2)
print ("Server bound to ", HOST, ":", PORT, "\nConnect both players before continuing...")
(conn1, addr) = s.accept()
print ("Connected to Player 1 at ", addr)
(conn2, addr) = s.accept()
print ("Connected to Player 2 at ", addr)

connlist = [conn1, conn2]

time.sleep(0.1)
conn1.send("I".encode())
conn1.send("Player 1".encode())

time.sleep(0.1)
conn2.send("I".encode())
conn2.send("You are Player 2".encode())

for questionNo in range(totalQuestions):
    conn1.send("Q".encode())
    time.sleep(0.1)
    conn2.send("Q".encode())
    time.sleep(0.1)
    
    Soal = "\nPertanyaan Nomor " + str(questionNo+1)
    conn1.send(Soal.encode())
    time.sleep(0.1)
    conn2.send(Soal.encode())
    time.sleep(0.1)

    ques = f.readline()+f.readline()+f.readline()+f.readline()+f.readline()
    print (ques)
    ans = f.readline()
    
    playerThread1 = threading.Thread(target = askQuestion, name = "Thread1", args = (connlist, 0, ques, ans, questionNo))
    playerThread2 = threading.Thread(target = askQuestion, name = "Thread2", args = (connlist, 1, ques, ans, questionNo))
    playerThread1.start()
    playerThread2.start()
    playerThread1.join()
    playerThread2.join()

    if questionNo<totalQuestions:
        sendallScore(connlist)

time.sleep(0.1)
conn1.send("F".encode())
time.sleep(0.1)
conn2.send("F".encode())
scoreFinal()
s.close()
