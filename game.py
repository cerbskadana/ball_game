from pygame import *
from math import hypot
from random import randint


class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.speed = speed
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def move(self):
        keys = key.get_pressed()
        if keys[K_UP]:
            self.y -= self.speed
        if keys[K_DOWN]:
            self.y += self.speed
        if keys[K_LEFT]:
            self.x -= self.speed
        if keys[K_RIGHT]:
            self.x += self.speed

    def reset(self, center_x, center_y, scale):
        sx = int((self.x - center_x) * scale + WINDOW_SIZE[0] / 2)
        sy = int((self.y - center_y) * scale + WINDOW_SIZE[1] / 2)
        draw.circle(window, self.color, (sx, sy), self.radius * scale)

    def collidecircle(self, ball2):
        distance = hypot(self.x - ball2.x, self.y - ball2.y)
        return distance < (self.radius + ball2.radius)

    def draw_centre(self,scale):
        draw.circle(window, self.color, (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2), int(self.radius * scale))
init()

WINDOW_SIZE = 500, 500

window = display.set_mode(WINDOW_SIZE)
display.set_caption("ВАША НАЗВА")
clock = time.Clock()

# bg = image.load("img.png")
# bg = transform.scale(bg, size)

player = Ball(300, 300, 25, (255, 100, 255), 5)

balls=[Ball(randint(-2000, 2000), randint(-2000, 2000), 10 ,(randint(0,255), randint(0,255), randint(0,255)), 5) for _ in range(300)]
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
    scale = max(0.3, min(50/player.radius, 1.5))
    window.fill((255, 255, 255))
    # window.blit(bg, (0, 0))
    player.move()
    player.draw_centre(scale)

    # Кульки
    to_remove = []
    for ball in balls:
        if player.collidecircle(ball):
            to_remove.append(ball)
            player.radius += int(ball.radius * 0.2)
        else:
            ball.reset(player.x, player.y, scale)

    for ball in to_remove:
        balls.remove(ball)


    display.update()
    clock.tick(60)