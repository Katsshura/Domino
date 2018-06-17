import cocos
from cocos.actions import *

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


cocos.director.director.init()
hello_layer = HelloWorld()
cocos.director.director.run(cocos.scene.Scene(hello_layer))