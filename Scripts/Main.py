import cocos
import pyglet
from cocos.actions import *
from cocos.scene import *

class HelloWorld(cocos.layer.ColorLayer):
    def __init__(self):
        super(HelloWorld, self).__init__(64,645,255,255)
        text = cocos.text.Label("Domino Game", font_name = "Times New Roman", font_size = 32, anchor_x="center", anchor_y = "center")
        text.position = 320, 340
        self.add(text)
        sub_text = cocos.text.Label("A game made by: Emerson Alves", font_name = "Times New Roman", font_size = 24, anchor_x="center", anchor_y = "center")
        sub_text.position = 320, 240
        self.add(sub_text)
        scale = ScaleBy(2, duration=2)
        text.do(Repeat(scale + Reverse(scale)))
        sub_text.do(Repeat(Reverse(scale) + scale))

class KeyDisplay(cocos.layer.Layer):

    # If you want that your layer receives director.window events
    # you must set this variable to 'True'
    is_event_handler = True

    def __init__(self):

        super( KeyDisplay, self ).__init__()

        self.text = cocos.text.Label("", x=100, y=280 )

        # To keep track of which keys are pressed:
        self.keys_pressed = set()
        self.update_text()
        self.add(self.text)

    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed.
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
        """

        self.keys_pressed.add(key)
        self.update_text()


    def on_key_release(self, key, modifiers):
        """This function is called when a key is released.

        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)

        Constants are the ones from pyglet.window.key
        """

        self.keys_pressed.remove(key)
        self.update_text()

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        text = 'Keys: ' + ','.join(key_names)
        # Update self.text
        self.text.element.text = text

cocos.director.director.init( width=1280, height=720)
cocos.director.director.run(cocos.scene.Scene(KeyDisplay()))


