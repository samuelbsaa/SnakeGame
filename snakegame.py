import pygame
import random
import pygame.mixer

pygame.init()

pygame.mixer.init()
eat_sound = pygame.mixer.music.load("eat_sound.wav")
collision_sound = pygame.mixer.Sound("collision_sound.mp3")
game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")
game_over_sound_played = False


# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (124, 179, 66)
BLUE = (0, 0, 255)

# Definição das dimensões da janela
window_width = 800
window_height = 600

# Configurações da cobrinha
snake_block = 20
snake_speed = 13

# Inicialização da janela do jogo
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Jogo da Cobrinha")

clock = pygame.time.Clock()

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Função para desenhar um botão com texto na tela
def draw_button_with_text(x, y, width, height, color, text, text_color):
    pygame.draw.rect(window, color, [x, y, width, height])
    font = pygame.font.SysFont(None, 30)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width/2, y + height/2)
    window.blit(text_surface, text_rect)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, BLACK, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [window_width/10, window_height/2])

def game_loop():
    game_over = False
    game_close = False

    x1 = window_width / 2
    y1 = window_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, window_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, window_height - snake_block) / 20.0) * 20.0

    apple_img = pygame.image.load("apple.png")
    apple_img = pygame.transform.scale(apple_img, (snake_block, snake_block))

    def game_over_screen(score):
        gameover_img = pygame.image.load("game_over.png")  # Carrega a imagem do fundo do game over
        gameover_img = pygame.transform.scale(gameover_img, (800, 900))  # Redimensiona a imagem para o tamanho da janela
        window.blit(gameover_img, (0, 0))  # Desenha a imagem na janela
        message("Em desenvolvimento.", WHITE)


    score = 0


    while not game_over:
        while game_close == True:
            game_over_screen(score)

            # Desenhar o botão com o texto na tela
            button_x = 270
            button_y = 400
            button_width = 300
            button_height = 50
            button_color = WHITE
            button_text = "Aperte para jogar novamente"
            button_text_color = BLACK
            draw_button_with_text(button_x, button_y, button_width, button_height, button_color, button_text,
                                  button_text_color)

            # Verificar eventos de clique
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Obter as coordenadas do clique do mouse
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Verificar se o clique está dentro dos limites do botão
                    if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                        # Reiniciar o jogo
                        game_loop()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if game_over:
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -snake_block
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = snake_block
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -snake_block
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = snake_block
                x1_change = 0

        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        window.fill(BLACK)
        window.blit(apple_img, (foodx, foody))
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        window.blit(apple_img, (foodx, foody))

        if x1 == foodx and y1 == foody:
            collision_sound.play()
            foodx = round(random.randrange(0, window_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, window_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 2
            score += 5

        pygame.display.update()

        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_close = True

        window.fill(GREEN)
        window.blit(apple_img, (foodx, foody))

        score_text = score_font.render("Pontuação: " + str(score), True, WHITE)
        window.blit(score_text, [10, 10])

        our_snake(snake_block, snake_List)

        pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()


game_loop()
