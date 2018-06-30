import cocos
import layers

cocos.director.director.init(width=1280, height=720, fullscreen=True)
cocos.director.director.run(cocos.scene.Scene(layers.Background(), layers.Main()))
