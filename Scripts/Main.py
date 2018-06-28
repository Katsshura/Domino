import cocos
import pyglet
from cocos.actions import *
from pool_struct import *
import sys,os
from cocos.scene import *
from peca import *
from random import randint
from hand_struct import *

#Those classes are just for tests

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
        self._pool.start()
        self.start_hand()
        self._h_sprites = self._hand.hand_sprites()
        self._pieceIndex = None
        self._isPieceSelected = False

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

    def on_mouse_press(self, x, y, buttons, modifiers):
        print(x,y)

        if self.check_click(x,y):
            print(True, self._hand.search(self._pieceIndex))
            self._isPieceSelected = True
        else:
            self._isPieceSelected = False
            print(False)

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


    def start_hand(self):
        for i in range(7):
            self._hand.insert(self._pool.sort_peca())


cocos.director.director.init( width=1280, height=720)
cocos.director.director.run(cocos.scene.Scene(Background(),Main()))

