from peca import *
from random import randint
import cocos

class Pool:
    def __init__(self):
        self._pool = []
        self._size = 28
        self._peca1  = Peca_Domino(0,0)
        self._peca1.setSprite(cocos.sprite.Sprite("peca01.png"))
        self._peca2  = Peca_Domino(0,1)
        self._peca2.setSprite(cocos.sprite.Sprite("peca02.png"))
        self._peca3  = Peca_Domino(0,2)
        self._peca3.setSprite(cocos.sprite.Sprite("peca03.png"))
        self._peca4  = Peca_Domino(0,3)
        self._peca4.setSprite(cocos.sprite.Sprite("peca04.png"))
        self._peca5  = Peca_Domino(0,4)
        self._peca5.setSprite(cocos.sprite.Sprite("peca05.png"))
        self._peca6  = Peca_Domino(0,5)
        self._peca6.setSprite(cocos.sprite.Sprite("peca06.png"))
        self._peca7  = Peca_Domino(0,6)
        self._peca7.setSprite(cocos.sprite.Sprite("peca07.png"))
        self._peca8  = Peca_Domino(1,1)
        self._peca8.setSprite(cocos.sprite.Sprite("peca08.png"))
        self._peca9  = Peca_Domino(1,2)
        self._peca9.setSprite(cocos.sprite.Sprite("peca09.png"))
        self._peca10 = Peca_Domino(1,3)
        self._peca10.setSprite(cocos.sprite.Sprite("peca10.png"))
        self._peca11 = Peca_Domino(1,4)
        self._peca11.setSprite(cocos.sprite.Sprite("peca11.png"))
        self._peca12 = Peca_Domino(1,5)
        self._peca12.setSprite(cocos.sprite.Sprite("peca12.png"))
        self._peca13 = Peca_Domino(1,6)
        self._peca13.setSprite(cocos.sprite.Sprite("peca13.png"))
        self._peca14 = Peca_Domino(2,2)
        self._peca14.setSprite(cocos.sprite.Sprite("peca14.png"))
        self._peca15 = Peca_Domino(2,3)
        self._peca15.setSprite(cocos.sprite.Sprite("peca15.png"))
        self._peca16 = Peca_Domino(2,4)
        self._peca16.setSprite(cocos.sprite.Sprite("peca16.png"))
        self._peca17 = Peca_Domino(2,5)
        self._peca17.setSprite(cocos.sprite.Sprite("peca17.png"))
        self._peca18 = Peca_Domino(2,6)
        self._peca18.setSprite(cocos.sprite.Sprite("peca18.png"))
        self._peca19 = Peca_Domino(3,3)
        self._peca19.setSprite(cocos.sprite.Sprite("peca19.png"))
        self._peca20 = Peca_Domino(3,4)
        self._peca20.setSprite(cocos.sprite.Sprite("peca20.png"))
        self._peca21 = Peca_Domino(3,5)
        self._peca21.setSprite(cocos.sprite.Sprite("peca21.png"))
        self._peca22 = Peca_Domino(3,6)
        self._peca22.setSprite(cocos.sprite.Sprite("peca22.png"))
        self._peca23 = Peca_Domino(4,4)
        self._peca23.setSprite(cocos.sprite.Sprite("peca23.png"))
        self._peca24 = Peca_Domino(4,5)
        self._peca24.setSprite(cocos.sprite.Sprite("peca24.png"))
        self._peca25 = Peca_Domino(4,6)
        self._peca25.setSprite(cocos.sprite.Sprite("peca25.png"))
        self._peca26 = Peca_Domino(5,5)
        self._peca26.setSprite(cocos.sprite.Sprite("peca26.png"))
        self._peca27 = Peca_Domino(5,6)
        self._peca27.setSprite(cocos.sprite.Sprite("peca27.png"))
        self._peca28 = Peca_Domino(6,6)
        self._peca28.setSprite(cocos.sprite.Sprite("peca28.png"))

    def start(self):
        self._pool.append(self._peca1)
        self._pool.append(self._peca2)
        self._pool.append(self._peca3)
        self._pool.append(self._peca4)
        self._pool.append(self._peca5)
        self._pool.append(self._peca6)
        self._pool.append(self._peca7)
        self._pool.append(self._peca8)
        self._pool.append(self._peca9)
        self._pool.append(self._peca10)
        self._pool.append(self._peca11)
        self._pool.append(self._peca12)
        self._pool.append(self._peca13)
        self._pool.append(self._peca14)
        self._pool.append(self._peca15)
        self._pool.append(self._peca16)
        self._pool.append(self._peca17)
        self._pool.append(self._peca18)
        self._pool.append(self._peca19)
        self._pool.append(self._peca20)
        self._pool.append(self._peca21)
        self._pool.append(self._peca22)
        self._pool.append(self._peca23)
        self._pool.append(self._peca24)
        self._pool.append(self._peca25)
        self._pool.append(self._peca26)
        self._pool.append(self._peca27)
        self._pool.append(self._peca28)

    def sort_peca(self):
        self._size -= 1
        return self._pool.pop(randint(0, self._size))
