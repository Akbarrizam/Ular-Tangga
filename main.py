import pygame
import sys
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ular Futuristik')

background_color = (13, 2, 33)
grid_color = (0, 255, 255, 50)
snake_head_color = (0, 255, 127)
snake_body_color = (57, 255, 20)
fruit_color = (255, 0, 255)
fruit_glow_color = (255, 0, 255, 100)
text_color = (240, 240, 240)
game_over_color = (255, 20, 147)

clock = pygame.time.Clock()
snake_block = 20
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 30)
score_font = pygame.font.SysFont("consolas", 35, bold=True)

def show_score(score):
    score_text = "SKOR: " + str(score)
    value = score_font.render(score_text, True, text_color)
    shadow = score_font.render(score_text, True, fruit_color)
    screen.blit(shadow, (12, 12))
    screen.blit(value, (10, 10))

def our_snake(snake_block, snake_list):
    if snake_list:
        head = snake_list[-1]
        pygame.draw.rect(screen, snake_head_color, [head[0], head[1], snake_block, snake_block], border_radius=7)
        pygame.draw.rect(screen, (255,255,255), [head[0]+5, head[1]+5, 6, 6], border_radius=3)

    for i, segment in enumerate(snake_list[:-1]):
        ratio = i / len(snake_list)
        color = (
            int(snake_body_color[0] * (1 - ratio) + background_color[0] * ratio),
            int(snake_body_color[1] * (1 - ratio) + background_color[1] * ratio),
            int(snake_body_color[2] * (1 - ratio) + background_color[2] * ratio)
        )
        pygame.draw.rect(screen, color, [segment[0], segment[1], snake_block, snake_block], border_radius=5)

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(screen_width / 2, screen_height / 2 + y_displace))
    screen.blit(mesg, mesg_rect)

def draw_background_grid():
    screen.fill(background_color)
    for x in range(0, screen_width, snake_block):
        pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height), 1)
    for y in range(0, screen_height, snake_block):
        pygame.draw.line(screen, grid_color, (0, y), (screen_width, y), 1)

def draw_fruit(x, y):
    center_x, center_y = x + snake_block // 2, y + snake_block // 2
    pygame.draw.circle(screen, fruit_glow_color, (center_x, center_y), snake_block // 2 + 3)
    pygame.draw.circle(screen, fruit_color, (center_x, center_y), snake_block // 2)


def gameLoop():
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    score = 0

    fruitx = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
    fruity = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0

    while not game_over:

        while game_close:
            draw_background_grid()
            message("GAME OVER", game_over_color, -50)
            message("Skor Akhir: " + str(score), text_color, 0)
            message("Tekan 'C' untuk Main Lagi atau 'Q' untuk Keluar", text_color, 70)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True
            
        x1 += x1_change
        y1 += y1_change
        
        draw_background_grid()
        
        draw_fruit(fruitx, fruity)
        
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
        show_score(score)

        pygame.display.update()

        if x1 == fruitx and y1 == fruity:
            fruitx = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
            fruity = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            score += 10

        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

gameLoop()