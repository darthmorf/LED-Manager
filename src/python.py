import socket
import random
import time

def __main__():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(('localhost', 2626))

	pixelcount = 64 * 32

	randbg(sock, pixelcount)

	sock.close()


def randcolor(sock, pixelcount):
	while True:
		string = ""
		for i in range(pixelcount):
			string += str(random.randint(0,255)) + "," + str(random.randint(0,255)) + "," + str(random.randint(0,255)) + ","

		string = string[:-1]

		sock.send(string)

def randbg(sock, pixelcount):
	while True:
		string = str(random.randint(0,255)) + "," + str(random.randint(0,255)) + "," + str(random.randint(0,255)) + ","
		string = string * pixelcount
		string = string[:-1]
		time.sleep(0.1)
		sock.send(string)


__main__()		