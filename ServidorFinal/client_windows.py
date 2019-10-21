# Python program to implement client side of chat room.
import socket
import select
import sys
import json
import hashlib
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = str("localhost")
Port = int(8080)
server.connect((IP_address, Port))

while True:
    read_sockets = select.select([server], [], [], 1)[0]
    import msvcrt
    if msvcrt.kbhit(): read_sockets.append(sys.stdin)
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2560)
            try:
                dict_obj = json.loads(str(message.decode('utf-8')))
                z=json.dumps(dict_obj["DATA"],indent=4)
                h=(str(dict_obj["INDEX"])+str(dict_obj["TIMESTAMP"])+str(dict_obj["CLASS"])+str(z)+str(dict_obj["PREVIOUSHASH"]))
                j= hashlib.sha256(h.encode()).hexdigest()
                print("--------DATA--------")
                print(str(dict_obj["DATA"]))
                print("--------DATA--------")
                print(str(dict_obj["INDEX"]))
                print(str(dict_obj["TIMESTAMP"]))
                print(str(dict_obj["CLASS"]))
                print(str(dict_obj["PREVIOUSHASH"]))
                print(str(dict_obj["HASH"]))
                print(z)
                print(j)
                if str(dict_obj["HASH"])==j:
                    server.sendall('true'.encode('utf-8'))
                    print("---true----")
                else:
                    server.sendall('false'.encode('utf-8'))
            except:

                print(message.decode('utf-8'))
        else:
            message = sys.stdin.readline()
            server.sendall(message.encode('utf-8'))
            sys.stdout.write("<You>")
            sys.stdout.flush()
server.close()