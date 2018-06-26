class Peca_Domino:
    def __init__(self, top, bottom):
        self._proximo = None
        self._anterior = None
        self._value = [top, bottom]
        self._sprite = None

    def getNext(self):
        return self._proximo
    def getPrevious(self):
        return self._anterior
    def getValue(self):
        return self._value
    def setNext(self, next):
        self._proximo = next
    def setPrevious(self, prev):
        self._anterior = prev
    def setSprite(self, sprite):
        self._sprite = sprite
    def sprite(self):
        return self._sprite
    def __str__(self):
        return str(self._value)


