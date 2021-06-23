import socket
 
HOST = '10.3.22.188'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
 
while True:
    user_input = input('msg to send:').encode()
    s.sendall(user_input)
    data = s.recv(1024)
    print ('Received', repr(data))
    # if data == b'c' or data == b'C':break
 
s.close()
