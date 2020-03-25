import socket
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
name = input()
client.send(bytes("This is from " + name,'UTF-8'))
while True:
  in_data =  client.recv(1024)
  print("From Server :" ,in_data.decode())
  out_data = input()
  client.send(bytes(out_data,'UTF-8'))
  if out_data=='bye':
    break
client.close()