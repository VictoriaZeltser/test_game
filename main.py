import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Волк и яйца')
clock = pygame.time.Clock()
game_over = False

# Цвета
dark_grey = (100, 150, 255)  # Потемнее фон
egg_color = (255, 255, 255)

# Начальные позиции и размеры волка
wolf_width = 240  # Увеличенный размер волка
wolf_height = 120
wolf_x = screen_width // 2 - wolf_width // 2
wolf_y = screen_height - wolf_height - 10
wolf_speed = 5
wolf_direction = 'right'  # Начальное направление волка

# Загрузка и масштабирование изображения волка
wolf_image_original = pygame.image.load('picPython-removebg-preview.png')
wolf_image = pygame.transform.scale(wolf_image_original, (wolf_width, wolf_height))

# Яйца
eggs = []
egg_speed_initial = 1
egg_width = 20
egg_height = 26
missed_eggs = 0

# Счет
score = 0

# Шрифт
font = pygame.font.SysFont(None, 36)

def draw_wolf(x, y, direction):
    wolf_flipped = pygame.transform.flip(wolf_image, direction == 'left', False)
    screen.blit(wolf_flipped, (x, y))

def drop_egg():
    x = random.randint(0, screen_width - egg_width)
    eggs.append([x, 0, egg_speed_initial + random.random() * 2])  # Разная скорость падения

def draw_eggs():
    for egg in eggs:
        pygame.draw.ellipse(screen, egg_color, [egg[0], egg[1], egg_width, egg_height])

def update_eggs():
    global missed_eggs
    for egg in eggs:
        egg[1] += egg[2]
        if egg[1] > screen_height:
            eggs.remove(egg)
            missed_eggs += 1

def check_collision():
    global score
    wolf_rect = pygame.Rect(wolf_x, wolf_y, wolf_width, wolf_height)
    for egg in eggs[:]:
        egg_rect = pygame.Rect(egg[0], egg[1], egg_width, egg_height)
        if wolf_rect.colliderect(egg_rect):
            eggs.remove(egg)
            score += 1

def draw_score():
    score_text = font.render(f"Счет: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

def draw_missed_eggs():
    missed_text = font.render(f"Пропущено: {missed_eggs}", True, (0, 0, 0))
    screen.blit(missed_text, (screen_width - 150, 10))

# Главный игровой цикл
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Управление волком с помощью мыши и клавиатуры
    mouse_x, mouse_y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or (event.type == pygame.MOUSEMOTION and mouse_x < wolf_x):
        wolf_x -= wolf_speed
        wolf_direction = 'left'
    elif keys[pygame.K_RIGHT] or (event.type == pygame.MOUSEMOTION and mouse_x > wolf_x + wolf_width):
        wolf_x += wolf_speed
        wolf_direction = 'right'

    wolf_x = max(0, min(screen_width - wolf_width, wolf_x))  # Ограничение перемещения волка в пределах экрана

    # Обновление экрана
    screen.fill(dark_grey)
    draw_wolf(wolf_x, wolf_y, wolf_direction)
    if random.randint(1, 60) == 1:
        drop_egg()
    update_eggs()
    check_collision()
    draw_eggs()
    draw_score()
    draw_missed_eggs()

    # Условие проигрыша
    if missed_eggs >= 3:
        game_over_text = font.render("Игра окончена", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
