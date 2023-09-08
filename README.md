# PT-BR
## Jogo do PONG

Jogo do PONG feito em Python com a biblioteca Pygame.

O jogo pode ser jogado sozinho contra o computador ou contra outra pessoa. O jogo termina quando um dos jogadores atinge 5 pontos.

![Jogo do PONG](images/Pong%20game.jpg)

### Lógica do código

Logica do jogo, a bola é redesenhada a cada tick (240 ticks por segundo) ela é desenhada baseada em seus parâmetros  X (horizontal) e Y (Vertical) que são atualizados a cada tick, a cada tick a bola é redesenhada em uma posição diferente, dando a impressão de movimento. Os parâmetros são alterados baseado na Velocidade X e Velocidade Y. Quando a bola colide com um jogador a velocidade X é invertida e a velocidade Y é alterada baseada na posição do jogador, se o jogador estiver no meio a bola vai sair reto, se estiver no canto a bola vai sair em um angulo de 45 graus, se estiver no meio e se movendo para cima a bola vai sair em um angulo de 45 graus para cima, se estiver no meio e se movendo para baixo a bola vai sair em um angulo de 45 graus para baixo (ângulos ilustrativos). Quando a bola colide com a parede a velocidade Y é invertida. Quando a bola colide com a parede esquerda ou direita a pontuação é alterada e a bola é resetada para o meio da tela. Quando a pontuação chega a 5 o jogo acaba e o jogador que chegou a 5 pontos ganha.
OBS: Vale lembrar que a tela é a todo momento redesenhada, então se você desenhar um retângulo na posição (0, 0) e depois desenhar um retângulo na posição (0, 0) o primeiro retângulo será apagado, por isso é necessário redesenhar a tela a todo momento.

### Como jogar

Para jogar é necessário ter o Python 3 instalado e a biblioteca Pygame instalada, para instalar o Pygame basta digitar o seguinte comando no terminal:

```bash
pip install pygame
```

Após instalar o Pygame, basta executar o arquivo main.py com o Python 3.

### Controles

Jogador 1 (Esquerda):

- W: Move para cima
- S: Move para baixo

Jogador 2 (Direita):

- Seta para cima: Move para cima
- Seta para baixo: Move para baixo

### Créditos

- [Pygame](https://www.pygame.org/)
- [Python](https://www.python.org/)
- [João Victor](https://github.com/JoaoVictor-C)

# EN-US
## PONG game

PONG game made in Python with the Pygame library.

The game can be played alone against the computer or against another person. The game ends when one of the players reaches 5 points.

![PONG game](images/Pong%20game.jpg)

### Code logic

Game logic, the ball is redrawn every tick (240 ticks per second) it is drawn based on its parameters X (horizontal) and Y (Vertical) which are updated every tick, every tick the ball is redrawn in a different position, giving the impression of movement. The parameters are changed based on the X Speed and Y Speed. When the ball collides with a player the X speed is inverted and the Y speed is changed based on the position of the player, if the player is in the middle the ball will come out straight, if it is in the corner the ball will come out at an angle of 45 degrees, if it is in the middle and moving up the ball will come out at an angle of 45 degrees up, if it is in the middle and moving down the ball will come out at an angle of 45 degrees down (illustrative angles). When the ball collides with the wall the Y speed is inverted. When the ball collides with the left or right wall the score is changed and the ball is reset to the middle of the screen. When the score reaches 5 the game is over and the player who reached 5 points wins.

### How to play

To play you need to have Python 3 installed and the Pygame library installed, to install Pygame just type the following command in the terminal:

```bash
pip install pygame
```

After installing Pygame, just run the main.py file with Python 3.

### Controls

Player 1 (Left): 

- W: Move up
- S: Move down

Player 2 (Right):

- Up arrow: Move up
- Down arrow: Move down

### Credits

- [Pygame](https://www.pygame.org/)
- [Python](https://www.python.org/)
- [João Victor](https://github.com/JoaoVictor-C)