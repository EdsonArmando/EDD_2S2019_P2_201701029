# Python program to implement client side of chat room.
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = str("localhost")
Port = int(8000)
server.connect((IP_address, Port))

while True:

	read_sockets = select.select([server], [], [], 1)[0]
	import msvcrt
	if msvcrt.kbhit(): read_sockets.append(sys.stdin)

	for socks in read_sockets:
		if socks == server:
			message = socks.recv(2048)
			print (message.decode('utf-8'))
		else:
			message = sys.stdin.readline()
			server.sendall('true'.encode('utf-8'))
			sys.stdout.write("<You>")
			sys.stdout.write(message)
			sys.stdout.flush()
server.close()
