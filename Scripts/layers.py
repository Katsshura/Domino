import cocos
import pyglet
from cocos.actions import *
from cocos.scene import *
from pool_struct import *
from hand_struct import *
from domino_struct import *


# Class que define a imagem de fundo
class Background(cocos.layer.Layer):
    def __init__(self):
        super(Background, self).__init__()

        background = cocos.sprite.Sprite('background.png')
        background.position = 1280 // 2, 720 // 2
        self.add(background)


# Funcao que verifica se o botao de passar foi clicado
def pass_button(x, y):
    if 1100 <= x <= 1200:
        if 25 <= y <= 55:
            return True
        return False
    else:
        return False


# Class para definir as funcoes do jogo
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
        self._isGameClosed = False
        self._bot1Passed = False
        self._bot2Passed = False
        self._bot3Passed = False
        self._playerPassed = False
        self.start_hand()
        self.start_bots_hand()
        self.load_parts_on_screen()
        self._h_sprites = self._hand.hand_sprites()
        self._d_sprites = []
        self._pieceIndex = None
        self._isPieceSelected = False
        self._lastPosition = None
        self._indiceHead = 0
        self._indiceTail = 1
        self.set_sprites()
        self._posX = 0
        self._posY = 0
        self._label = cocos.text.Label("",
                                       font_name='Times New Roman',
                                       font_size=32,
                                       anchor_x='center',
                                       anchor_y='center')  # Exibe Texto na tela

        layer = cocos.layer.ColorLayer(24, 24, 255, 50, width=100, height=30)
        layer.position = (1100, 25)
        layerText = cocos.text.Label("PASS",
                                     font_name='Times New Roman',
                                     font_size=20,
                                     anchor_x='center',
                                     anchor_y='center')
        layerText.position = (100 // 2, 30 // 2)
        layer.add(layerText)
        # Da linha 64 a 72 cria o label para passar a vez

        bomb6 = cocos.sprite.Sprite("peca28.png")
        bomb6.anchor = bomb6.get_rect().bottomleft
        bomb6.position = (1280//2),(720//2)
        bomb6.scale = 0.45
        self.add(bomb6)

        self.add(layer)  # Adiciona o botao no layer principal
        self._label.position = 1280 // 2, 720 - (720 // 8)  # Define a posicao do texto
        self.add(self._label)

    # Exibe na tela as pecas da mao do player
    def set_sprites(self):
        pos_x = -125
        for i in range(self._hand.len()):
            sprite = self._h_sprites[i]
            sprite.anchor = sprite.get_rect().bottomleft
            sprite.position = (1280 // 2) + pos_x, (720 // 2) - 250
            sprite.scale = 0.45
            self.add(sprite)
            pos_x += 50

    # Funcao para checar se o mouse esta sendo clicado e arrastado
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._isPieceSelected:
            self._h_sprites[self._pieceIndex].position = x + 31, y + 51

    # Funcao para checar se o botao do mouse foi soltado
    def on_mouse_release(self, x, y, buttons, modifiers):
        self._isPieceSelected = False
        try:
            if self._isPlayer:
                if self._h_sprites[self._pieceIndex].y > 720 // 4:
                    if self._domino.len() != 0:
                        if self._h_sprites[self._pieceIndex].x > 640:  # olha pra direita
                            self.check_tail()
                        elif self._h_sprites[self._pieceIndex].x < 640:  # olha pra esquerda
                            self.check_head()
                    else:
                        if self._hand.search(self._pieceIndex) == self._hand.search(self.check_highest_piece()):
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
        except:
            pass

    # Funcao para checar se o botao do mouse foi pressionado
    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._isPlayer:
            if self.check_click(x, y):
                self._isPieceSelected = True
                print(self.is_bomb())
                print(self._pieceIndex, self._hand.search(self._pieceIndex), self._hand.len())
                '''print(self._domino.head(), self._domino.tail())'''
                self._lastPosition = self._h_sprites[self._pieceIndex].position
            else:
                if pass_button(x, y):
                    self._isPlayer = False
                    self._playerPassed = True
                    self._isBot1 = True
                    self.bot_time()
                self._isPieceSelected = False
                self._lastPosition = None
        else:
            print("Not Your Time")
            self.bot_time()

        print("Bot 1 - " + str(self._bot1.show()), "\n" + "Bot 2 - " + str(self._bot2.show()),
              "\n" + "Bot 3 - " + str(self._bot3.show()), "\n" + "Domino - " + str(self._domino.show()))
        print("Bot 1 Passou - " + str(self._bot1Passed), "\n" + "Bot 2 Passou - " + str(self._bot2Passed),
              "\n" + "Bot 3 Passou - " + str(self._bot3Passed))

    # Funcao que faz a verificacao de cliques (Se esta clicando na peca ou no layer)
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

    # Funcao que verifica se a peca selecionada e compativel com a cabeca do domino
    def check_head(self):
        if self._domino.head().get_value()[self._indiceHead] in self._hand.search(self._pieceIndex).get_value():
            self.place_at_left()
        else:
            self._h_sprites[self._pieceIndex].position = self._lastPosition

    # Funcao que verifica se a peca selecionada e compativel com o tail do domino
    def check_tail(self):
        if self._domino.tail().get_value()[self._indiceTail] in self._hand.search(self._pieceIndex).get_value():
            self.place_at_right()
        else:
            self._h_sprites[self._pieceIndex].position = self._lastPosition

    # Funcao que verifica se a peca selecionada e a maior da mao
    def check_highest_piece(self):
        highest = 0
        aux = -1
        pos = 0
        for i in range(self._hand.len()):
            peca = self._hand.search(i)
            peca_value = peca.get_value()[0] + peca.get_value()[1]
            if peca.get_value()[0] == peca.get_value()[1] and self._domino.len() == 0:
                peca_value += 20
            if peca_value > highest:
                highest = peca_value
                aux += 1
                pos = aux
            else:
                aux += 1
        return pos

    # Funcao que verifica se a peca selecionada e uma bomba
    def is_bomb(self):
        return self._hand.search(self._pieceIndex).get_value()[0] == self._hand.search(self._pieceIndex).get_value()[1]

    # Funcao que inicia a mao do jogador (chamada no __init__)
    def start_hand(self):
        for i in range(7):
            a = self._pool.sort_peca()
            if a.get_value()[0] == a.get_value()[1] and a.get_value()[0] == 6:
                self._isPlayer = True
                self._domino.add(a)
            else:
                self._hand.insert(a)

    # Funcao para inserir o sprite da peca a direita
    def place_at_right(self):
        a = self._h_sprites.pop(self._pieceIndex)
        self._d_sprites.append(a)
        self.throw_right(a)

    # Funcao para inserir o sprite da peca a esquerda
    def place_at_left(self):
        a = self._h_sprites.pop(self._pieceIndex)
        self._d_sprites.insert(0, a)
        self.throw_left(a)

    # Funcao para inserir a peca no struct do domino e posicionar os sprites a esquerda
    def throw_left(self, a):
        peca = self._hand.remove(self._pieceIndex)
        peca.set_previous(None)
        peca.set_next(None)
        if self._domino.head().get_value()[0] is peca.get_value()[0]:
            temp = peca.get_value()[1]
            peca.get_value()[1] = peca.get_value()[0]
            peca.get_value()[0] = temp
            self._domino.insert(peca, 0)
            a.rotation = 0
            a.position = (1280//8) + self._posX, 720 - (720 // 8)
            self._posX += 45
        elif self._domino.head().get_value()[0] is peca.get_value()[1]:
            self._domino.insert(peca, 0)
            a.rotation = 0
            print("de baixo: {}".format((83 // 3)))
            print(a.get_rect())
            a.position = (1280//8) + self._posX, 720 - (720 // 8)
            self._posX += 45

        self._isPlayer = False
        self._playerPassed = False
        self._isBot1 = True
        self.bot_time()
        self.player_winner()

    # Funcao para inserir a peca no struct do domino e posicionar os sprites a direita
    def throw_right(self, a):
        peca = self._hand.remove(self._pieceIndex)
        peca.set_previous(None)
        peca.set_next(None)
        if self._domino.tail().get_value()[1] is peca.get_value()[0]:
            self._domino.append(peca)
            a.rotation = 0
            if len(self._d_sprites) > 1:
                a.position = (1280//8) + self._posY, 720 - (720 // 4)
                self._posY += 45
            else:
                a.position = (1280//8) + self._posY, 720 - (720 // 4)
                self._posY += 45

        elif self._domino.tail().get_value()[1] is peca.get_value()[1]:
            temp = peca.get_value()[1]
            peca.get_value()[1] = peca.get_value()[0]
            peca.get_value()[0] = temp
            self._domino.append(peca)
            a.rotation = 0
            if len(self._d_sprites) > 1:
                a.position = (1280//8) + self._posY, 720 - (720 // 4)
                self._posY += 45

            else:
                a.position = (1280//8) + self._posY, 720 - (720 // 4)
                self._posY += 45

        self._isPlayer = False
        self._playerPassed = False
        self._isBot1 = True
        self.bot_time()
        self.player_winner()

    # Funcao para jogar peca no jogo, chamada quando o player possui a maior peca do jogo
    def throw(self):
        peca = self._hand.remove(self._pieceIndex)
        peca.set_previous(None)
        peca.set_next(None)
        self._domino.append(peca)
        self._isPlayer = False
        self._isBot1 = True
        self.bot_time()

    # Funcao que inicia a mao dos bots
    def start_bots_hand(self):
        for i in range(7):
            a = self._pool.sort_peca()
            if a.get_value()[0] == a.get_value()[1] and a.get_value()[0] == 6:
                peca = a
                peca.sprite().rotation = 0
                peca.sprite().position = (1280 // 2), (720 // 2)
                self._domino.insert(peca, 1)
            else:
                self._bot1.insert(a)

        for i in range(7):
            b = self._pool.sort_peca()
            if b.get_value()[0] == b.get_value()[1] and b.get_value()[0] == 6:
                peca = b
                peca.sprite().rotation = 0
                peca.sprite().position = (1280 // 2), (720 // 2)
                self._domino.insert(peca, 1)
            else:
                self._bot2.insert(b)
        for i in range(7):
            c = self._pool.sort_peca()
            if c.get_value()[0] == c.get_value()[1] and c.get_value()[0] == 6:
                peca = c
                peca.sprite().rotation = 0
                peca.sprite().position = (1280 // 2), (720 // 2)
                self._domino.insert(peca, 1)
            else:
                self._bot3.insert(c)

        self.bot_time()

    # Funcao que coordena a vez dos bots assim como verifica se ele possui a peca a ser jogada
    def bot_time(self):
        if self._isBot1:
            if self._domino.len() != 0:
                for i in range(self._bot1.len()):
                    peca = self._bot1.search(i)
                    if self._domino.head().get_value()[0] in peca.get_value():
                        print("Bot 1 Jogou")
                        self.throw_bot(1, i, 0)
                        self._isBot1 = False
                        self._isBot2 = True
                        self._bot1Passed = False
                        break
                    elif self._domino.tail().get_value()[1] in peca.get_value():
                        print("Bot 1 Jogou")
                        self.throw_bot(1, i, 1)
                        self._isBot1 = False
                        self._bot1Passed = False
                        self._isBot2 = True
                        break
                    else:
                        self._isBot1 = False
                        self._bot1Passed = True
                        self._isBot2 = True
            else:
                for i in range(self._bot1.len()):
                    p = self._bot1.search(i)
                    if p.get_value()[0] == p.get_value()[1] and p.get_value()[0] == 6:
                        print("Comecando a mao bot1" + " " + self._bot1.show())
                        #self.throw_bot(1, i, 0)
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
                    if self._domino.head().get_value()[0] in peca.get_value():
                        print("Bot 2 Jogou")
                        self.throw_bot(2, i, 0)
                        self._isBot2 = False
                        self._bot2Passed = False
                        self._isBot3 = True
                        break
                    elif self._domino.tail().get_value()[1] in peca.get_value():
                        print("Bot 2 Jogou")
                        self.throw_bot(2, i, 1)
                        self._isBot2 = False
                        self._bot2Passed = False
                        self._isBot3 = True
                        break
                    else:
                        self._isBot2 = False
                        self._bot2Passed = True
                        self._isBot3 = True
            else:
                for i in range(self._bot2.len()):
                    p = self._bot2.search(i)
                    if p.get_value()[0] == p.get_value()[1] and p.get_value()[0] == 6:
                        print("Comecando a mao bot2" + " " + self._bot2.show())
                        #self.throw_bot(2, i, 0)
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
                    if self._domino.head().get_value()[0] in peca.get_value():
                        print("Bot 3 Jogou")
                        self.throw_bot(3, i, 0)
                        self._isBot3 = False
                        self._bot3Passed = False
                        self._isPlayer = True
                        break
                    elif self._domino.tail().get_value()[1] in peca.get_value():
                        print("Bot 3 Jogou")
                        self.throw_bot(3, i, 1)
                        self._isBot3 = False
                        self._bot3Passed = False
                        self._isPlayer = True
                        break
                    else:
                        self._isBot3 = False
                        self._bot3Passed = True
                        self._isPlayer = True
            else:
                for i in range(self._bot3.len()):
                    p = self._bot3.search(i)
                    if p.get_value()[0] == p.get_value()[1] and p.get_value()[0] == 6:
                        print("Comecando a mao bot3" + " " + self._bot3.show())
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
        if (self._isBot1 == False and self._isBot2 == False and self._isBot3 == False):
            self._isPlayer = True

        if self._bot1Passed and self._bot2Passed and self._bot3Passed and self._playerPassed and not self._isGameClosed:
            self._isGameClosed = True
            self.count()

    # Funcao de bot que joga a peca selecionada no domino
    def throw_bot(self, bot, index, position):
        if bot == 1:
            if self._domino.len() != 0:
                if position == 0:
                    peca = self._bot1.remove(index)
                    peca.set_previous(None)
                    peca.set_next(None)
                    if self._domino.head().get_value()[0] is peca.get_value()[0]:
                        temp = peca.get_value()[1]
                        peca.get_value()[1] = peca.get_value()[0]
                        peca.get_value()[0] = temp
                        peca.sprite().rotation =  0
                        peca.sprite().position = (1280 // 8) + self._posX, 720 - (720 // 8)
                        self._posX += 45
                        self._domino.insert(peca, 0)
                    elif self._domino.head().get_value()[0] is peca.get_value()[1]:
                        peca.sprite().rotation = 0
                        peca.sprite().position = (1280 // 8) + self._posX, 720 - (720 // 8)
                        self._posX += 45
                        self._domino.insert(peca, 0)
                elif position == 1:
                    peca = self._bot1.remove(index)
                    peca.set_previous(None)
                    peca.set_next(None)
                    if self._domino.tail().get_value()[1] is peca.get_value()[0]:
                        peca.sprite().rotation = 0
                        peca.sprite().position = (1280 // 8) + self._posY, 720 - (720 // 4)
                        self._posY += 45
                        self._domino.append(peca)
                    elif self._domino.tail().get_value()[1] is peca.get_value()[1]:
                        temp = peca.get_value()[1]
                        peca.get_value()[1] = peca.get_value()[0]
                        peca.get_value()[0] = temp
                        peca.sprite().rotation = 0
                        peca.sprite().position = (1280 // 8) + self._posY, 720 - (720 // 4)
                        self._posY += 45
                        self._domino.append(peca)
            else:
                peca = self._bot1.remove(index)
                peca.set_previous(None)
                peca.set_next(None)
                peca.sprite().rotation = 0
                peca.sprite().position = (1280 // 2), (720 // 2)
                self._domino.insert(peca, 1)
        elif bot == 2:
            if self._domino.len() != 0:
                if position == 0:
                    peca = self._bot2.remove(index)
                    peca.set_previous(None)
                    peca.set_next(None)
                    if self._domino.head().get_value()[0] is peca.get_value()[0]:
                        temp = peca.get_value()[1]
                        peca.get_value()[1] = peca.get_value()[0]
                        peca.get_value()[0] = temp
                        peca.sprite().rotation = 0
                        peca.sprite().position = (1280 // 8) + self._posX, 720 - (720 // 8)
                        self._posX += 45
                        self._domino.insert(peca, 0)
                    elif self._domino.head().get_value()[0] is peca.get_value()[1]:
                        peca.sprite().rotation = 0
                        peca.sprite().position = (1280 // 8) + self._posX, 720 - (720 // 8)
                        self._posX += 45
                        self._domino.insert(peca, 0)
                elif position == 1:
                    peca = self._bot2.remove(index)
                    peca.set_previous(None)
                    peca.set_next(None)
                    if self._domino.tail().get_value()[1] is peca.get_value()[0]:
                        peca.sprite().rotation = 0
                        peca.sprite().position = (1280 // 8) + self._posY, 720 - (720 // 4)
                        self._posY += 45
                        self._domino.append(peca)
                    elif self._domino.tail().get_value()[1] is peca.get_value()[1]:
                        temp = peca.get_value()[1]
                        peca.get_value()[1] = peca.get_value()[0]
                        peca.get_value()[0] = temp
                        peca.sprite().rotation = 0
                        peca.sprite().position = (1280 // 8) + self._posY, 720 - (720 // 4)
                        self._posY += 45
                        self._domino.append(peca)
            else:
                peca = self._bot2.remove(index)
                peca.set_previous(None)
                peca.set_next(None)
                peca.sprite().rotation = 0
                peca.sprite().position = (1280 // 2),(720 // 2)
                self._domino.insert(peca, 1)
        elif bot == 3:
            if self._domino.len() != 0:
                if position == 0:
                    peca = self._bot3.remove(index)
                    peca.set_previous(None)
                    peca.set_next(None)
                    if self._domino.head().get_value()[0] is peca.get_value()[0]:
                        temp = peca.get_value()[1]
                        peca.get_value()[1] = peca.get_value()[0]
                        peca.get_value()[0] = temp
                        peca.sprite().rotation = 0
                        peca.sprite().position = (1280 // 8) + self._posX, 720 - (720 // 8)
                        self._posX += 45
                        self._domino.insert(peca, 0)
                    elif self._domino.head().get_value()[0] is peca.get_value()[1]:
                        peca.sprite().rotation = 0
                        peca.sprite().position = (1280 // 8) + self._posX, 720 - (720 // 8)
                        self._posX += 45
                        self._domino.insert(peca, 0)
                elif position == 1:
                    peca = self._bot3.remove(index)
                    peca.set_previous(None)
                    peca.set_next(None)
                    if self._domino.tail().get_value()[1] is peca.get_value()[0]:
                        peca.sprite().rotation = 0
                        peca.sprite().position = (1280 // 8) + self._posY, 720 - (720 // 4)
                        self._posY += 45
                        self._domino.append(peca)
                    elif self._domino.tail().get_value()[1] is peca.get_value()[1]:
                        temp = peca.get_value()[1]
                        peca.get_value()[1] = peca.get_value()[0]
                        peca.get_value()[0] = temp
                        peca.sprite().rotation = 0
                        peca.sprite().position = (1280 // 8) + self._posY, 720 - (720 // 4)
                        self._posY += 45
                        self._domino.append(peca)
            else:
                peca = self._bot3.remove(index)
                peca.set_previous(None)
                peca.set_next(None)
                peca.sprite().rotation = 0
                peca.sprite().position = (1280 // 2), (720 // 2)
                self._domino.insert(peca, 1)
        else:
            raise Exception("Exception, no bot found")

    # Funcao que verifica quem tem a menor contagem de pontos (Chamada quando todos passam a vez)
    def count(self):
        winner = ""
        score = 0
        player_score = 0
        bot1_score = 0
        bot2_score = 0
        bot3_score = 0

        self._label.element.text = "Contagem de Pontos"

        for p in range(self._hand.len()):
            peca = self._hand.search(p)
            player_score += (peca.get_value()[0] + peca.get_value()[1])

            score = player_score
            winner = "voce"

        for i in range(self._bot1.len()):
            peca = self._bot1.search(i)
            bot1_score += (peca.get_value()[0] + peca.get_value()[1])
        if bot1_score < score:
            score = bot1_score
            winner = "Bot 1"

        for i in range(self._bot2.len()):
            peca = self._bot2.search(i)
            bot2_score += (peca.get_value()[0] + peca.get_value()[1])
        if bot2_score < score:
            score = bot2_score
            winner = "Bot 2"

        for i in range(self._bot3.len()):
            peca = self._bot3.search(i)
            bot3_score += (peca.get_value()[0] + peca.get_value()[1])
        if bot3_score < score:
            score = bot3_score
            winner = "Bot 3"

        self._label.element.text = "Pela contagem de pontos o ganhador foi: " + winner
        self._isPlayer = False
        self._isBot1 = False
        self._isBot2 = False
        self._isBot3 = False

    # Funcao que diz que o player venceu
    def player_winner(self):
        if self._hand.len() == 0:
            self._label.element.text = "Voce Venceu, Parabens"
            self._isPlayer = False
            self._isBot1 = False
            self._isBot2 = False
            self._isBot3 = False

    # Funcao que carrega as imagens das pecas dos bots na tela
    def load_parts_on_screen(self):
        array_sprite_bot1 = self._bot1.hand_sprites()
        self.get_sprites(array_sprite_bot1, 150, -125, 50, "y")
        array_sprite_bot2 = self._bot2.hand_sprites()
        self.get_sprites(array_sprite_bot2, -150, 720, 50, "x")
        array_sprite_bot3 = self._bot3.hand_sprites()
        self.get_sprites(array_sprite_bot3, 1280, -125, 50, "y")

    def get_sprites(self, array, pos_x, pos_y, space, orientation):
        if orientation == 'x':
            for i in range(len(array)):
                sprite = array[i]
                sprite.anchor = sprite.get_rect().bottomleft
                sprite.position = (1280 // 2) + pos_x, pos_y
                sprite.scale = 0.45
                self.add(sprite)
                pos_x += space
        else:
            for i in range(len(array)):
                sprite = array[i]
                sprite.anchor = sprite.get_rect().bottomleft
                sprite.rotation = -90
                sprite.position = pos_x, (720 // 2) + pos_y
                sprite.scale = 0.45
                self.add(sprite)
                pos_y += space

        return pos_x
