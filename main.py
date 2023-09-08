import pygame
import random

# Logica do jogo, a bola é redesenhada a cada tick (240 ticks por segundo) ela é desenhada baseada em seus parâmetros  X (horizontal) e Y (Vertical) que são atualizados a cada tick, a cada tick a bola é redesenhada em uma posição diferente, dando a impressão de movimento. Os parâmetros são alterados baseado na Velocidade X e Velocidade Y. Quando a bola colide com um jogador a velocidade X é invertida e a velocidade Y é alterada baseada na posição do jogador, se o jogador estiver no meio a bola vai sair reto, se estiver no canto a bola vai sair em um angulo de 45 graus, se estiver no meio e se movendo para cima a bola vai sair em um angulo de 45 graus para cima, se estiver no meio e se movendo para baixo a bola vai sair em um angulo de 45 graus para baixo (ângulos ilustrativos). Quando a bola colide com a parede a velocidade Y é invertida. Quando a bola colide com a parede esquerda ou direita a pontuação é alterada e a bola é resetada para o meio da tela. Quando a pontuação chega a 5 o jogo acaba e o jogador que chegou a 5 pontos ganha.
#OBS: Vale lembrar que a tela é a todo momento redesenhada, então se você desenhar um retângulo na posição (0, 0) e depois desenhar um retângulo na posição (0, 0) o primeiro retângulo será apagado, por isso é necessário redesenhar a tela a todo momento.

# Inicializa o pygame
pygame.init()

# Cria a tela
tela = pygame.display.set_mode((800, 600))

# Definição de cores
cores = {
    'vermelho': (255, 0, 0),
    'verde': (0, 255, 0),
    'azul': (0, 0, 255),
    'amarelo': (255, 255, 0),
    'roxo': (255, 0, 255),
    'ciano': (0, 255, 255),
    'branco': (255, 255, 255),
    'preto': (0, 0, 0)
}

# Título
pygame.display.set_caption("Pong Pong")

pontuacaoA = 0  # Jogador da esquerda
pontuacaoB = 0  # Jogador da direita

class Bola:
    def __init__(self, x, y, cor, velInicial):
        self.x = x
        self.y = y
        self.movX = velInicial
        self.movX_padrao = velInicial
        self.movY = 0
        self.cor = cor
    
    def mover(self):
        self.x += self.movX
        self.y += self.movY # type: ignore

        if self.x <= 0 or self.x >= 800:
            self.movX *= -1
        if self.y <= 10 or self.y >= 590:
            self.movY *= -1 # type: ignore
    
    def desenhar(self):
        pygame.draw.circle(tela, self.cor, (self.x, self.y), 10)
    
    def colisao(self, jogadorA, jogadorB, maxVel, amplitudeAngulo):
        if self.x <= jogadorA.x + 25 and self.y >= jogadorA.y and self.y <= jogadorA.y + 100:
            if jogadorA.tangivel == True:
                pygame.mixer.music.load(random.choice(['intermediário/PongPong/audios/colisao_jogador1.mp3', 'intermediário/PongPong/audios/colisao_jogador2.mp3', 'intermediário/PongPong/audios/colisao_jogador3.mp3', 'intermediário/PongPong/audios/colisao_jogador4.mp3', 'intermediário/PongPong/audios/colisao_jogador5.mp3', 'intermediário/PongPong/audios/colisao_jogador6.mp3'])) # Escolhe um audio aleatório para tocar
                pygame.mixer.music.play()
                
                # Se a bola bater na parte de baixo ou de cima do jogador verifica se ela está 70% a direita (Valor X segue em frente e o Y inverte) ou 30% a esquerda (Valor X inverte e o Y inverte).
                #OBS: Valor X da bola sempre será negativo pois o jogador 1 está na esquerda.
                if self.x >= jogadorA.x + 10:
                    self.movX *= -1.05 # Aumenta a velocidade horizontal da bola em 5%
                elif self.x < jogadorA.x + 10:
                    self.movX *= 1.05 # Aumenta a velocidade horizontal da bola em 5%
                
                # Define o limite de velocidade horizontal
                if self.movX < 0:
                    if self.movX <= -maxVel:
                        self.movX = -maxVel
                else:
                    if self.movX >= maxVel:
                        self.movX = maxVel
                
                # Tamanho do jogador é 100, então se y=0 o primeiro pixel do jogador é 0 e o último é 100, logo se a bola estiver entre 0 e 100 ela está no jogador, baseado nisso podemos inferir o angulo que a bola vai sair.
                # Podemos adicionar a direção que o jogador está se movendo para que a bola saia em um angulo diferente.
                # Limitando o movimento vertical entre -1.5 e 1.5
                self.movY = min(max((self.y - jogadorA.y - 50) / 50 + jogadorA.mov * 0.3, -amplitudeAngulo), amplitudeAngulo)
                jogadorA.tangivel = not jogador1.tangivel # Inverte o valor tangivel do jogador, para que ele não possa colidir com a bola por 1 tick, isso evita que a bola fique presa no jogador.
                jogadorB.tangivel = not jogador1.tangivel # Inverte o valor tangivel do jogador, garantindo assim que ele possa colidir com a bola.
                
        if self.x >= jogadorB.x - 10 and self.y >= jogadorB.y and self.y <= jogadorB.y + 100:
            if jogadorB.tangivel == True:
                pygame.mixer.music.load(random.choice(['intermediário/PongPong/audios/colisao_jogador1.mp3', 'intermediário/PongPong/audios/colisao_jogador2.mp3', 'intermediário/PongPong/audios/colisao_jogador3.mp3', 'intermediário/PongPong/audios/colisao_jogador4.mp3', 'intermediário/PongPong/audios/colisao_jogador5.mp3', 'intermediário/PongPong/audios/colisao_jogador6.mp3'])) # Escolhe um audio aleatório para tocar
                pygame.mixer.music.play()
                
                # Se a bola bater na parte de baixo ou de cima do jogador verifica se ela está 30% a direita (Valor X segue em frente e o Y inverte) ou 70% a esquerda (Valor X inverte e o Y inverte).
                #OBS: Valor X da bola sempre será positivo pois o jogador 2 está na direita.
                if self.x <= jogadorB.x + 10:
                    self.movX *= -1.05 # Aumenta a velocidade horizontal da bola em 5%
                elif self.x > jogadorB.x + 10:
                    self.movX *= 1.05
                    
                
                # Define o limite de velocidade horizontal
                if self.movX < 0:
                    if self.movX <= -maxVel:
                        self.movX = -maxVel
                else:
                    if self.movX >= maxVel:
                        self.movX = maxVel
                        
                # Tamanho do jogador é 100, então se y=0 o primeiro pixel do jogador é 0 e o último é 100, logo se a bola estiver entre 0 e 100 ela está no jogador, baseado nisso podemos inferir o angulo que a bola vai sair.
                # Podemos adicionar a direção que o jogador está se movendo para que a bola saia em um angulo diferente.
                # Limitando o movimento vertical entre -1.5 e 1.5
                self.movY = min(max((self.y - jogadorB.y - 50) / 50 + jogadorB.mov * 0.3, -amplitudeAngulo), amplitudeAngulo)
                jogadorB.tangivel = not jogadorB.tangivel # Inverte o valor tangivel do jogador, para que ele não possa colidir com a bola por 1 tick, isso evita que a bola fique presa no jogador.
                jogadorA.tangivel = not jogadorB.tangivel # Inverte o valor tangivel do jogador, garantindo assim que ele possa colidir com a bola.
            
    def resetar(self):
        self.x = 400
        self.y = 300
        self.movX = random.choice([-self.movX_padrao, self.movX_padrao])
        self.movY = 0
        pygame.mixer.music.load('intermediário/PongPong/audios/ponto.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        jogador2.tangivel = True
        jogador1.tangivel = True
        jogador1.y = 250
        jogador2.y = 250
        pygame.time.delay(500)
    
    
    def pontuar(self):
        global pontuacaoA
        global pontuacaoB
        if self.x <= 1:
            pontuacaoB += 1
            self.resetar()
            
        if self.x >= 799:
            pontuacaoA += 1
            self.resetar()

class Jogador:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.mov = 0
        self.cor = cor
        self.tangivel = True

    def mover(self):
        self.y += self.mov
        self.y = max(0, min(self.y, 500))  # Garante que a posição y esteja dentro dos limites

    def desenhar(self):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, 20, 100))

class Bot:
    def __init__(self, jogador, bola):
        self.jogador = jogador
        self.bola = bola

    def mover(self, velocidade, angulo):
        if angulo == 50: # Se o angulo for 50, o bot irá se mover para cima ou para baixo baseado na posição da bola, se a bola estiver acima do bot, o bot irá se mover para cima, se a bola estiver abaixo do bot, o bot irá se mover para baixo.
        # O bot consegue controlar o ângulo da bola baseado na posição que a bola bate no jogador, nesse caso o angulo máximo e mínimo que ela vai bater é pequeno.
            if self.jogador.y + random.randint(45, 55) < self.bola.y:
                self.jogador.mov = velocidade
                
            elif self.jogador.y + random.randint(45, 55) > self.bola.y:
                self.jogador.mov = -velocidade
                
            else:
                self.jogador.mov = 0
        elif angulo == 70: # Se o angulo for 70, o bot irá se mover para cima ou para baixo baseado na posição da bola, se a bola estiver acima do bot, o bot irá se mover para cima, se a bola estiver abaixo do bot, o bot irá se mover para baixo.
        # O bot consegue controlar o ângulo da bola baseado na posição que a bola bate no jogador, nesse caso o angulo máximo e mínimo que ela vai bater é grande.
            if self.jogador.y + (random.randint(30, 70)) < self.bola.y:
                self.jogador.mov = velocidade
                
            elif self.jogador.y + (random.randint(30, 70)) > self.bola.y:
                self.jogador.mov = -velocidade
                
            else:
                self.jogador.mov = 0
        elif angulo == 100:
            if self.jogador.y + (random.randint(-20, 120)) < self.bola.y:
                self.jogador.mov = velocidade
                
            elif self.jogador.y + (random.randint(-20, 120)) > self.bola.y:
                self.jogador.mov = -velocidade
                
            else:
                self.jogador.mov = 0

def mostrar_pontuacao():
    fonte = pygame.font.Font('freesansbold.ttf', 32)
    texto = fonte.render(str(pontuacaoA), True, cores['branco'])
    retanguloTexto = texto.get_rect()
    retanguloTexto.center = (200, 50)
    tela.blit(texto, retanguloTexto)
    texto = fonte.render(str(pontuacaoB), True, cores['branco'])
    retanguloTexto = texto.get_rect()
    retanguloTexto.center = (600, 50)
    tela.blit(texto, retanguloTexto)

def verificar_vitoria():
    global pontuacaoA
    global pontuacaoB
    if pontuacaoA == 5:
        pygame.display.update()
        return 1
    if pontuacaoB == 5:
        pygame.display.update()
        return 2
    return 0

relogio = pygame.time.Clock()
jogador1 = Jogador(50, 250, cores['vermelho'])
jogador2 = Jogador(730, 250, cores['azul'])
bola = Bola(400, 300, cores['branco'], 1)
bot1 = Bot(jogador2, bola)
bot2 = Bot(jogador1, bola)
pausado = False

def jogo(qtd_jogadores, velocidade_bot, max_vel, angulo, velocidade_inicial, velocidade_jogador, amplitudeAngulo=1.2):
    global pausado
    rodando = True
    bola.movX = random.choice([velocidade_inicial, -velocidade_inicial])
    bola.movX_padrao = random.choice([velocidade_inicial, -velocidade_inicial])
    while rodando:
        # Limita a taxa de atualização da tela
        relogio.tick(240)

        # Definição de cores de fundo
        tela.fill(cores['preto'])   

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pausado = True
                    font = pygame.font.Font('freesansbold.ttf', 32)
                    texto = font.render("Jogo pausado", True, cores['branco'])
                    retanguloTexto = texto.get_rect()
                    retanguloTexto.center = (400, 300)
                    tela.blit(texto, retanguloTexto)
                    
                    pygame.draw.rect(tela, cores['ciano'], (350, 375, 100, 50))
                    texto = font.render("Sair", True, cores['branco'])
                    retanguloTexto = texto.get_rect()
                    retanguloTexto.center = (400, 400)
                    tela.blit(texto, retanguloTexto)
                    
                    pygame.display.update()
                    while pausado:
                        for evento in pygame.event.get():
                            if evento.type == pygame.QUIT:
                                pausado = False
                                rodando = False
                            if evento.type == pygame.KEYDOWN:
                                if evento.key == pygame.K_ESCAPE:
                                    pausado = False
                                    rodando = True
                                    break
                            if evento.type == pygame.MOUSEBUTTONDOWN:
                                # Se o botão esquerdo do mouse for clicado e tiver na posição (350, 375) até (450, 425) ou seja, se o botão "Sair" for clicado
                                if evento.button == 1 and 350 < evento.pos[0] < 450 and 375 < evento.pos[1] < 425:
                                    pausado = False
                                    pygame.time.delay(200)
                                    tela_inicial()
                                    break
            if qtd_jogadores == 1:
                if evento.type == pygame.KEYDOWN: # Se alguma tecla for pressionada
                    if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                        jogador1.mov = -velocidade_jogador
                    if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                        jogador1.mov = velocidade_jogador

                        
                if evento.type == pygame.KEYUP: # Se alguma tecla for solta
                    if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                        jogador1.mov = 0
                    if evento.key == pygame.K_w or evento.key == pygame.K_s:
                        jogador1.mov = 0
                        
            elif qtd_jogadores == 2:
                if evento.type == pygame.KEYDOWN: # Se alguma tecla for pressionada
                    if evento.key == pygame.K_UP:
                        jogador2.mov = -velocidade_jogador
                    if evento.key == pygame.K_DOWN:
                        jogador2.mov = velocidade_jogador
                    if evento.key == pygame.K_w:
                        jogador1.mov = -velocidade_jogador
                    if evento.key == pygame.K_s:
                        jogador1.mov = velocidade_jogador

                        
                if evento.type == pygame.KEYUP: # Se alguma tecla for solta
                    if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                        jogador2.mov = 0
                    if evento.key == pygame.K_w or evento.key == pygame.K_s:
                        jogador1.mov = 0
                
        # Move a bola
        bola.mover()
        
        # Move os jogadores
        jogador1.mover()
        jogador2.mover()
        if qtd_jogadores == 1:
            bot1.mover(velocidade_bot, angulo)
            #bot2. mover(velocidade_bot, angulo)
            
        if qtd_jogadores == 0:
            bot1.mover(velocidade_bot, angulo)
            bot2. mover(velocidade_bot, angulo)

            
        
        # Desenha a bola
        bola.desenhar()
        
        # Desenha os jogadores
        jogador1.desenhar()
        jogador2.desenhar()

        # Desenha a pontuação
        mostrar_pontuacao()
        
        # Verifica a colisão
        bola.colisao(jogador1, jogador2, max_vel, amplitudeAngulo)
        
        # Verifica a pontuação
        bola.pontuar()
        
        # Verifica se alguém ganhou
        vitoria = verificar_vitoria() 
        # Se vitoria == 1, jogador 1 ganhou, 
        # se vitoria == 2, jogador 2 ganhou

        if vitoria == 1:
            fonte = pygame.font.Font('freesansbold.ttf', 32)
            texto = fonte.render("Jogador 1 ganhou!", True, cores['branco'])
            retanguloTexto = texto.get_rect()
            retanguloTexto.center = (400, 300)
            tela.blit(texto, retanguloTexto)
            pygame.display.update()
            pygame.time.delay(2000)
            exit()
            
        elif vitoria == 2:
            fonte = pygame.font.Font('freesansbold.ttf', 32)
            if qtd_jogadores == 1:
                texto = fonte.render("Bot ganhou!", True, cores['branco'])
            else:
                texto = fonte.render("Jogador 2 ganhou!", True, cores['branco'])
            retanguloTexto = texto.get_rect()
            retanguloTexto.center = (400, 300)
            tela.blit(texto, retanguloTexto)
            pygame.display.update()
            pygame.time.delay(2000)
            exit()
        
        # Atualiza a tela
        pygame.display.update()

def tela_velocidade_bola(qtdJogadores):
    rodando = True
    while rodando:
        # Limita a taxa de atualização da tela
        relogio.tick(240)

        # Definição de cores de fundo
        tela.fill(cores['preto'])
            
        # Irá aparecer um título "Escolha a velocidade da bola" e irá aparecer um campo de texto para o usuário digitar a velocidade da bola, a velocidade da bola é um número entre 0.5 e 5, se o usuário digitar um número fora desse intervalo, o jogo irá pedir para ele digitar novamente.
        
        fonte = pygame.font.Font('freesansbold.ttf', 32)
        texto = fonte.render("Escolha a velocidade da bola (1 é o padrão)", True, cores['branco'])
        retanguloTexto = texto.get_rect()
        retanguloTexto.center = (400, 100)
        tela.blit(texto, retanguloTexto)
        
        def desenhar_botao(texto, x, y, largura, altura, cor, cor_hover):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if x < mouse[0] < x + largura and y < mouse[1] < y + altura:
                pygame.draw.rect(tela, cor_hover, (x, y, largura, altura))
                if click[0] == 1:
                    return True
            else:
                pygame.draw.rect(tela, cor, (x, y, largura, altura))
                
            # Desenha o texto do botão
            texto_botao = fonte.render(texto, True, cores['preto'])
            retanguloTexto = texto_botao.get_rect()
            retanguloTexto.center = (x + largura / 2, y + altura / 2)
            tela.blit(texto_botao, retanguloTexto)
            return False
        
        if qtdJogadores == 0:
            if desenhar_botao("Velocidade 1", 250, 250, 250, 50, cores['branco'], cores['ciano']):
                jogo(qtdJogadores, 0.89, 5, 70, 1.25, 1)
                rodando = False
            
            if desenhar_botao("Velocidade 2", 250, 350, 250, 50, cores['branco'], cores['ciano']):
                jogo(qtdJogadores, 1, 7, 100, 1.75, 1.25)
                rodando = False
            
            if desenhar_botao("Velocidade 3", 250, 450, 250, 50, cores['branco'], cores['ciano']):
                jogo(qtdJogadores, 3, 15, 100, 5, 1.5, 5)
                rodando = False

        elif qtdJogadores == 2:
            if desenhar_botao("Velocidade 1", 250, 250, 250, 50, cores['branco'], cores['ciano']):
                jogo(qtdJogadores, 1, 3, 50, 1.25, 1)
                rodando = False
            
            if desenhar_botao("Velocidade 2", 250, 350, 250, 50, cores['branco'], cores['ciano']):
                jogo(qtdJogadores, 1, 5, 50, 1.75, 1.25)
                rodando = False
            
            if desenhar_botao("Velocidade 3", 250, 450, 250, 50, cores['branco'], cores['ciano']):
                jogo(qtdJogadores, 1, 7, 50, 2.5, 1.5)
                rodando = False
                
        if desenhar_botao("Voltar", 600, 500, 150, 50, cores['branco'], cores['ciano']):
            tela_inicial()
            rodando = False
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
        
        pygame.display.update()
        
def tela_dificuldade_bot():
    rodando = True
    while rodando:
        # Limita a taxa de atualização da tela
        relogio.tick(240)

        # Definição de cores de fundo
        tela.fill(cores['preto'])
            
        # Irá aparecer um título "Escolha a dificuldade" e irá aparecer 3 dificuldades: fácil, médio e impossível,
        # cada uma irá retornar a função "jogo" com 1 jogador e uma velocidadeBot diferente: 0.5, 0.8 e 0.85 respectivamente.
        fonte = pygame.font.Font('freesansbold.ttf', 32)
        texto = fonte.render("Escolha a dificuldade", True, cores['branco'])
        retanguloTexto = texto.get_rect()
        retanguloTexto.center = (400, 100)
        tela.blit(texto, retanguloTexto)

        def desenhar_botao(texto, x, y, largura, altura, cor, cor_hover):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if x < mouse[0] < x + largura and y < mouse[1] < y + altura:
                pygame.draw.rect(tela, cor_hover, (x, y, largura, altura))
                if click[0] == 1:
                    return True
            else:
                pygame.draw.rect(tela, cor, (x, y, largura, altura))
                
            # Desenha o texto do botão
            texto_botao = fonte.render(texto, True, cores['preto'])
            retanguloTexto = texto_botao.get_rect()
            retanguloTexto.center = (x + largura / 2, y + altura / 2)
            tela.blit(texto_botao, retanguloTexto)
            return False
        
        if desenhar_botao("Fácil", 300, 250, 200, 50, cores['branco'], cores['ciano']): # Se o botão for clicado, a função jogo será chamada com os parâmetros: 1 jogador, velocidadeBot = 0.5, maxVel = 2 e angulo = 50
            jogo(1, 0.75, 2, 50, 1.25, 1)
            rodando = False

        if desenhar_botao("Médio", 300, 350, 200, 50, cores['branco'], cores['ciano']): # Se o botão for clicado, a função jogo será chamada com os parâmetros: 1 jogador, velocidadeBot = 0.75, maxVel = 4 e angulo = 50
            jogo(1, 0.9, 3, 70, 1.75, 1)
            rodando = False

        if desenhar_botao("Impossível", 300, 450, 200, 50, cores['branco'], cores['ciano']): # Se o botão for clicado, a função jogo será chamada com os parâmetros: 1 jogador, velocidadeBot = 0.85, maxVel = 5 e angulo = 100
            jogo(1, 1.5, 5, 100, 2, 1.25)
            rodando = False
            
        if desenhar_botao("Voltar", 600, 500, 150, 50, cores['branco'], cores['ciano']):
            tela_inicial()
            rodando = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        pygame.display.update()

def tela_inicial():
    rodando = True
    while rodando:
        # Limita a taxa de atualização da tela
        relogio.tick(240)

        # Definição de cores de fundo
        tela.fill(cores['preto'])
        
        # Irá aparecer um título "Ping Pong" e os botões "Bot VS Bot", "1 Jogador", "2 Jogadores" e "Sair"
        fonte = pygame.font.Font('freesansbold.ttf', 32)
        texto = fonte.render("Ping Pong", True, cores['branco'])
        retanguloTexto = texto.get_rect()
        retanguloTexto.center = (400, 100)
        tela.blit(texto, retanguloTexto)

        def desenhar_botao(texto, x, y, largura, altura, cor, cor_hover):
            mouse = pygame.mouse.get_pos() # Pega a posição do mouse
            click = pygame.mouse.get_pressed() # Pega o clique do mouse

            if x < mouse[0] < x + largura and y < mouse[1] < y + altura: # Se o mouse estiver dentro do botão
                pygame.draw.rect(tela, cor_hover, (x, y, largura, altura))
                if click[0] == 1: # Se o botão esquerdo do mouse for clicado
                    return True
            else:
                pygame.draw.rect(tela, cor, (x, y, largura, altura))

            # Desenha o texto do botão
            texto_botao = fonte.render(texto, True, cores['preto'])
            retanguloTexto = texto_botao.get_rect()
            retanguloTexto.center = (x + largura / 2, y + altura / 2)
            tela.blit(texto_botao, retanguloTexto)
            return False
        
        if desenhar_botao("Bot VS Bot", 300, 200, 200, 50, cores['branco'], cores['ciano']):
            tela_velocidade_bola(0)
            rodando = False # Anti bug
        
        if desenhar_botao("1 Jogador", 300, 300, 200, 50, cores['branco'], cores['ciano']):
            tela_dificuldade_bot()
            rodando = False # Anti bug

        if desenhar_botao("2 Jogadores", 300, 400, 200, 50, cores['branco'], cores['ciano']):
            tela_velocidade_bola(2)
            rodando = False # Anti bug
        
        if desenhar_botao("Sair", 300, 500, 200, 50, cores['branco'], cores['ciano']):
            exit()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False # Anti bug

        pygame.display.update()

if __name__ == "__main__":
    tela_inicial()