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
        self._pieceIndex = None
        self._isPieceSelected = False
        self._lastPosition = None

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
                    self.throw_piece()
                else:
                    self._h_sprites[self._pieceIndex].position = self._lastPosition
        else:
            self._h_sprites[self._pieceIndex].position = self._lastPosition

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_click(x,y):
            self._isPieceSelected = True
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
        if (self._domino.head().getValue()[0] == self._hand.search(self._pieceIndex).getValue()[0]):
            print("sim", self._hand.search(self._pieceIndex).getValue()[0])
        else:
            print("nao", self._hand.search(self._pieceIndex).getValue())

    def check_tail(self):
        pass

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

    def throw_piece(self):
        peca = self._hand.remove(self._pieceIndex)
        peca.setPrevious(None)
        peca.setNext(None)
        self._domino.insert(peca, 0)