import json
from Structures.AVL import AVL
from Structures.AVL import NodeAVL
from Structures.ListBlock import ListBlockChain
from Structures.ListBlock import BlockNode
list = ListBlockChain()
avl = AVL()
class dataNode:
    def __init__(self,name,key,left,right):
        self.key=key
        self.name=name
        self.left=left
        self.right=right
class Menu:
    def __init__(self):
        self.root=None
    def Menu(self):
        print("Ingrese opcion: ")
        print("1. Insert Block")
        print("2. Select Block")
        print("3. Reports")
        op = input()
        if op=="1":
            print("Insert Ruta")
            ruta = input()
            self.insertBlock(ruta,"Estructuras de Datos")
            self.Menu()
        elif op=="3":
            print("1. AVL")
            print("2. Recorridos")
            op = input()
            if op=="1":
                self.castJson()
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
                    avl.recoPost(self.root)
                    avl.grafReco("PREORDEN")
            list.GenerateImage()
            self.Menu()
    def insertBlock(self,data,classs):
        nodo = BlockNode()
        nodo.data = data
        nodo.claSS = classs
        list.addBlock(nodo)
        list.showBlock()

    def castJson(self):

        # json data string
        avlData = '{"value":"Armando-201701029", "left":{"value":"Kyara-2017010265", "left":{"value":"Mocica-2017010265", "left":null, "right":null}, "right":{"value":"Mike-201875498", "left":null, "right":null}}, ' \
                  '"right":{"value":"Aylin-2015478524", "left":{"value":"Lucy-2017010265", "left":null, "right":null}, ' \
                  '"right":{"value":"DulMa-2017010265", "left":{"value":"Karol-201524156", "left":null, "right":null}, "right":{"value":"Emiliana-2017010265", "left":{"value":"DJ-20170102785", "left":null, "right":null}, "right":null}}}}'
        # Decoding or converting JSON format in dictionary using loads()
        dict_obj = json.loads(avlData)
        print(dict_obj)
        value=None
        left=None
        right=None
        value = dict_obj["value"].split("-")
        left = dict_obj["left"]
        right = dict_obj["right"]
        data=dataNode(value[0],value[1],left,right)
        self.craeteAVL(data.name,data.key,data.left,data.right)
    def craeteAVL(self,name,key,left,right):

        root = None
        root = NodeAVL(name,key)
        root.right = NodeAVL(right["value"].split("-")[0],right["value"].split("-")[1])
        root.right = self.retornNode(root.right," "," ",right["left"],right["right"])
        root.left = NodeAVL(left["value"].split("-")[0],left["value"].split("-")[1])
        root.left = self.retornNode(root.left, " ", " ", left["left"], left["right"])
        self.root=root
        avl.graphAVL(root)
        avl.graficarAvl()
    def retornNode(self,root,key,name,left,right):
        if left!=None:
            valLeft = left["value"].split("-")
        if right!=None:
            valRigt = right["value"].split("-")
        if root is None:
            return NodeAVL(key,name)
        if root.right is None and right != None:
            root.right = self.retornNode(root.right,valRigt[0],valRigt[1],left,right)
        elif root.left is None and left !=None:
            root.left = self.retornNode(root.left, valLeft[0], valLeft[1], left, right)
        if right !=None:
            root.right = self.retornNode(root.right, valRigt[0], valRigt[1], right["left"], right["right"])
        if left!=None:
            root.left = self.retornNode(root.left, valLeft[0], valLeft[1], left["left"], left["right"])
        return root
menu = Menu()
menu.Menu()
