import os
from datetime import datetime
import hashlib
class BlockNode:
    def __init__(self):
        now = datetime.now()
        self.time = now.strftime("%d-%m-%y: :%H:%M:%S")
        self.index=0
        self.data = None
        self.claSS=None
        self.hash=None
        self.prevHash=None
        self.next=None
        self.prev=None

class ListBlockChain:
    def __init__(self):
        self.first=None
        self.last=None
        self.cont=0
    def addBlock(self,nodo):
        new = nodo
        if self.first is None:
            new.index=self.cont
            new.prevHash ="0000"
            new.hash = self.sha256(str(new.index)+str(new.time)+str(new.claSS)+str(new.data)+str(new.prevHash))
            self.last = new
            self.first = new
            self.last.next=None
        else:
            new.index = self.cont
            new.prevHash = self.last.hash
            new.hash = self.sha256(str(new.index)+str(new.time)+str(new.claSS)+str(new.data)+str(new.prevHash))
            self.last.next=new
            new.prev=self.last
            self.last=new
            self.last.next=None
        self.cont+=1

    def GenerateImage(self):
        texto = 'digraph { \n node [shape=record]; \n label="ListBlock";\n null [label="NULL" shape=box];\n'
        datesSocre = ""
        aux = self.first
        cont = 0
        while aux != None:
            datesSocre += str(cont) + '[label="{<data> ' + 'Class: ' + aux.claSS + '\\n Time: ' + aux.time +\
                          "\\n Has: "+aux.hash+"\\n PrevHash: "+aux.prevHash+ '| <ref>  }", width=1.2]\n'
            if aux.next != None:
                datesSocre += str(cont) + ':ref:c' + '->' + str(cont + 1) + ':data\n'
            cont += 1
            aux = aux.next
        with open("ListBlock.txt", 'w', encoding='utf-8') as f:
            f.write(texto + datesSocre + str(cont - 1) + ':ref:c->null\n}')
            f.close()
        cmd = 'dot -Tpng ListBlock.txt -o listBlock.png'
        os.system(cmd)
        os.system('listBlock.png')
    def showBlock(self):
        aux=self.first
        while aux !=None:
            print("No: ", aux.index, "Time: ", aux.time , "Hash", aux.prevHash)
            aux=aux.next
    def sha256(self,val):
        h=hashlib.sha256(val.encode()).hexdigest()
        return h
