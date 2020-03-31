import socket
import sys

def intros(s):
    res = s.recv(PORT).decode()
    print(res)

def question(s):
    quesNum = s.recv(PORT).decode()
    print(quesNum)
    ques = s.recv(PORT).decode()
    print(ques)
    ans = input("Jawaban: ")
    while ans not in ['A', 'B', 'C', 'D']:
        print ("Jawaban tidak sesuai dengan pilihan yang tersedia ! Try Again")
        ans = input("Jawaban: ")
    s.send(ans.encode())
    response = s.recv(PORT).decode()
    print(response)

def scores(s):
    res = s.recv(PORT).decode()
    print(res)

def final(s):
    res = s.recv(PORT).decode()
    print(res)

HOST = 'localhost'   
PORT = int(input("Input port yang akan digunakan : "))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    choice = s.recv(PORT).decode()
    if choice == "I": 
        intros(s)
    elif choice == "Q":
        question(s)
    elif choice == "S":
        scores(s)
    elif choice == "F":
        final(s)
        break
s.close()