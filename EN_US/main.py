import pygame
import random

# Game logic: the ball is redrawn every tick (240 ticks per second). It is drawn based on its X (horizontal) and Y (vertical) parameters, which are updated every tick. Each tick, the ball is redrawn in a different position, giving the impression of movement. The parameters are changed based on the X and Y velocities. When the ball collides with a player, the X velocity is inverted, and the Y velocity is adjusted based on the player's position. If the player is in the middle, the ball will go straight; if in the corner, it will bounce at a 45-degree angle. If the player is in the middle and moving up, the ball will bounce at a 45-degree angle upwards; if moving down, it will bounce at a 45-degree angle downwards (illustrative angles). When the ball collides with the wall, the Y velocity is inverted. When the ball collides with the left or right wall, the score is changed, and the ball is reset to the middle of the screen. When the score reaches 5, the game ends, and the player with 5 points wins.
# Note: It's worth mentioning that the screen is constantly redrawn. So if you draw a rectangle at position (0, 0) and then draw another rectangle at the same position, the first rectangle will be erased. Therefore, it's necessary to redraw the screen at all times.

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Color definitions
colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'purple': (255, 0, 255),
    'cyan': (0, 255, 255),
    'white': (255, 255, 255),
    'black': (0, 0, 0)
}

# Title
pygame.display.set_caption("Pong Pong")

scoreA = 0  # Left player
scoreB = 0  # Right player

class Ball:
    def __init__(self, x, y, color, initialVel):
        self.x = x
        self.y = y
        self.moveX = initialVel
        self.defaultMoveX = initialVel
        self.moveY = 0
        self.color = color
    
    def move(self):
        self.x += self.moveX
        self.y += self.moveY # type: ignore

        if self.x <= 0 or self.x >= 800:
            self.moveX *= -1
        if self.y <= 10 or self.y >= 590:
            self.moveY *= -1 # type: ignore
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)
    
    def collision(self, playerA, playerB, maxVel, angleAmplitude):
        if self.x <= playerA.x + 25 and self.y >= playerA.y and self.y <= playerA.y + 100:
            if playerA.tangible == True:
                pygame.mixer.music.load(random.choice(['EN_US/sounds/collision_player1.mp3', 'EN_US/sounds/collision_player2.mp3', 'EN_US/sounds/collision_player3.mp3', 'EN_US/sounds/collision_player4.mp3', 'EN_US/sounds/collision_player5.mp3', 'EN_US/sounds/collision_player6.mp3'])) # Chooses a random sounds to play
                pygame.mixer.music.play()
                
                # If the ball hits the bottom or top of the player, it checks if it's 70% to the right (X value goes forward and Y inverts) or 30% to the left (X value inverts and Y inverts).
                # Note: The X value of the ball will always be negative because player 1 is on the left.
                if self.x >= playerA.x + 10:
                    self.moveX *= -1.05 # Increases the horizontal speed of the ball by 5%
                elif self.x < playerA.x + 10:
                    self.moveX *= 1.05 # Increases the horizontal speed of the ball by 5%
                
                # Sets the limit for horizontal speed
                if self.moveX < 0:
                    if self.moveX <= -maxVel:
                        self.moveX = -maxVel
                else:
                    if self.moveX >= maxVel:
                        self.moveX = maxVel
                
                # Player size is 100, so if y=0, the first pixel of the player is 0 and the last one is 100. Therefore, if the ball is between 0 and 100, it's on the player. Based on this, we can infer the angle the ball will bounce.
                # We can add the direction the player is moving so the ball bounces at a different angle.
                # Limiting vertical movement between -1.5 and 1.5
                self.moveY = min(max((self.y - playerA.y - 50) / 50 + playerA.move * 0.3, -angleAmplitude), angleAmplitude)
                playerA.tangible = not player1.tangible # Inverts the tangible value of the player, so it cannot collide with the ball for 1 tick, preventing the ball from getting stuck to the player.
                playerB.tangible = not player1.tangible # Inverts the tangible value of the player, ensuring that it can collide with the ball.
                
        if self.x >= playerB.x - 10 and self.y >= playerB.y and self.y <= playerB.y + 100:
            if playerB.tangible == True:
                pygame.mixer.music.load(random.choice(['EN_US/sounds/collision_player1.mp3', 'EN_US/sounds/collision_player2.mp3', 'EN_US/sounds/collision_player3.mp3', 'EN_US/sounds/collision_player4.mp3', 'EN_US/sounds/collision_player5.mp3', 'EN_US/sounds/collision_player6.mp3'])) # Chooses a random sounds to play
                pygame.mixer.music.play()
                
                # If the ball hits the bottom or top of the player, it checks if it's 30% to the right (X value goes forward and Y inverts) or 70% to the left (X value inverts and Y inverts).
                # Note: The X value of the ball will always be positive because player 2 is on the right.
                if self.x <= playerB.x + 10:
                    self.moveX *= -1.05 # Increases the horizontal speed of the ball by 5%
                elif self.x > playerB.x + 10:
                    self.moveX *= 1.05
                    
                # Sets the limit for horizontal speed
                if self.moveX < 0:
                    if self.moveX <= -maxVel:
                        self.moveX = -maxVel
                else:
                    if self.moveX >= maxVel:
                        self.moveX = maxVel
                        
                # Player size is 100, so if y=0 the first player pixel is 0 and the last one is 100, so if the ball is between 0 and 100 it's on the player, based on this we can infer the angle the ball will exit.
                # We can add the direction the player is moving so the ball exits at a different angle.
                # Limiting vertical movement between -1.5 and 1.5
                self.moveY = min(max((self.y - playerB.y - 50) / 50 + playerB.move * 0.3, -angleAmplitude), angleAmplitude)
                playerB.tangible = not playerB.tangible # Inverts the player's tangible value, so it can't collide with the ball for 1 tick, this prevents the ball from getting stuck on the player.
                playerA.tangible = not playerB.tangible # Inverts the player's tangible value, ensuring it can collide with the ball.

    def reset(self):
        self.x = 400
        self.y = 300
        self.moveX = random.choice([-self.defaultMoveX, self.defaultMoveX])
        self.moveY = 0
        pygame.mixer.music.load('EN_US/sounds/point.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        player2.tangible = True
        player1.tangible = True
        player1.y = 250
        player2.y = 250
        pygame.time.delay(500)

    def score(self):
        global scoreA
        global scoreB
        if self.x <= 1:
            scoreB += 1
            self.reset()
            
        if self.x >= 799:
            scoreA += 1
            self.reset()

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.move = 0
        self.color = color
        self.tangible = True

    def move_player(self):
        self.y += self.move
        self.y = max(0, min(self.y, 500))  # Ensures that the y position is within bounds

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 20, 100))

class Bot:
    def __init__(self, player, ball):
        self.player = player
        self.ball = ball

    def move(self, speed, angle):
        if angle == 50: # If the angle is 50, the bot will move up or down based on the ball's position, if the ball is above the bot, it will move up, if the ball is below the bot, it will move down.
        # The bot can control the angle of the ball based on where the ball hits the player, in this case, the maximum and minimum angle it will hit is small.
            if self.player.y + random.randint(45, 55) < self.ball.y:
                self.player.move = speed
                
            elif self.player.y + random.randint(45, 55) > self.ball.y:
                self.player.move = -speed
                
            else:
                self.player.move = 0
        elif angle == 70: # If the angle is 70, the bot will move up or down based on the ball's position, if the ball is above the bot, it will move up, if the ball is below the bot, it will move down.
        # The bot can control the angle of the ball based on where the ball hits the player, in this case, the maximum and minimum angle it will hit is large.
            if self.player.y + (random.randint(30, 70)) < self.ball.y:
                self.player.move = speed
                
            elif self.player.y + (random.randint(30, 70)) > self.ball.y:
                self.player.move = -speed
                
            else:
                self.player.move = 0
        elif angle == 100:
            if self.player.y + (random.randint(-20, 120)) < self.ball.y:
                self.player.move = speed
                
            elif self.player.y + (random.randint(-20, 120)) > self.ball.y:
                self.player.move = -speed
                
            else:
                self.player.move = 0

def show_score():
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(scoreA), True, colors['white'])
    textRect = text.get_rect()
    textRect.center = (200, 50)
    screen.blit(text, textRect)
    text = font.render(str(scoreB), True, colors['white'])
    textRect = text.get_rect()
    textRect.center = (600, 50)
    screen.blit(text, textRect)

def check_victory():
    global scoreA
    global scoreB
    if scoreA == 5:
        pygame.display.update()
        return 1
    if scoreB == 5:
        pygame.display.update()
        return 2
    return 0

def reset_all():
    global scoreA
    global scoreB
    scoreA = 0
    scoreB = 0
    player1.y = 250
    player2.y = 250
    player1.tangible = True
    player2.tangible = True
    ball.reset()

clock = pygame.time.Clock()
player1 = Player(50, 250, colors['red'])
player2 = Player(730, 250, colors['blue'])
ball = Ball(400, 300, colors['white'], 1)
bot1 = Bot(player2, ball)
bot2 = Bot(player1, ball)
paused = False

def game(num_players, bot_speed, max_speed, angle, initial_speed, player_speed, angle_amplitude=1.2):
    global paused
    running = True
    ball.moveX = random.choice([initial_speed, -initial_speed])
    ball.default_moveX = random.choice([initial_speed, -initial_speed])
    while running:
        # Limits the screen update rate
        clock.tick(240)

        # Set background colors
        screen.fill(colors['black'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                    font = pygame.font.Font('freesansbold.ttf', 32)
                    text = font.render("Game paused", True, colors['white'])
                    text_rect = text.get_rect()
                    text_rect.center = (400, 300)
                    screen.blit(text, text_rect)
                    
                    pygame.draw.rect(screen, colors['cyan'], (350, 375, 100, 50))
                    text = font.render("Quit", True, colors['white'])
                    text_rect = text.get_rect()
                    text_rect.center = (400, 400)
                    screen.blit(text, text_rect)
                    
                    pygame.display.update()
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                paused = False
                                running = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    paused = False
                                    running = True
                                    break
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # If the left mouse button is clicked and it's in the position (350, 375) to (450, 425), i.e., if the "Quit" button is clicked
                                if event.button == 1 and 350 < event.pos[0] < 450 and 375 < event.pos[1] < 425:
                                    paused = False
                                    pygame.time.delay(200)
                                    reset_all()
                                    initial_screen()
                                    break
            if num_players == 1:
                if event.type == pygame.KEYDOWN: # If any key is pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player1.move = -player_speed
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        player1.move = player_speed

                        
                if event.type == pygame.KEYUP: # If any key is released
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player1.move = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player1.move = 0
                        
            elif num_players == 2:
                if event.type == pygame.KEYDOWN: # If any key is pressed
                    if event.key == pygame.K_UP:
                        player2.move = -player_speed
                    if event.key == pygame.K_DOWN:
                        player2.move = player_speed
                    if event.key == pygame.K_w:
                        player1.move = -player_speed
                    if event.key == pygame.K_s:
                        player1.move = player_speed

                        
                if event.type == pygame.KEYUP: # If any key is released
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player2.move = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player1.move = 0
                
        # Move the ball
        ball.move()
        
        # Move the players
        player1.move_player()
        player2.move_player()
        if num_players == 1:
            bot1.move(bot_speed, angle)

        if num_players == 0:
            bot1.move(bot_speed, angle)
            bot2.move(bot_speed, angle)


        # Draw the ball
        ball.draw()

        # Draw the players
        player1.draw()
        player2.draw()

        # Draw the score
        show_score()

        # Check for collision
        ball.collision(player1, player2, max_speed, angle_amplitude)

        # Check for scoring
        ball.score()

        # Check if anyone won
        victory = check_victory() 
        # If victory == 1, player 1 won,
        # if victory == 2, player 2 won

        if victory == 1:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render("Player 1 won!", True, colors['white'])
            text_rect = text.get_rect()
            text_rect.center = (400, 300)
            screen.blit(text, text_rect)
            pygame.display.update()
            pygame.time.delay(2000)
            exit()
            
        elif victory == 2:
            font = pygame.font.Font('freesansbold.ttf', 32)
            if num_players == 1:
                text = font.render("Bot won!", True, colors['white'])
            else:
                text = font.render("Player 2 won!", True, colors['white'])
            text_rect = text.get_rect()
            text_rect.center = (400, 300)
            screen.blit(text, text_rect)
            pygame.display.update()
            pygame.time.delay(2000)
            exit()

        # Update the screen
        pygame.display.update()

def ball_speed_screen(numPlayers):
    running = True
    while running:
        # Limit the screen update rate
        clock.tick(240)

        # Background color setting
        screen.fill(colors['black'])
            
        # A title "Choose the ball speed" will appear, and a text field will appear for the user to enter the ball speed. The ball speed is a number between 0.5 and 5. If the user enters a number outside this range, the game will ask them to enter again.
        
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Choose the ball speed (1 is default)", True, colors['white'])
        text_rect = text.get_rect()
        text_rect.center = (400, 100)
        screen.blit(text, text_rect)
        
        def draw_button(text, x, y, width, height, color, hover_color):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if x < mouse[0] < x + width and y < mouse[1] < y + height:
                pygame.draw.rect(screen, hover_color, (x, y, width, height))
                if click[0] == 1:
                    return True
            else:
                pygame.draw.rect(screen, color, (x, y, width, height))
                
            # Draw button text
            button_text = font.render(text, True, colors['black'])
            text_rect = button_text.get_rect()
            text_rect.center = (x + width / 2, y + height / 2)
            screen.blit(button_text, text_rect)
            return False
        
        if numPlayers == 0:
            if draw_button("Speed 1", 250, 250, 250, 50, colors['white'], colors['cyan']):
                game(numPlayers, 0.89, 5, 70, 1.25, 1)
                running = False
            
            if draw_button("Speed 2", 250, 350, 250, 50, colors['white'], colors['cyan']):
                game(numPlayers, 1, 7, 100, 1.75, 1)
                running = False
            
            if draw_button("Speed 3", 250, 450, 250, 50, colors['white'], colors['cyan']):
                game(numPlayers, 3, 14, 100, 4, 1)
                running = False

        if numPlayers == 2:
            if draw_button("Speed 1", 250, 250, 250, 50, colors['white'], colors['cyan']):
                game(numPlayers, 1, 3, 50, 1.25, 1)
                running = False

            if draw_button("Speed 2", 250, 350, 250, 50, colors['white'], colors['cyan']):
                game(numPlayers, 1, 5, 50, 1.75, 1.25)
                running = False

            if draw_button("Speed 3", 250, 450, 250, 50, colors['white'], colors['cyan']):
                game(numPlayers, 1, 7, 50, 2.5, 1.5)
                running = False

        if draw_button("Back", 600, 500, 150, 50, colors['white'], colors['cyan']):
            initial_screen()
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

def difficulty_screen():
    running = True
    while running:
        # Limit the screen update rate
        clock.tick(240)

        # Set background colors
        screen.fill(colors['black'])

        # Display a title "Choose the difficulty" and three difficulties: easy, medium, and impossible,
        # each one will call the "game" function with 1 player and a different botSpeed: 0.5, 0.8, and 0.85 respectively.
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Choose the difficulty", True, colors['white'])
        text_rect = text.get_rect()
        text_rect.center = (400, 100)
        screen.blit(text, text_rect)

        def draw_button(text, x, y, width, height, color, hover_color):
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
                pygame.draw.rect(screen, hover_color, (x, y, width, height))
                if click[0] == 1:
                    return True
            else:
                pygame.draw.rect(screen, color, (x, y, width, height))

            # Draw button text
            button_text = font.render(text, True, colors['black'])
            text_rect = button_text.get_rect()
            text_rect.center = (x + width / 2, y + height / 2)
            screen.blit(button_text, text_rect)
            return False

        if draw_button("Easy", 300, 250, 200, 50, colors['white'], colors['cyan']):
            game(1, 0.75, 2, 50, 1.25, 1)
            running = False

        if draw_button("Medium", 300, 350, 200, 50, colors['white'], colors['cyan']):
            game(1, 0.9, 3, 70, 1.75, 1)
            running = False

        if draw_button("Impossible", 300, 450, 200, 50, colors['white'], colors['cyan']):
            game(1, 1.5, 5, 100, 2, 1.25)
            running = False

        if draw_button("Back", 600, 500, 150, 50, colors['white'], colors['cyan']):
            initial_screen()
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

def initial_screen():
    running = True
    while running:
        # Limit the screen update rate
        clock.tick(240)

        # Set background colors
        screen.fill(colors['black'])

        # Display a title "Ping Pong" and buttons "Bot VS Bot", "1 Player", "2 Players", and "Quit"
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Ping Pong", True, colors['white'])
        text_rect = text.get_rect()
        text_rect.center = (400, 100)
        screen.blit(text, text_rect)

        def draw_button(text, x, y, width, height, color, hover_color):
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:  # If the mouse is inside the button
                pygame.draw.rect(screen, hover_color, (x, y, width, height))
                if click[0] == 1:  # If the left mouse button is clicked
                    return True
            else:
                pygame.draw.rect(screen, color, (x, y, width, height))

            # Draw the button text
            button_text = font.render(text, True, colors['black'])
            text_rectangle = button_text.get_rect()
            text_rectangle.center = (x + width / 2, y + height / 2)
            screen.blit(button_text, text_rectangle)
            return False

        if draw_button("Bot VS Bot", 300, 200, 200, 50, colors['white'], colors['cyan']):
            ball_speed_screen(0)
            running = False  # Anti bug

        if draw_button("1 Player", 300, 300, 200, 50, colors['white'], colors['cyan']):
            difficulty_screen()
            running = False  # Anti bug

        if draw_button("2 Players", 300, 400, 200, 50, colors['white'], colors['cyan']):
            ball_speed_screen(2)
            running = False  # Anti bug

        if draw_button("Exit", 300, 500, 200, 50, colors['white'], colors['cyan']):
            exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Anti bug

        pygame.display.update()

if __name__ == "__main__":
    initial_screen()