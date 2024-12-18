import socket

server_socket = socket.socket()
print("created a socket object")

port = 1234

server_socket.bind(('',port))
print("Scoket has been binded to port :: {}".format(port))

server_socket.listen(5)
print ("socket is listening")           

while True:
    c, addr = server_socket.accept()
    
    print("got connected form",addr)
    
    c.send('Thank you for connecting'.encode())
    for i in range(0,10):
        c.send("i".encode())
        
    c.close()
    
    # Breaking once connection closed
    break