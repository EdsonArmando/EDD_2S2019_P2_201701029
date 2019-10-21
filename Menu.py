import json
import curses
import hashlib
from Structures.AVL import AVL
from Structures.AVL import NodeAVL
from Structures.ListBlock import ListBlockChain
from Structures.ListBlock import BlockNode
from curses import KEY_LEFT, KEY_RIGHT, KEY_UP
import socket
import select
import sys
list = ListBlockChain()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost", 8080))
class dataNode:
    def __init__(self, name, key, left, right):
        self.key = key
        self.name = name
        self.left = left
        self.right = right
class Menu:
    def __init__(self):
        self.root = None
        self.data = None
        self.cont = 0
        self.alt=0
        self.prevHash=None
    def escuchar2(self):
        cont=0
        new=BlockNode()
        while True:
            read_sockets = select.select([server], [], [], 1)[0]
            if cont==1:
                if len(read_sockets)==1:
                    sock=read_sockets[0]
                    message = sock.recv(2560)
                    if message.decode('utf-8') != "false":
                        list.addBlock(new)
                        self.cont+=1
                        print("Add block succes")
                        break;
                    else:
                        print("failed")
                        break;
            import msvcrt
            if msvcrt.kbhit(): read_sockets.append(sys.stdin)
            for socks in read_sockets:
                if socks == server:
                    message = socks.recv(2560)
                    try:
                        dict_obj = json.loads(str(message.decode('utf-8')))
                        z = json.dumps(dict_obj["DATA"], indent=4)
                        h = (str(dict_obj["INDEX"]) + str(dict_obj["TIMESTAMP"]) + str(dict_obj["CLASS"]) + str(z) + str(
                            dict_obj["PREVIOUSHASH"]))
                        j = hashlib.sha256(h.encode()).hexdigest()
                        if str(dict_obj["HASH"]) == j:
                            new.index = str(self.cont)
                            new.claSS=str(dict_obj["CLASS"])
                            new.time=str(dict_obj["TIMESTAMP"])
                            new.datos=z
                            new.data=str(dict_obj["DATA"])
                            new.hash=str(dict_obj["HASH"])
                            new.prevHash=str(dict_obj["PREVIOUSHASH"])
                            server.sendall('true'.encode('utf-8'))
                            cont=1
                        else:
                            server.sendall('false'.encode('utf-8'))
                    except:
                        print(message.decode('utf-8'))
                else:
                    message = sys.stdin.readline()
                    server.sendall(message.encode('utf-8'))
                    sys.stdout.write("<You>")
                    sys.stdout.flush()
    def verificar(self,nodoGlobal):
        while True:
            read_sockets = select.select([server], [], [], 1)[0]
            if len(read_sockets)==0:
                break
            import msvcrt
            if msvcrt.kbhit(): read_sockets.append(sys.stdin)
            for socks in read_sockets:
                if socks == server:
                    message = socks.recv(2560)
                    if nodoGlobal != None:
                        if message.decode('utf-8') == "true":
                            list.addBlock(nodoGlobal)
                            nodoGlobal = None
                            print("Block add succes")
                        else:
                            print("Block us failed")
                    try:
                        dict_obj = json.loads(str(message.decode('utf-8')))
                        z = json.dumps(dict_obj["DATA"], indent=4)
                        h = (str(dict_obj["INDEX"]) + str(dict_obj["TIMESTAMP"]) + str(dict_obj["CLASS"]) + str(
                            z) + str(
                            dict_obj["PREVIOUSHASH"]))
                        j = hashlib.sha256(h.encode()).hexdigest()
                        if str(dict_obj["HASH"]) == j:
                            server.sendall('true'.encode('utf-8'))
                        else:
                            server.sendall('false'.encode('utf-8'))
                    except:
                        print(message.decode('utf-8'))
                else:
                    print("")
    def Menu(self):
        avl = AVL()
        nodoGlobal = None
        print("Ingrese opcion: ")
        print("1. Insert Block")
        print("2. Select Block")
        print("3. Reports")
        op = input()
        if op == "1":
            print("Insert Ruta")
            ruta = input()
            f = open(ruta, 'r', encoding='utf-8')
            if f.mode == "r":
                contents = f.read()
                cont = contents.split("\n")
            clase = cont[0]
            data = cont[1]
            self.data = data.replace("data,","")
            nodoGlobal=self.insertBlock(self.data, clase.split(",")[1])
            self.data = ""
            self.verificar(nodoGlobal)
            self.Menu()
        elif op == "4":
            self.escuchar2()
        elif op == "2":
            node = list.returnFirt()
            stdscr = curses.initscr()
            win = curses.newwin(40, 120, 1, 2)  # create a new curses window
            curses.noecho()
            curses.curs_set(0)
            win.keypad(True)
            key = None
            while (key != ord('q')):
                win.addstr(2, 30, "Move Block")
                key = win.getch()
                stdscr.clear()
                if key == KEY_LEFT:
                    win.clear()
                    win.border(0)
                    win.refresh()
                    if node.prev != None:
                        node = node.prev
                    cont = 0
                    y = 11
                    x = 10
                    win.addstr(5,10,"CLASS: "+str(node.claSS))
                    win.addstr(6, 10, "INDEX: " + str(node.index))
                    win.addstr(7, 10, "TIMESTAMP: " + str(node.time))
                    win.addstr(8, 10, "HASH: " + str(node.hash))
                    win.addstr(9, 10, "PREVIOUSHASH: " + str(node.prevHash))
                    win.addstr(10, 10, "DATA: ")
                    while cont < len(node.datos):
                        letra = node.datos[cont]
                        win.addstr(y, x, letra)
                        if x == 80:
                            y += 1
                            x = 10
                        cont += 1
                        x += 1
                elif key == KEY_RIGHT:
                    win.clear()
                    win.border(0)
                    win.refresh()
                    cont = 0
                    y = 11
                    x=10
                    win.addstr(5, 10, "CLASS: " + str(node.claSS))
                    win.addstr(6, 10, "INDEX: " + str(node.index))
                    win.addstr(7, 10, "TIMESTAMP: " + str(node.time))
                    win.addstr(8, 10, "HASH: " + str(node.hash))
                    win.addstr(9, 10, "PREVIOUSHASH: " + str(node.prevHash))
                    win.addstr(10, 10, "DATA: ")
                    while cont < len(node.datos):
                        letra = node.datos[cont]
                        win.addstr(y, x, letra)
                        if x == 80:
                            y += 1
                            x=10
                        cont += 1
                        x+=1
                    if node.next != None:
                        node = node.next
                elif key == KEY_UP:
                    break;
            win.clear()
            curses.endwin()
            self.Menu()
        elif op == "3":
            print("1. AVL")
            print("2. Recorridos")
            print("3. BlockChain")
            op = input()
            if op == "1":
                list.showBlock()
                print("Insert key Block")
                key = input()
                nodeAVL = list.returnBlock(key)

                self.graphAVL(nodeAVL.datos)
            elif op == "2":
                print("1. INORDEN")
                print("2. PREORDEN")
                print("3. POSTORDEN")
                op = input()
                if op == "1":
                    avl.recoIn(self.root)
                    avl.grafReco("INORDEN")
                elif op == "2":
                    avl.recoPre(self.root)
                    avl.grafReco("PREORDEN")
                elif op == "3":
                    avl.recoPost(self.root)
                    avl.grafReco("POSTORDEN")
            elif op=="3":
                list.GenerateImage()
        self.Menu()
    def insertBlock(self, data,classs):
        new = BlockNode()
        dataJson = json.dumps(json.loads(data), indent=4)
        new.datos = data
        new.claSS = classs
        new.index = self.cont
        if self.cont == 0:
            new.prevHash = "0000"
        elif self.cont > 0:
            new.prevHash = self.prevHash
        new.hash = self.sha256(str(new.index) + str(new.time) + str(new.claSS)+str(dataJson) + str(new.prevHash))
        new.data = '{\n"INDEX"' + ': ' + str(new.index) + ',\n"TIMESTAMP"' + ': ' + '"' + str(new.time) + '"' + ',\n"CLASS"' + ': ' + '"' + str(new.claSS) + '",' + '\n"DATA"' + ': '+ str(dataJson) + ',\n"PREVIOUSHASH"' + ': ' + '"' + str(new.prevHash) + '"' + ',\n"HASH"' + ': ' + '"' + str(new.hash) + '"' + '\n}'
        server.sendall(new.data.encode('utf-8'))
        sys.stdout.flush()
        self.cont += 1
        self.prevHash = new.hash
        return new
    def sha256(self, val):
        h = hashlib.sha256(val.encode()).hexdigest()
        return h
    def graphAVL(self, avleData):
        dict_obj = json.loads(str(avleData))
        value = dict_obj["value"].split("-")
        left = dict_obj["left"]
        right = dict_obj["right"]
        data = dataNode(value[0], value[1], left, right)
        self.generateaAVL(data.name, data.key, data.left, data.right)
    def generateaAVL(self, name, key, left, right):
        avl = AVL()
        root = NodeAVL(name, key)
        root.right = NodeAVL(right["value"].split("-")[0], right["value"].split("-")[1])
        root.right = self.nodeTree(root.right, " ", " ", right["left"], right["right"])
        self.alt=0
        root.left = NodeAVL(left["value"].split("-")[0], left["value"].split("-")[1])
        root.left = self.nodeTree(root.left, " ", " ", left["left"], left["right"])
        root.alt=self.alt+1
        self.root = root
        self.alt = 0
        avl.graphAVL(root)
        avl.graficarAvl()
    def nodeTree(self, root, key, name, left, right):
        if left != None:
            valLeft = left["value"].split("-")
        if right != None:
            valRigt = right["value"].split("-")
        else:
            try:
                root.alt=self.alt
            except:
                print("err")
        if root is None:
            return NodeAVL(key, name)
        if root.right is None and right != None:
            root.right = self.nodeTree(root.right, valRigt[0], valRigt[1], left, right)
        if root.left is None and left != None:
            root.left = self.nodeTree(root.left, valLeft[0], valLeft[1], left, right)
        if right != None:
            root.right = self.nodeTree(root.right, valRigt[0], valRigt[1], right["left"], right["right"])
        if left != None:
            self.alt += 1
            root.left = self.nodeTree(root.left, valLeft[0], valLeft[1], left["left"], left["right"])
        return root
menu = Menu()
menu.verificar(None)
menu.Menu()
server.close()