import json
import curses
from Structures.AVL import AVL
from Structures.AVL import NodeAVL
from Structures.ListBlock import ListBlockChain
from Structures.ListBlock import BlockNode
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from curses import KEY_LEFT
import socket
import select
import sys
list = ListBlockChain()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost", 8000))
class dataNode:
    def __init__(self,name,key,left,right):
        self.key=key
        self.name=name
        self.left=left
        self.right=right
class Menu:
    def __init__(self):
        self.root=None
        self.data = None
        self.cont=0
    def Menu(self):
        avl = AVL()
        print("Ingrese opcion: ")
        print("1. Insert Block")
        print("2. Select Block")
        print("3. Reports")
        op = input()
        if op=="1":
            print("Insert Ruta")
            ruta = input()

            f = open(ruta, 'r', encoding='utf-8')
            if f.mode == "r":
                contents = f.read()
                cont = contents.split("\n")
            clase=cont[0]
            data=cont[1]
            self.data=data.replace("data,","")
            self.insertBlock(self.data,clase.split(",")[1])
            self.data=""
        elif op=="2":
            node = list.returnFirt()
            stdscr = curses.initscr()
            win = curses.newwin(42, 120, 0, 0)
            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
            win.keypad(True)
            key=None
            while (key != ord('q')):
                win.addstr(2, 30, "Move Block")
                key = win.getch()
                stdscr.clear()
                if key == KEY_LEFT:
                    win.clear()
                    win.border(0)
                    win.refresh()
                    if node.prev!=None:
                        node = node.prev
                    win.addstr(10, 40,str(node.data))
                elif key == KEY_RIGHT:
                    win.clear()
                    win.border(0)
                    win.refresh()
                    win.addstr(10, 40,str(node.data))
                    print(node.data)
                    if node.next != None:
                        node = node.next
                elif key==KEY_UP:
                    break;
            win.clear()
            curses.endwin()
            print("hola")
        elif op=="3":
            print("1. AVL")
            print("2. Recorridos")
            op = input()
            if op=="1":
                list.showBlock()
                print("Insert key Block")
                key = input()
                nodeAVL = list.returnBlock(key)

                self.castJson(nodeAVL.datos)
            if op=="2":
                print("1. INORDEN")
                print("2. PREORDEN")
                print("3. POSTORDEN")
                op = input()
                if op=="1":
                    avl.recoIn(self.root)
                    avl.grafReco("INORDEN")
                elif op=="2":
                    avl.recoPre(self.root)
                    avl.grafReco("PREORDEN")
                elif op=="3":
                    avl.recoPre(self.root)
                    avl.grafReco("POSTORDEN")
    def insertBlock(self,data,classs):
        new = BlockNode()
        dataJson =json.dumps(json.loads(data),indent=4)
        new.claSS = classs
        new.index = self.cont
        if self.cont==0:
            new.prevHash = "0000"
        elif self.cont>0:
            new.prevHash=None
        new.hash = self.sha256(str(new.index) + str(new.time) + str(new.claSS) + str(new.data) + str(new.prevHash))
        new.data = '{\n\t"INDEX"' + ': ' + str(new.index) + ',\n"TIMESTAP"' + ': ' + '"' + str(
            new.time) + '"' + ',\n"CLASS"' + ': ' + '"' + str(
            new.claSS) + '",' + '\n"DATA: "' + dataJson + ',' + '\n"PREVIUSHASH"' + ': ' + '"' + new.prevHash + '"' + ',\n"HASH"' + ': ' + '"' + new.hash + '"' + '\n}'
        server.sendall(new.data.encode('utf-8'))
        sys.stdout.write("<You>")
        sys.stdout.flush()
        list.addBlock(new)
        self.cont += 1
    def sha256(self,val):
        h=hashlib.sha256(val.encode()).hexdigest()
        return h
    def castJson(self,avleData):
        dict_obj = json.loads(str(avleData))
        value=None
        left=None
        right=None
        value = dict_obj["value"].split("-")
        left = dict_obj["left"]
        right = dict_obj["right"]
        data=dataNode(value[0],value[1],left,right)
        self.craeteAVL(data.name,data.key,data.left,data.right)
    def craeteAVL(self,name,key,left,right):
        avl = AVL()
        root = None
        root = NodeAVL(name,key)
        root.right = NodeAVL(right["value"].split("-")[0],right["value"].split("-")[1])
        root.right = self.retornAVLNode(root.right," "," ",right["left"],right["right"])
        root.left = NodeAVL(left["value"].split("-")[0],left["value"].split("-")[1])
        root.left = self.retornAVLNode(root.left, " ", " ", left["left"], left["right"])
        self.root=root
        avl.graphAVL(root)
        avl.graficarAvl()
    def retornAVLNode(self,root,key,name,left,right):
        if left!=None:
            valLeft = left["value"].split("-")
        if right!=None:
            valRigt = right["value"].split("-")
        if root is None:
            return NodeAVL(key,name)
        if root.right is None and right != None:
            root.right = self.retornAVLNode(root.right,valRigt[0],valRigt[1],left,right)
        if root.left is None and left !=None:
            root.left = self.retornAVLNode(root.left, valLeft[0], valLeft[1], left, right)
        if right !=None:
            root.right = self.retornAVLNode(root.right, valRigt[0], valRigt[1], right["left"], right["right"])
        if left!=None:
            root.left = self.retornAVLNode(root.left, valLeft[0], valLeft[1], left["left"], left["right"])
        return root
menu = Menu()
while True:
    read_sockets = select.select([server], [], [], 1)[0]
    import msvcrt
    if msvcrt.kbhit(): read_sockets.append(sys.stdin)
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print(message.decode('utf-8'))
        else:
            print("")
    menu.Menu()
server.close()
