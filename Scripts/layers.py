import cocos
import pyglet
from cocos.actions import *
from cocos.scene import *
from pool_struct import *
from hand_struct import *
from domino_struct import *

#42x83 each

class Background(cocos.layer.Layer):
    def __init__(self):
        super(Background, self).__init__()

        background = cocos.sprite.Sprite('background.png')
        background.position = 1280 // 2, 720 // 2
        self.add(background)

class Main(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(Main, self).__init__()
        self._pool = Pool()
        self._hand = Hand_struct()
        self._domino = Domino_struct()
        self.start_hand()
        self._h_sprites = self._hand.hand_sprites()
        self._d_sprites = []
        self._pieceIndex = None
        self._isPieceSelected = False
        self._lastPosition = None
        self._indiceHead = 0
        self._indiceTail = 1
        print(self._hand.len(), self._h_sprites.__len__(),self._domino.len())

        self.set_sprites()

    def set_sprites(self):
        pos_x = -125
        for i in range(7):
            sprite = self._h_sprites[i]
            sprite.anchor = sprite.get_rect().bottomleft
            sprite.position = (1280//2) + pos_x, (720//2)-250
            sprite.scale = 0.45
            self.add(sprite)
            pos_x += 50

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._isPieceSelected:
            self._h_sprites[self._pieceIndex].position = x+31, y+51

    def on_mouse_release(self, x, y, buttons, modifiers):
        self._isPieceSelected = False
        if self._h_sprites[self._pieceIndex].y > 720//4:
            if self._domino.len() != 0:
                 if self._h_sprites[self._pieceIndex].x > 640: #olha pra direita
                    self.check_tail()
                 elif self._h_sprites[self._pieceIndex].x < 640: #olha pra esquerda
                    self.check_head()
            else:
                if(self._hand.search(self._pieceIndex) == self._hand.search(self.check_highest_piece())):
                    self._h_sprites[self._pieceIndex].position = 1280//2, 720//2
                    self._d_sprites.insert(0,self._h_sprites.pop(self._pieceIndex))
                    self.throw_left()
                else:
                    self._h_sprites[self._pieceIndex].position = self._lastPosition
        else:
            self._h_sprites[self._pieceIndex].position = self._lastPosition

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_click(x,y):
            self._isPieceSelected = True
            print(self._pieceIndex, self._hand.search(self._pieceIndex), self._hand.len())
            print(self._domino.head())
            print(self._domino.tail())
            self._lastPosition = self._h_sprites[self._pieceIndex].position
        else:
            self._isPieceSelected = False
            self._lastPosition = None

    def check_click(self,x,y):
        check = False
        pos = 0
        while pos < len(self._h_sprites) and not check:
            if self._h_sprites[pos].get_rect().contains(x,y):
                check = True
                self._pieceIndex = pos
            else:
                pos += 1
        return check

    def check_head(self):
        #value for head is on index 0
        self.count = 0
        if (self._domino.head().getValue()[self._indiceHead] == self._hand.search(self._pieceIndex).getValue()[self._indiceHead]):
            self.place_at_left()
        else:
            self._h_sprites[self._pieceIndex].position = self._lastPosition

    def check_tail(self):
        if (self._domino.tail().getValue()[1] == self._hand.search(self._pieceIndex).getValue()[1]):
            self.place_at_right()
        else:
            self._h_sprites[self._pieceIndex].position = self._lastPosition

    def check_highest_piece(self):
        highest = 0
        aux = -1
        pos = 0
        for i in range(self._hand.len()):
            peca = self._hand.search(i)
            peca_value = peca.getValue()[0] + peca.getValue()[1]
            if(peca.getValue()[0] == peca.getValue()[1] and self._domino.len() == 0):
                peca_value += 20
            if peca_value > highest:
                highest = peca_value
                aux += 1
                pos = aux
            else:
                aux += 1
        return pos


    def start_hand(self):
        for i in range(7):
            self._hand.insert(self._pool.sort_peca())

    def place_at_right(self):
        a = self._h_sprites.pop(self._pieceIndex)
        self._d_sprites.append(a)
        self.throw_right()
        #print("sim", self._hand.show(), self._domino.show())

    def place_at_left(self):
        a = self._h_sprites.pop(self._pieceIndex)
        self._d_sprites.insert(0,a)
        self.throw_left()
        #print("sim", self._hand.show(), self._domino.show())

    def throw_left(self):
        peca = self._hand.remove(self._pieceIndex)
        peca.setPrevious(None)
        peca.setNext(None)
        self._domino.insert(peca, 0)

    def throw_right(self):
        peca = self._hand.remove(self._pieceIndex)
        peca.setPrevious(None)
        peca.setNext(None)
        self._domino.append(peca)

    def change_head(self, n):
        if n%2 == 0:
            self._indiceHead = 1
        else:
            self._indiceHead = 0

    def change_tail(self, n):
        if n%2 == 0:
            self._indiceTail = 0
        else:
            self._indiceTail = 1
