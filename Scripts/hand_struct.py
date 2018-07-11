class Hand_struct:
    def __init__(self):
        self._head = None #peca no inicio da mao
        self._tail = None #peca no fim da mao
        self._tam = 0

    #In this struct, i'll be receiving the object peca as parameter for Add, Append and Remove

    def add(self, peca):
        if self.len() == 0:
            self._head = peca
            self._tail = peca
            self._tam += 1
        else:
            peca.set_next(self._head)
            self._head.set_previous(peca)
            self._head = peca
            self._tam += 1

    def insert(self, peca):
        self.add(peca)

    def search(self, index):
        atual = self._head
        pos = 0
        if index > self._tam-1:
            return None
        else:
            while pos != index:
                atual = atual.get_next()
                pos += 1
            return atual

    def hand_sprites(self):
        sprites = []
        atual = self._head

        while atual != None:
            sprites.append(atual.sprite())
            atual = atual.get_next()

        return sprites

    def remove(self, index):
        atual = self._head
        pos = 0
        if index > self.len() - 1:
            return False
        elif self._tam > 1:
            while pos != index:
                atual = atual.get_next()
                pos += 1

            if pos == 0:
                temp = self._head.get_next()
                temp.set_previous(None)
                peca = self._head
                self._head = temp
                self._tam -= 1
                return peca

            if pos == self.len() -1:
                tem = self._tail.get_previous()
                tem.set_next(None)
                peca = self._tail
                self._tail = tem
                self._tam -= 1
                return peca
            else:
                next = atual.get_next()
                previous = atual.get_previous()
                previous.set_next(next)
                next.set_previous(previous)
                self._tam -= 1
                return atual

        elif self._tam == 1:
            self._tail = None
            self._head = None
            self._tam -= 1
            return atual


    def len(self):
        return self._tam

    def show(self):
        atual = self._head
        l = "["
        while atual != None:
            if atual.get_next() != None:
                l += str(atual.get_value()) + ","
                atual = atual.get_next()
            else:
                l += str(atual.get_value())
                atual = atual.get_next()
        l += "]"

        return l
