import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 2626))
while True:
	sock.send(str(input(">")))
sock.close()
