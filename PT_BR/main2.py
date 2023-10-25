import random
import pygame
import math

pygame.init()

Colors = {'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0), 'blue': (0, 0, 255)}

font = 'Verdana'

height = 600
width = 800
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Pong game')

clock = pygame.time.Clock()
FPS = 240


class Ball:
    def __init__(self):
        self.x = width / 2
        self.y = height / 2
        self.radius = 10
        self.color = Colors['white']
        self.speed_x = 2 * random.choice((1, -1))
        self.speed_y = 0
        self.is_moving = True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        if self.is_moving:
            self.x += self.speed_x
            self.y += self.speed_y

    def wallCollision(self):
        if self.is_moving and self.y <= self.radius or self.y >= height - self.radius:
            self.speed_y *= -1

    def playerCollisionResponse(self, player):
        self.speed_x = min(5, -1.1 * self.speed_x)
        self.speed_y = min(max((self.y - player.y - 50) / 50 + player.speed * 0.3, -2), 2)
        if player.y == self.y - 50:
            self.speed_y = 0

    def playerCollision(self, players):
        player1 = players[0]
        player2 = players[1]
        p1_rect = pygame.Rect(player1.x, player1.y, player1.width, player1.height)
        p2_rect = pygame.Rect(player2.x, player2.y, player2.width, player2.height)
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

        if ball_rect.colliderect(p1_rect) and player1.tangible:
            self.playerCollisionResponse(player1)

            player1.tangible = not player1.tangible
            player2.tangible = not player1.tangible

        if ball_rect.colliderect(p2_rect) and player2.tangible:
            self.playerCollisionResponse(player2)

            player2.tangible = not player2.tangible
            player1.tangible = not player2.tangible

    def reset(self):
        self.is_moving = True
        self.x = width / 2
        self.y = height / 2
        self.speed_x = 2 * random.choice((1, -1))
        self.speed_y = 0


class Player:
    def __init__(self, is_ai, is_left=False, difficulty=0):
        self.x = 30 if is_left else width - 40
        self.y = (height / 2) - 50
        self.width = 15
        self.height = 100
        self.speed = 2
        self.score = 0
        self.tangible = True
        self.is_ai = is_ai
        self.is_left = is_left
        self.difficulty = difficulty

    def draw(self, screen):
        pygame.draw.rect(screen, Colors['red'] if self.is_left else Colors['blue'], (self.x, self.y, self.width, self.height))

    def move(self, keys, ball):
        if self.is_ai:
            angulo_A = 0
            angulo_B = 0
            if self.difficulty == 1:
                angulo_A += 35
                angulo_B += 65
            elif self.difficulty == 2:
                angulo_A += 20
                angulo_B += 70
            elif self.difficulty == 3:
                angulo_A += 0
                angulo_B += 100

            if ball.is_moving:
                if self.y + random.randint(angulo_A, angulo_B) > ball.y and self.y > 0:
                    self.speed = -1.5
                    self.y += self.speed
                elif self.y + random.randint(angulo_A, angulo_B) < ball.y and self.y < height - self.height:
                    self.speed = 1.5
                    self.y += self.speed
        elif self.is_left:
            if keys[pygame.K_w] and self.y > 0:
                self.speed = -1.5
                self.y += self.speed
            if keys[pygame.K_s] and self.y < height - self.height:
                self.speed = 1.5
                self.y += self.speed
        else:
            if keys[pygame.K_UP] and self.y > 0:
                self.speed = -1.5
                self.y += self.speed
            if keys[pygame.K_DOWN] and self.y < height - self.height:
                self.speed = 1.5
                self.y += self.speed

    def scorePoint(self, ball):
        self.score += 1
        ball.reset()

    def reset(self):
        self.x = 30 if self.is_left else width - 40
        self.y = (height / 2) - 50
        self.tangible = True


class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]  # Player1 = left, Player2 = right
        self.ball = Ball()
        self.font = pygame.font.SysFont(font, 40)

    def draw(self, screen):
        self.ball.draw(screen)
        for player in self.players:
            player.draw(screen)

        score_text = self.font.render(f'{self.players[0].score}                 x                 {self.players[1].score}', True, Colors['white'])
        screen.blit(score_text, (width / 2 - score_text.get_width() / 2, 10))

    def update(self):
        for player in self.players:
            player.move(pygame.key.get_pressed(), self.ball)
        self.ball.playerCollision(self.players)
        self.ball.move()
        self.ball.wallCollision()
        if self.checkScore() == 1:
            self.reset()

    def checkScore(self):
        if self.ball.x <= 0:
            self.players[1].scorePoint(self.ball)
            for i in range(3, 0, -1):
                counter_text = self.font.render(f'{i}', True, Colors['white'])
                screen.blit(counter_text, (width / 2 - counter_text.get_width() / 2, height - 50))
                pygame.display.update()
                pygame.time.wait(500)

                cleaner = pygame.Surface((counter_text.get_width(), counter_text.get_height()))
                cleaner.fill(Colors['black'])
                screen.blit(cleaner, (width / 2 - counter_text.get_width() / 2, height - 50))
                pygame.display.update()
            return 1
        elif self.ball.x >= width:
            self.players[0].scorePoint(self.ball)
            for i in range(3, 0, -1):
                counter_text = self.font.render(f'{i}', True, Colors['white'])
                screen.blit(counter_text, (width / 2 - counter_text.get_width() / 2, height - 50))
                pygame.display.update()
                pygame.time.wait(500)

                cleaner = pygame.Surface((counter_text.get_width(), counter_text.get_height()))
                cleaner.fill(Colors['black'])
                screen.blit(cleaner, (width / 2 - counter_text.get_width() / 2, height - 50))
                pygame.display.update()
            return 1

    def reset(self):
        self.ball.reset()
        for player in self.players:
            player.reset()

    def deleteAll(self):
        self.players = []
        self.ball = None

    def checkGameOver(self):
        for player in self.players:
            if player.score >= 5:
                return player.is_left

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            screen.fill(Colors['black'])
            self.draw(screen)
            self.update()
            if self.checkGameOver():
                screen.fill(Colors['black'])
                winner_text = self.font.render(f'Player 1 venceu!', True, Colors['white'])
                screen.blit(winner_text, (width / 2 - winner_text.get_width() / 2, height / 2 - winner_text.get_height() / 2))
                pygame.display.update()
                pygame.time.wait(1500)

                main_menu(restart=True)
                exit()

            elif self.checkGameOver() == False:
                screen.fill(Colors['black'])
                winner_text = self.font.render(f'Player 2 venceu!', True, Colors['white'])
                screen.blit(winner_text, (width / 2 - winner_text.get_width() / 2, height / 2 - winner_text.get_height() / 2))
                pygame.display.update()
                pygame.time.wait(1500)
                self.deleteAll()
                main_menu(restart=True)
                exit()
            pygame.display.update()
            clock.tick(240)


class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.color = color
        self.text_color = text_color
        self.font = font
        self.font_size = font_size
        self.color_hover = '#708090'

    def draw(self, screen):
        mousePos = pygame.mouse.get_pos()
        if self.isOver(mousePos):
            pygame.draw.rect(screen, self.color_hover, (self.x, self.y, self.width, self.height))
            text = pygame.font.SysFont(self.font, self.font_size).render(self.text, True, self.text_color)
            screen.blit(text, ( self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 2 - text.get_height() / 2))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            text = pygame.font.SysFont(self.font, self.font_size).render(self.text, True, self.text_color)
            screen.blit(text, (self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 2 - text.get_height() / 2))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


def main_menu(restart=False):
    run = True
    while run:
        screen.fill(Colors['black'])
        title_text = pygame.font.SysFont(font, 60).render('Pong game', True, Colors['white'])
        screen.blit(title_text, (width / 2 - title_text.get_width() / 2, 50))
        dois_players = Button(width / 2 - 150, 200, 300, 50, '2 jogadores', Colors['white'], Colors['black'], 36)
        um_player = Button(width / 2 - 150, 300, 300, 50, '1 jogador', Colors['white'], Colors['black'], 36)
        bot_bot = Button(width / 2 - 150, 400, 300, 50, 'Bot vs Bot', Colors['white'], Colors['black'], 36)
        sair = Button(width - 185, 515, 150, 50, 'Sair', Colors['white'], Colors['black'], 36)
        dois_players.draw(screen)
        um_player.draw(screen)
        bot_bot.draw(screen)
        sair.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if um_player.isOver(pos):
                    tela_dificuldade()
                elif dois_players.isOver(pos):
                    ball = Ball()
                    player1 = Player(is_ai=False, is_left=True)
                    player2 = Player(is_ai=False)
                    game1 = Game(player1, player2)
                    game1.run()
                elif bot_bot.isOver(pos):
                    ball = Ball()
                    bot1 = Player(is_ai=True, difficulty=3, is_left=True)
                    bot2 = Player(is_ai=True, difficulty=3)
                    game2 = Game(bot1, bot2)
                    game2.run()
                elif sair.isOver(pos):
                    run = False


def tela_dificuldade():
    run = True
    while run:
        screen.fill(Colors['black'])
        title_text = pygame.font.SysFont(font, 60).render('Pong game', True, Colors['white'])
        screen.blit(title_text, (width / 2 - title_text.get_width() / 2, 50))
        facil = Button(width / 2 - 150, 200, 300, 50, 'Fácil', Colors['white'], Colors['black'], 36)
        medio = Button(width / 2 - 150, 300, 300, 50, 'Médio', Colors['white'], Colors['black'], 36)
        dificil = Button(width / 2 - 150, 400, 300, 50, 'Difícil', Colors['white'], Colors['black'], 36)
        voltar = Button(width - 185, 515, 150, 50, 'Voltar', Colors['white'], Colors['black'], 36)
        facil.draw(screen)
        medio.draw(screen)
        dificil.draw(screen)
        voltar.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if facil.isOver(pos):
                    ball = Ball()
                    player1 = Player(is_ai=False, is_left=True)
                    bot1 = Player(is_ai=True, difficulty=1)
                    game3 = Game(player1, bot1)
                    game3.run()
                elif medio.isOver(pos):
                    ball = Ball()
                    player1 = Player(is_ai=False, is_left=True)
                    bot2 = Player(is_ai=True, difficulty=2)
                    game4 = Game(player1, bot2)
                    game4.run()
                elif dificil.isOver(pos):
                    ball = Ball()
                    player1 = Player(is_ai=False, is_left=True)
                    bot3 = Player(is_ai=True, difficulty=3)
                    game5 = Game(player1, bot3)
                    game5.run()
                elif voltar.isOver(pos):
                    run = False
                    main_menu()


if __name__ == '__main__':
    main_menu()
