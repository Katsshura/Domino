from peca import *

class Domino_struct:
    def __init__(self):
        self._head = None #peca no topo do domino
        self._tail = None #peca no fim do domino
        self._tam = 0

    #In this struct, i'll be receiving the object peca as parameter for Add, Append and Remove

    def add(self, peca):
        if self.len() == 0:
            self._head = peca
            self._tail = peca
            self._tam += 1
        else:
            peca.setNext(self._head)
            self._head.setPrevious(peca)
            self._head = peca
            self._tam += 1

    def append(self, peca):
        if self.len() == 0:
            self._head = peca
            self._tail = peca
            self._tam += 1
        else:
            peca.setPrevious(self._tail)
            self._tail.setNext(peca)
            self._tail = peca
            self._tam += 1

    def insert(self, peca, index):
        if index == 0:
            self.add(peca)
        elif index == 1:
            self.append(peca)
        else:
            raise Exception("Index out of bounds")

    def search(self, index):
        atual = self._head
        pos = 0
        if index > self._tam-1:
            return False
        else:
            while pos != index:
                atual = atual.getNext()
                pos += 1
            return atual

    def remove(self, index):
        atual = self._head
        pos = 0
        if index > self.len() - 1:
            return False
        else:
            while pos != index:
                atual = atual.getNext()
                pos += 1

            if pos == 0:
                temp = self._head.getNext()
                temp.setPrevious(None)
                peca = self._head
                self._head = temp
                return peca

            if pos == self.len() -1:
                tem = self._tail.getPrevious()
                tem.setNext(None)
                peca = self._tail
                self._tail = tem
                return peca
            else:
                next = atual.getNext()
                previous = atual.getPrevious()
                previous.setNext(next)
                next.setPrevious(previous)
                return atual


    def len(self):
        return self._tam

    def show(self):
        atual = self._head
        l = "["
        while atual != None:
            if atual.getNext() != None:
                l += str(atual.getValue()) + ","
                atual = atual.getNext()
            else:
                l += str(atual.getValue())
                atual = atual.getNext()
        l += "]"

        return l


peca1 = Peca_Domino(0,3)
peca2 = Peca_Domino(2,3)
peca3 = Peca_Domino(1,4)
peca4 = Peca_Domino(1,5)
peca5 = Peca_Domino(6,6)
peca6 = Peca_Domino(2,2)
f = Domino_struct()

f.append(peca1)
f.append(peca2)
f.append(peca3)
f.append(peca4)
f.append(peca5)
print(f.show())
f.insert(peca6,1)
print(f.show())
