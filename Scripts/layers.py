import cocos
import pyglet
from cocos.actions import *
from cocos.scene import *
from pool_struct import *
from hand_struct import *
from domino_struct import *


# 42x83 each

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
        self._bot1 = Hand_struct()
        self._bot2 = Hand_struct()
        self._bot3 = Hand_struct()
        self._domino = Domino_struct()
        self._isPlayer = False
        self._isBot1 = False
        self._isBot2 = False
        self._isBot3 = False
        self.start_hand()
        self.start_bots_hand()
        self._h_sprites = self._hand.hand_sprites()
        self._d_sprites = []
        self._pieceIndex = None
        self._isPieceSelected = False
        self._lastPosition = None
        self._indiceHead = 0
        self._indiceTail = 1
        self.set_sprites()
        self._label = cocos.text.Label("", font_name='Times New Roman', font_size=32, anchor_x='center',
                                       anchor_y='center')

        layer = cocos.layer.ColorLayer(255, 255, 255, 255, width=100, height=30)
        layer.position = (1100, 25)
        self.add(layer)
        self._label.position = 1280 // 2, 720 // 2
        self.add(self._label)
        self.load_parts_on_screen()

    def set_sprites(self):
        pos_x = -125
        for i in range(7):
            sprite = self._h_sprites[i]
            sprite.anchor = sprite.get_rect().bottomleft
            sprite.position = (1280 // 2) + pos_x, (720 // 2) - 250
            sprite.scale = 0.45
            self.add(sprite)
            pos_x += 50

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._isPieceSelected:
            self._h_sprites[self._pieceIndex].position = x + 31, y + 51

    def on_mouse_release(self, x, y, buttons, modifiers):
        self._isPieceSelected = False
        if self._isPlayer:
            if self._h_sprites[self._pieceIndex].y > 720 // 4:
                if self._domino.len() != 0:
                    if self._h_sprites[self._pieceIndex].x > 640:  # olha pra direita
                        self.check_tail()
                    elif self._h_sprites[self._pieceIndex].x < 640:  # olha pra esquerda
                        self.check_head()
                else:
                    if (self._hand.search(self._pieceIndex) == self._hand.search(self.check_highest_piece())):
                        if self.is_bomb():
                            self._h_sprites[self._pieceIndex].position = (1280 // 2), 720 // 2
                            self._h_sprites[self._pieceIndex].rotation = 90
                            self._d_sprites.insert(0, self._h_sprites.pop(self._pieceIndex))
                            self.throw()
                        else:
                            self._h_sprites[self._pieceIndex].position = (1280 // 2) + 83, 720 // 2
                            self._h_sprites[self._pieceIndex].rotation = -90
                            self._d_sprites.insert(0, self._h_sprites.pop(self._pieceIndex))
                            self.throw()
                    else:
                        self._h_sprites[self._pieceIndex].position = self._lastPosition
            else:
                self._h_sprites[self._pieceIndex].position = self._lastPosition

        else:
            pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._isPlayer:
            if self.check_click(x, y):
                self._isPieceSelected = True
                print(self.is_bomb())
                print(self._pieceIndex, self._hand.search(self._pieceIndex), self._hand.len())
                '''print(self._domino.head(), self._domino.tail())'''
                self._lastPosition = self._h_sprites[self._pieceIndex].position
            else:
                if self.pass_button(x, y):
                    self._isPlayer = False
                    self._isBot1 = True
                    self.bot_time()
                self._isPieceSelected = False
                self._lastPosition = None
        else:
            print("Not Your Time")
            self.bot_time()

        print("Bot 1 - " + str(self._bot1.show()), "\n" + "Bot 2 - " + str(self._bot2.show()),
              "\n" + "Bot 3 - " + str(self._bot3.show()), "\n" + "Domino - " + str(self._domino.show()))

    def check_click(self, x, y):
        check = False
        pos = 0
        while pos < len(self._h_sprites) and not check:
            if self._h_sprites[pos].get_rect().contains(x, y):
                check = True
                self._pieceIndex = pos
            else:
                pos += 1
        return check

    def check_head(self):
        if (self._domino.head().getValue()[self._indiceHead] in self._hand.search(self._pieceIndex).getValue()):
            self.place_at_left()
        else:
            self._h_sprites[self._pieceIndex].position = self._lastPosition

    def check_tail(self):
        if (self._domino.tail().getValue()[self._indiceTail] in self._hand.search(self._pieceIndex).getValue()):
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
            if (peca.getValue()[0] == peca.getValue()[1] and self._domino.len() == 0):
                peca_value += 20
            if peca_value > highest:
                highest = peca_value
                aux += 1
                pos = aux
            else:
                aux += 1
        return pos

    def is_bomb(self):
        return (self._hand.search(self._pieceIndex).getValue()[0] == self._hand.search(self._pieceIndex).getValue()[1])

    def start_hand(self):
        for i in range(7):
            a = self._pool.sort_peca()
            self._hand.insert(a)
            if a.getValue()[0] == a.getValue()[1] and a.getValue()[0] == 6:
                self._isPlayer = True

    def place_at_right(self):
        a = self._h_sprites.pop(self._pieceIndex)
        self._d_sprites.append(a)
        self.throw_right(a)

    def place_at_left(self):
        a = self._h_sprites.pop(self._pieceIndex)
        self._d_sprites.insert(0, a)
        self.throw_left(a)

    def throw_left(self, a):
        peca = self._hand.remove(self._pieceIndex)
        peca.setPrevious(None)
        peca.setNext(None)
        if self._domino.head().getValue()[0] is peca.getValue()[0]:
            temp = peca.getValue()[1]
            peca.getValue()[1] = peca.getValue()[0]
            peca.getValue()[0] = temp
            self._domino.insert(peca, 0)
            a.rotation = 90
            print(a.get_rect())
            a.position = self._d_sprites[0].x - (83 // 2) + 2, 720 // 2
        elif self._domino.head().getValue()[0] is peca.getValue()[1]:
            self._domino.insert(peca, 0)
            a.rotation = -90
            print("de baixo: {}".format((83 // 3)))
            print(a.get_rect())
            a.position = self._d_sprites[0].x + 83 // 2, (720 // 2) - 42

        self._isPlayer = False
        self._isBot1 = True
        self.bot_time()

    def throw_right(self, a):
        peca = self._hand.remove(self._pieceIndex)
        peca.setPrevious(None)
        peca.setNext(None)
        if self._domino.tail().getValue()[1] is peca.getValue()[0]:
            self._domino.append(peca)
            a.rotation = -90
            if len(self._d_sprites) > 1:
                a.position = self._d_sprites[1].x + 83 // 2, (720 // 2) - 42
            else:
                a.position = self._d_sprites[0].x + 83 // 2, (720 // 2) - 42

        elif self._domino.tail().getValue()[1] is peca.getValue()[1]:
            temp = peca.getValue()[1]
            peca.getValue()[1] = peca.getValue()[0]
            peca.getValue()[0] = temp
            self._domino.append(peca)
            a.rotation = 90
            if len(self._d_sprites) > 1:
                a.position = self._d_sprites[1].x + (83 // 2) + 2, 720 // 2
            else:
                a.position = self._d_sprites[0].x + (83 // 2) + 2, 720 // 2

        self._isPlayer = False
        self._isBot1 = True
        self.bot_time()

    def throw(self):
        peca = self._hand.remove(self._pieceIndex)
        peca.setPrevious(None)
        peca.setNext(None)
        self._domino.append(peca)
        self._isPlayer = False
        self._isBot1 = True
        self.bot_time()

    def start_bots_hand(self):
        for i in range(7):
            a = self._pool.sort_peca()
            self._bot1.insert(a)
            if a.getValue()[0] == a.getValue()[1] and a.getValue()[0] == 6:
                self._isBot1 = True
        for i in range(7):
            b = self._pool.sort_peca()
            self._bot2.insert(b)
            if b.getValue()[0] == b.getValue()[1] and b.getValue()[0] == 6:
                self._isBot2 = True
        for i in range(7):
            c = self._pool.sort_peca()
            self._bot3.insert(c)
            if c.getValue()[0] == c.getValue()[1] and c.getValue()[0] == 6:
                self._isBot3 = True

        self.bot_time()

    def bot_time(self):
        if self._isBot1:
            if self._domino.len() != 0:
                for i in range(self._bot1.len()):
                    peca = self._bot1.search(i)
                    if (self._domino.head().getValue()[0] in peca.getValue()):
                        print("Bot 1 Tem peça")
                        self.throw_bot(1, i, 0)
                        self._isBot1 = False
                        self._isBot2 = True
                        break
                    elif (self._domino.tail().getValue()[1] in peca.getValue()):
                        print("Bot 1 Tem peça")
                        self.throw_bot(1, i, 1)
                        self._isBot1 = False
                        self._isBot2 = True
                        break
                    else:
                        self._isBot1 = False
                        self._isBot2 = True
            else:
                for i in range(self._bot1.len()):
                    p = self._bot1.search(i)
                    if (p.getValue()[0] == p.getValue()[1] and p.getValue()[0] == 6):
                        print("Comecando a mao bot1" + " " + self._bot1.show())
                        self.throw_bot(1, i, 0)
                        self._isBot1 = False
                        self._isBot2 = True
                        break
                    else:
                        self._isBot1 = False
                        self._isBot2 = True
            if self._bot1.len() != 0:
                self.bot_time()
            else:
                self._label.element.text = "Bot 1 Venceu!!"
                self._isPlayer = False
                self._isBot1 = False
                self._isBot2 = False
                self._isBot3 = False
        elif self._isBot2:
            if self._domino.len() != 0:
                for i in range(self._bot2.len()):
                    peca = self._bot2.search(i)
                    if (self._domino.head().getValue()[0] in peca.getValue()):
                        print("Bot 2 Tem peça")
                        self.throw_bot(2, i, 0)
                        self._isBot2 = False
                        self._isBot3 = True
                        break
                    elif (self._domino.tail().getValue()[1] in peca.getValue()):
                        print("Bot 2 Tem peça")
                        self.throw_bot(2, i, 1)
                        self._isBot2 = False
                        self._isBot3 = True
                        break
                    else:
                        self._isBot2 = False
                        self._isBot3 = True
            else:
                for i in range(self._bot2.len()):
                    p = self._bot2.search(i)
                    if (p.getValue()[0] == p.getValue()[1] and p.getValue()[0] == 6):
                        print("Comecando a mao bot2" + " " + self._bot2.show())
                        self.throw_bot(2, i, 0)
                        self._isBot2 = False
                        self._isBot3 = True
                        break
                    else:
                        self._isBot2 = False
                        self._isBot3 = True
            if self._bot2.len() != 0:
                self.bot_time()
            else:
                self._label.element.text = "Bot 2 Venceu!!"
                self._isPlayer = False
                self._isBot1 = False
                self._isBot2 = False
                self._isBot3 = False

        elif self._isBot3:
            if self._domino.len() != 0:
                for i in range(self._bot3.len()):
                    peca = self._bot3.search(i)
                    if (self._domino.head().getValue()[0] in peca.getValue()):
                        print("Bot 3 Tem peça")
                        self.throw_bot(3, i, 0)
                        self._isBot3 = False
                        self._isPlayer = True
                        break
                    elif (self._domino.tail().getValue()[1] in peca.getValue()):
                        print("Bot 3 Tem peça")
                        self.throw_bot(3, i, 1)
                        self._isBot3 = False
                        self._isPlayer = True
                        break
                    else:
                        self._isBot3 = False
                        self._isPlayer = True
            else:
                for i in range(self._bot3.len()):
                    p = self._bot3.search(i)
                    if (p.getValue()[0] == p.getValue()[1] and p.getValue()[0] == 6):
                        print("Comecando a mao bot3" + " " + self._bot3.show())
                        self.throw_bot(3, i, 0)
                        self._isBot3 = False
                        self._isPlayer = True
                        break
                    else:
                        self._isBot3 = False
                        self._isPlayer = True

            if self._bot3.len() == 0:
                self._label.element.text = "Bot 3 Venceu!!"
                self._isPlayer = False
                self._isBot1 = False
                self._isBot2 = False
                self._isBot3 = False

    def throw_bot(self, bot, index, position):
        if bot == 1:
            if self._domino.len() != 0:
                if position == 0:
                    peca = self._bot1.remove(index)
                    peca.setPrevious(None)
                    peca.setNext(None)
                    if self._domino.head().getValue()[0] is peca.getValue()[0]:
                        temp = peca.getValue()[1]
                        peca.getValue()[1] = peca.getValue()[0]
                        peca.getValue()[0] = temp
                        self._domino.insert(peca, 0)
                    elif self._domino.head().getValue()[0] is peca.getValue()[1]:
                        self._domino.insert(peca, 0)
                elif position == 1:
                    peca = self._bot1.remove(index)
                    peca.setPrevious(None)
                    peca.setNext(None)
                    if self._domino.tail().getValue()[1] is peca.getValue()[0]:
                        self._domino.append(peca)
                    elif self._domino.tail().getValue()[1] is peca.getValue()[1]:
                        temp = peca.getValue()[1]
                        peca.getValue()[1] = peca.getValue()[0]
                        peca.getValue()[0] = temp
                        self._domino.append(peca)
            else:
                peca = self._bot1.remove(index)
                peca.setPrevious(None)
                peca.setNext(None)
                self._domino.insert(peca, 1)
        elif bot == 2:
            if self._domino.len() != 0:
                if position == 0:
                    peca = self._bot2.remove(index)
                    peca.setPrevious(None)
                    peca.setNext(None)
                    if self._domino.head().getValue()[0] is peca.getValue()[0]:
                        temp = peca.getValue()[1]
                        peca.getValue()[1] = peca.getValue()[0]
                        peca.getValue()[0] = temp
                        self._domino.insert(peca, 0)
                    elif self._domino.head().getValue()[0] is peca.getValue()[1]:
                        self._domino.insert(peca, 0)
                elif position == 1:
                    peca = self._bot2.remove(index)
                    peca.setPrevious(None)
                    peca.setNext(None)
                    if self._domino.tail().getValue()[1] is peca.getValue()[0]:
                        self._domino.append(peca)
                    elif self._domino.tail().getValue()[1] is peca.getValue()[1]:
                        temp = peca.getValue()[1]
                        peca.getValue()[1] = peca.getValue()[0]
                        peca.getValue()[0] = temp
                        self._domino.append(peca)
            else:
                peca = self._bot2.remove(index)
                peca.setPrevious(None)
                peca.setNext(None)
                self._domino.insert(peca, 1)
        elif bot == 3:
            if self._domino.len() != 0:
                if position == 0:
                    peca = self._bot3.remove(index)
                    peca.setPrevious(None)
                    peca.setNext(None)
                    if self._domino.head().getValue()[0] is peca.getValue()[0]:
                        temp = peca.getValue()[1]
                        peca.getValue()[1] = peca.getValue()[0]
                        peca.getValue()[0] = temp
                        self._domino.insert(peca, 0)
                    elif self._domino.head().getValue()[0] is peca.getValue()[1]:
                        self._domino.insert(peca, 0)
                elif position == 1:
                    peca = self._bot3.remove(index)
                    peca.setPrevious(None)
                    peca.setNext(None)
                    if self._domino.tail().getValue()[1] is peca.getValue()[0]:
                        self._domino.append(peca)
                    elif self._domino.tail().getValue()[1] is peca.getValue()[1]:
                        temp = peca.getValue()[1]
                        peca.getValue()[1] = peca.getValue()[0]
                        peca.getValue()[0] = temp
                        self._domino.append(peca)
            else:
                peca = self._bot3.remove(index)
                peca.setPrevious(None)
                peca.setNext(None)
                self._domino.insert(peca, 1)
        else:
            raise ("Exception, no bot found")

    def pass_button(self, x, y):
        if x >= 1100 and x <= 1200:
            if y >= 25 and y <= 55:
                return True
            return False
        else:
            return False

    def load_parts_on_screen(self):
        array_sprite_bot1 = self._bot1.hand_sprites()
        self.get_sprites(array_sprite_bot1, 1280, -125, 50, "y")
        array_sprite_bot2 = self._bot2.hand_sprites()
        self.get_sprites(array_sprite_bot2, -150, 720, 50, "x")
        array_sprite_bot3 = self._bot3.hand_sprites()
        self.get_sprites(array_sprite_bot3, 0, -125, 50, "y")

    def get_sprites(self, array, pos_x, pos_y, space, type):
        if type == 'x':
            for i in range(len(array)):
                sprite = array[i]
                sprite.position = (1280 // 2) + pos_x, pos_y
                sprite.scale = 0.45
                self.add(sprite)
                pos_x += space
        else:
            for i in range(len(array)):
                sprite = array[i]
                sprite.rotation = -90
                sprite.position = pos_x, (720 // 2) + pos_y
                sprite.scale = 0.45
                self.add(sprite)
                pos_y += space

        return pos_x
