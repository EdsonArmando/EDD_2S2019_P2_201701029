import os
class NodeAVL:
    def __init__(self, key,name):
        self.key = key
        self.name = name
        self.left = None
        self.right = None
        self.alt = 1
class AVL:
    def __init__(self):
        self.nodes=""
        self.rela2=""
        self.rela=""
        self.nodes=""
        self.inicio = 'digraph grafica{\nrankdir=TB;\n label=\"Arbol AVL \"; \n node [shape = record, style=filled, fillcolor=seashell2];\n'
        self.recorrido = ' digraph{\nrankdir=LR;  \n node [shape=record];\n'
    def addNode(self, root, key,name):
        if root is None:
            return NodeAVL(key,name)
        elif key < root.key:
            root.left = self.addNode(root.left, key,name)
        else:
            root.right = self.addNode(root.right, key,name)
        if self.getNum(root) > 1 and key < root.left.key:
            return self.rotacionDerecha(root)
        if self.getNum(root) < -1 and key > root.right.key:
            return self.rotacionIzqu(root)
        if self.getNum(root) > 1 and key > root.left.key:
            root.left = self.rotacionIzqu(root.left)
            return self.rotacionDerecha(root)
        if self.getNum(root) < -1 and key < root.right.key:
            root.right = self.rotacionDerecha(root.right)
            return self.rotacionIzqu(root)
        d = self.getalt(root.left)
        e = self.getalt(root.right)
        m = max(d, e)
        root.alt = 1 + m
        print(root.alt)
        return root
    def graficarAvl(self):
        with open("AVL.txt", 'w', encoding='utf-8') as f:
            f.write(self.inicio + self.nodes + self.rela+"}")
            f.close()
        cmd = 'dot -Tpng AVL.txt -o AVLs.png'
        os.system(cmd)
        os.system('AVLs.png')
    def rotacionIzqu(self, z):
        newRoot = z.right
        temp = newRoot.left
        newRoot.left = z
        z.right = temp
        z.alt = 1 + max(self.getalt(z.left),self.getalt(z.right))
        newRoot.alt = 1 + max(self.getalt(newRoot.left),self.getalt(newRoot.right))
        return newRoot
    def rotation(self,root):
        print("")
    def graphAVL(self,root):
        if root != None:
            data = "Carne: "+str(root.key)+"\n"+" Nombre: " + root.name
            self.nodes = self.nodes + "nodo" + str(root.key) + " " + '[ label = \"<C0>|'+data+'|<C1>\"];\n'
            if root.left != None:
                self.rela = self.rela + "nodo" + str(root.key) + ":C0->" + "nodo" + str(root.left.key) + "\n"
            if root.right != None:
                self.rela = self.rela + "nodo" + str(root.key) + ":C1->" + "nodo" + str(root.right.key) + "\n"
            self.graphAVL(root.left)
            self.graphAVL(root.right)
    def generateString(self,raiz,tipo):
        string='"DATA": {\n'
        data=""
        if raiz is None:
            print("")
        else:
            if tipo !="izquierda" and tipo !="derecha":
                data +='\t "Value": "'+str(raiz.key)+"-"+raiz.name+'"'
            if tipo=="izquierda":
                data += '"Left":{ \n\t'
                data += '"Value": "' + str(raiz.key) + "-" + raiz.name + '"'
            self.generateString(raiz.left,"izquierda")
            self.generateString(raiz.right,"derecha")

    def grafReco(self, reco):
        print("Inici o->",self.rela2,"null")
        self.recorrido += 'label=\"' + reco + '\"\n'
        self.rela2= self.rela2[:-2:]
        with open("recorrido.txt", 'w', encoding='utf-8') as f:
            f.write(self.recorrido + self.rela2+"\n}")
            f.close()
        cmd = 'dot -Tpng recorrido.txt -o reco.png'
        os.system(cmd)
        os.system('reco.png')
        self.nodes = ""
        self.rela2 = ""

    def recoIn(self,raiz):
        if raiz is None:
            print("")
        else:
            self.recoIn(raiz.left)
            self.rela2 += raiz.key+"_"+raiz.name
            self.rela2 += "->"
            self.recoIn(raiz.right)
    def recoPost(self,raiz):
        if raiz is None:
            print("")
        else:
            self.recoPost(raiz.left)
            self.recoPost(raiz.right)
            self.rela2 += raiz.key+"_"+raiz.name
            self.rela2 += "->"
    def recoPre(self,raiz):
        if raiz is None:
            print("")
        else:
            self.rela2 += raiz.key+"_"+raiz.name
            self.rela2 += "->"
            self.recoPost(raiz.left)
            self.recoPost(raiz.right)

    def rotacionDerecha(self, nodo):
        newRoot = nodo.left
        temp = newRoot.right
        newRoot.right = nodo
        nodo.left = temp
        nodo.alt = max(self.getalt(nodo.left),self.getalt(nodo.right))+1
        newRoot.alt = max(self.getalt(newRoot.left),self.getalt(newRoot.right))+1
        return newRoot
    def getalt(self, root):
        if not root:
            return 0
        return root.alt
    def getNum(self, root):
        if not root:
            return 0
        return self.getalt(root.left) - self.getalt(root.right)
    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.key), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)