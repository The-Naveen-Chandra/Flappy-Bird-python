import pygame

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.game_over_message import GameOverMessage
from objects.game_start_message import GameStartMessage
from objects.score import Score

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameStarted = False
gameOver = False

assets.load_sprites()
assets.load_audios()


sprites = pygame.sprite.LayeredUpdates()


def create_sprites():
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)

    return Bird(sprites), GameStartMessage(sprites), Score(sprites)


bird, game_started_message, score = create_sprites()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gameStarted and not gameOver:
                gameStarted = True
                game_started_message.kill()
                pygame.time.set_timer(column_create_event, millis=1500)
            if event.key == pygame.K_ESCAPE and gameOver:
                gameOver = False
                gameStarted = False
                sprites.empty()
                bird, game_started_message, score = create_sprites()

        bird.handle_event(event)

    screen.fill(0)

    sprites.draw(screen)

    if gameStarted and not gameOver:
        sprites.update()

    if bird.check_collision(sprites) and not gameOver:
        gameOver = True
        gameStarted = False
        GameOverMessage(sprites)
        pygame.time.set_timer(column_create_event, millis=0)
        assets.play_audio("hit")

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            assets.play_audio("point")

    pygame.display.flip()
    clock.tick(configs.FPS)
pygame.quit()
