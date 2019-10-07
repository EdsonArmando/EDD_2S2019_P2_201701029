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
    def addBlock(self):
        new = BlockNode()
        if self.first is None:
            new.index=self.cont
            new.data="EDD"
            new.claSS="[EDD]"
            new.prevHash ="0000"
            new.hash = self.sha256(str(new.index)+str(new.time)+str(new.claSS)+str(new.data)+str(new.prevHash))
            self.last = new
            self.first = new
            self.last.next=None
        else:
            new.index = self.cont
            new.data = "EDD"
            new.claSS = "[EDD]"
            new.prevHash = self.last.hash
            new.hash = self.sha256(str(new.index)+str(new.time)+str(new.claSS)+str(new.data)+str(new.prevHash))
            self.last.next=new
            new.prev=self.last
            self.last=new
            self.last.next=None
        self.cont+=1
    def showBlock(self):
        aux=self.first
        while aux !=None:
            print("No: ", aux.index, "Time: ", aux.time , "Hash", aux.prevHash)
            aux=aux.next
    def sha256(self,val):
        h=hashlib.sha256(val.encode()).hexdigest()
        return h

list = ListBlockChain()
list.addBlock()
list.addBlock()
list.addBlock()
list.addBlock()
list.addBlock()
list.showBlock()