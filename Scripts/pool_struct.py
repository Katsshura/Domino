from peca import *
from random import randint
import cocos


class Pool:
    def __init__(self):
        self._pool = []
        self._size = 28

        x = 0
        i = 1
        while i != self._size + 1:
            while x != 7:
                y = x
                while y != 7:
                    self._peca = Peca_Domino(x, y)
                    self._peca.setSprite(cocos.sprite.Sprite("peca" + str(i) + ".png"))
                    self._pool.append(self._peca)
                    i += 1
                    y += 1
                x += 1

    def sort_peca(self):
        self._size -= 1
        return self._pool.pop(randint(0, self._size))
