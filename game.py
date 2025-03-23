from pygame import *

win_width, win_height = 700, 500
window = display.set_mode((win_width, win_height))
display.set_caption("Simple Platformer Game")

player_img = transform.scale(image.load('player.png'), (50, 50))
bullet_img = transform.scale(image.load('bullet.png'), (10, 5))
background_img = transform.scale(image.load('background0.png'), (win_width, win_height))
platform_img = transform.scale(image.load('platform.png'), (100, 20))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = player_image
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__(player_image, player_x, player_y, player_speed, size_x, size_y)
        self.original_image = player_image
        self.direction = 'right'
        self.is_jumping = False
        self.jump_speed = 10
        self.gravity = 0.5
        self.velocity_y = 0

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            if self.direction != 'left':
                self.image = transform.flip(self.original_image, True, False)
                self.direction = 'left'
            self.check_collision('left')
        if keys[K_RIGHT] and self.rect.x < win_width - 55:
            self.rect.x += self.speed
            if self.direction != 'right':
                self.image = self.original_image
                self.direction = 'right'
            self.check_collision('right')
        if not self.is_jumping:
            if keys[K_UP]:
                self.is_jumping = True
                self.velocity_y = -self.jump_speed

        self.rect.y += self.velocity_y
        self.velocity_y += self.gravity

        if self.rect.y >= win_height - 55:
            self.rect.y = win_height - 55
            self.is_jumping = False
            self.velocity_y = 0

        self.check_collision('vertical')

    def check_collision(self, direction):
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                if direction == 'vertical':
                    if self.velocity_y > 0 and self.rect.bottom <= platform.rect.bottom:
                        self.rect.bottom = platform.rect.top
                        self.is_jumping = False
                        self.velocity_y = 0
                    elif self.velocity_y < 0 and self.rect.top >= platform.rect.top:
                        self.rect.top = platform.rect.bottom
                        self.velocity_y = 0
                elif direction == 'left':
                    if self.rect.left <= platform.rect.right and self.rect.right >= platform.rect.left:
                        self.rect.left = platform.rect.right
                elif direction == 'right':
                    if self.rect.right >= platform.rect.left and self.rect.left <= platform.rect.right:
                        self.rect.right = platform.rect.left

    def fire(self):
        if self.direction == 'right':
            bullet = Bullet(bullet_img, self.rect.centerx, self.rect.centery, 15)
        else:
            bullet = Bullet(bullet_img, self.rect.centerx, self.rect.centery, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed, image.get_width(), image.get_height())

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width or self.rect.x < 0:
            self.kill()

class Platform(GameSprite):
    def __init__(self, x, y):
        super().__init__(platform_img, x, y, 0, platform_img.get_width(), platform_img.get_height())

player = Player(player_img, 100, 400, 5, 50, 50)
bullets = sprite.Group()
platforms = sprite.Group()

# Add platforms to create a full level
platforms.add(Platform(100, 450))
platforms.add(Platform(200, 400))
platforms.add(Platform(300, 350))
platforms.add(Platform(400, 300))
platforms.add(Platform(500, 250))
platforms.add(Platform(600, 200))
platforms.add(Platform(100, 150))
platforms.add(Platform(200, 100))
platforms.add(Platform(300, 50))
platforms.add(Platform(400, 150))
platforms.add(Platform(500, 50))
platforms.add(Platform(600, 150))

run = True
clock = time.Clock()
FPS = 60

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    window.blit(background_img, (0, 0))
    player.update()
    bullets.update()
    player.reset()
    bullets.draw(window)
    platforms.draw(window)

    display.update()
    clock.tick(FPS)