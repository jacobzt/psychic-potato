import pygame
import random
import os
import asyncio

pygame.init()

# 基本設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 500
HEIGHT = 600
FPS = 60

score = 0
game_start_time = pygame.time.get_ticks()

# 視窗初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D遊戲")
clock = pygame.time.Clock()

# 圖片載入與縮放
player_img = pygame.image.load(os.path.join("img", "player.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (30, 30))
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
rock_img = pygame.transform.scale(rock_img, (30, 30))

# 字型 & 文字顯示
font_name = pygame.font.match_font("arial")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

# 初始畫面
def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "just a game", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "WASD control player", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press any key to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP:
                return False

# 結束畫面
def show_game_over_screen():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "Game Over", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, f"your score: {score}", 32, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "press any key to continue", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP:
                return False

# 玩家精靈
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += self.speedx
        if keys[pygame.K_a]:
            self.rect.x -= self.speedx
        if keys[pygame.K_s]:
            self.rect.y += self.speedx
        if keys[pygame.K_w]:
            self.rect.y -= self.speedx

        # 邊界限制
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, 500)

# 隕石精靈
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = rock_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(4, 10)

    def update(self):
        global score
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(4, 10)
            score += 1

# 初始化新遊戲
def new_game():
    global all_sprites, rocks, player, score, game_start_time
    score = 0
    game_start_time = pygame.time.get_ticks()
    all_sprites = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(10):
        rock = Rock()
        all_sprites.add(rock)
        rocks.add(rock)

# 主迴圈
async def main():
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # 傳回控制權給主程式

        all_sprites.update()

        if pygame.sprite.spritecollide(player, rocks, False):
            if show_game_over_screen():
                return
            new_game()
            if draw_init():
                return

        if score >= 100:
            for rock in rocks:
                new_rock = Rock()
            all_sprites.add(new_rock)
            rocks.add(new_rock)

        if pygame.time.get_ticks() - game_start_time > 15000 and len(rocks) < 20:
            new_rock = Rock()
            all_sprites.add(new_rock)
            rocks.add(new_rock)

        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, "score: " + str(score), 18, WIDTH / 2, 10)
        pygame.display.flip()
        await asyncio.sleep(0)

# 執行遊戲
new_game()
if draw_init():
    pygame.quit()
else:
    asyncio.run(main())
    pygame.quit()