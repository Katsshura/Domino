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
class Background(cocos.layer.Layer):
    def __init__(self):
        super(Background, self).__init__()

        background = cocos.sprite.Sprite('background.png')
        background.position = 1280 // 2, 720 // 2
        self.add(background)

class Main(cocos.layer.Layer()):
    is_event_handler = True

    def __init__(self):
        super(Main, self).__init__()
        self._pool = Pool()
        self._hand = Hand_struct()
        self._pool.start()
        self.start_hand()
        self._h_sprites = self._hand.hand_sprites()

        self.set_sprites()

        self._text = cocos.text.Label("", font_name="Times New Roman", font_size=32, anchor_x="center", anchor_y="center")
        self._text.position = 1280 // 2, 720 // 2
        self.add(self._text)

    def set_sprites(self):
        pos_x = -150
        for i in range(7):
            sprite = self._h_sprites[i]
            sprite.position = (1280//2)+pos_x, (720//2)-300
            sprite.scale = 0.45
            self.add(sprite)
            pos_x += 50

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self._text.element.text = "Draging"

    def on_mouse_release(self, x, y, buttons, modifiers):
        self._text.element.text = "Released"

    def on_mouse_press(self, x, y, buttons, modifiers):
        self._text.element.text = 'Pressed'

    def start_hand(self):
        for i in range(7):
            self._hand.insert(self._pool.sort_peca())
        '''sprite2 = cocos.sprite.Sprite('peca01.png')
        sprite2.position = (1280//2), (720//2)-300
        sprite2.scale = 0.45
        self.add(sprite2)
        sprite3 = cocos.sprite.Sprite('peca02.png')
        sprite3.position = (1280//2)+50, (720//2)-300
        sprite3.scale = 0.45
        self.add(sprite3)
        text = cocos.text.Label("Domino Game", font_name = "Times New Roman", font_size = 32, anchor_x = "center", anchor_y = "center")
        text.position = 1280//2, 720//2
        self.add(text)
        sub_text = cocos.text.Label("A game made by: Emerson Alves", font_name = "Times New Roman", font_size = 24, anchor_x = "center", anchor_y = "center")
        sub_text.position = 320, 240
        self.add(sub_text)
        scale = ScaleBy(2, duration=2)
        text.do(Repeat(scale + Reverse(scale)))
        sub_text.do(Repeat(Reverse(scale) + scale))'''

cocos.director.director.init( width=1280, height=720)
cocos.director.director.run(cocos.scene.Scene(Background(),Main()))

