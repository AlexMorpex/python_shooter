import sys
import pygame
from random import randint

def run_game():
    while True:  # Цикл перезапуска игры
        game()
        if not ask_restart():
            break  # Если игрок выбирает "No", выходим из цикла и завершаем программу

def game():
    pygame.init()  # Инициализация игры

    game_font = pygame.font.Font(None, 30)

    # Устанавливаем размер экрана
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen_fill_color = (32, 52, 71)

    pygame.display.set_caption("Awesome Shooter Game")  # Заголовок игры

    FIGHTER_STEP = 0.3
    fighter_image = pygame.image.load('images/fighter.png')  # Загрузить изображение для корабля
    fighter_width, fighter_height = fighter_image.get_size()
    fighter_x, fighter_y = screen_width / 2 - fighter_width / 2, screen_height - fighter_height
    fighter_is_moving_left, fighter_is_moving_right = False, False

    BALL_STEP = 0.1
    ball_image = pygame.image.load('images/ball.png')
    ball_width, ball_height = ball_image.get_size()
    ball_x, ball_y = 0, 0
    ball_was_fired = False

    ALIEN_STEP = 0.03
    alien_speed = ALIEN_STEP
    alien_image = pygame.image.load('images/alien.png')
    alien_width, alien_height = alien_image.get_size()
    alien_x, alien_y = randint(0, screen_width - alien_width), 0

    game_is_running = True
    game_score = 0

    while game_is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fighter_is_moving_left = True
                if event.key == pygame.K_RIGHT:
                    fighter_is_moving_right = True
                if event.key == pygame.K_SPACE:
                    ball_was_fired = True
                    ball_x = fighter_x + fighter_width / 2 - ball_width / 2
                    ball_y = fighter_y - ball_height

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    fighter_is_moving_left = False
                if event.key == pygame.K_RIGHT:
                    fighter_is_moving_right = False

        if fighter_is_moving_left and fighter_x >= FIGHTER_STEP:
            fighter_x -= FIGHTER_STEP

        if fighter_is_moving_right and fighter_x <= screen_width - fighter_width - FIGHTER_STEP:
            fighter_x += FIGHTER_STEP

        alien_y += alien_speed

        if ball_was_fired and ball_y + ball_height < 0:
            ball_was_fired = False

        if ball_was_fired:
            ball_y -= BALL_STEP

        screen.fill(screen_fill_color)
        screen.blit(fighter_image, (fighter_x, fighter_y))
        screen.blit(alien_image, (alien_x, alien_y))

        if ball_was_fired:
            screen.blit(ball_image, (ball_x, ball_y))

        game_score_text = game_font.render(f"Score: {game_score}", True, 'white')
        screen.blit(game_score_text, (20, 20))

        pygame.display.update()

        if alien_y + alien_height > fighter_y:
            game_is_running = False

        if (ball_was_fired and
                alien_x-ball_width < ball_x < alien_x + alien_width and
                alien_y < ball_y < alien_y + alien_height):
            ball_was_fired = False
            alien_x, alien_y = randint(0, screen_width - alien_width), 0
            alien_speed += 0.002
            game_score += 1

def ask_restart():
    screen = pygame.display.get_surface()
    game_font = pygame.font.Font(None, 30)
    screen_width, screen_height = screen.get_size()

    restart_text = game_font.render("Restart ?", True, 'White')
    restart_rectangle = restart_text.get_rect(center=(screen_width / 2, screen_height / 2 + 10))
    screen.blit(restart_text, restart_rectangle)

    game_font_over = pygame.font.Font(None, 50)
    game_over_text = game_font_over.render("Game Over", True, 'White')
    game_over_rectangle = game_over_text.get_rect()
    game_over_rectangle.center = (restart_rectangle.centerx, restart_rectangle.y-game_over_text.get_height())
    screen.blit(game_over_text,game_over_rectangle)

    # Создаем кнопки "Yes" и "No"
    yes_button = pygame.Rect(screen_width / 2 - 50, screen_height / 2 + 40, 50, 30)
    no_button = pygame.Rect(screen_width / 2 + 10, screen_height / 2 + 40, 50, 30)

    pygame.draw.rect(screen, 'Green', yes_button)
    pygame.draw.rect(screen, 'Red', no_button)

    yes_text = game_font.render("Yes", True, 'White')
    no_text = game_font.render("No", True, 'White')


    screen.blit(yes_text, (yes_button.x + 8, yes_button.y + 5))
    screen.blit(no_text, (no_button.x + 8, no_button.y + 5))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if yes_button.collidepoint(mouse_pos):
                    return True  # Перезапустить игру
                elif no_button.collidepoint(mouse_pos):
                    return False  # Завершить программу

if __name__ == '__main__':
    run_game()
