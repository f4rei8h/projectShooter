import pygame
import random
from pygame.math import Vector2

width = 1000                    # ширина игрового окна
height = 1000                   # высота игрового окна
fps = 40                        # частота кадров в секунду
gameName = "MetroLublino"       # название нашей игры

pygame.init()                   # Инициализируем модуль pygame
pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

imgdir = 'media/img'
snddir = 'media/snd'

# Создаем игровой экран
screen = pygame.display.set_mode((width, height))

bg = pygame.image.load(imgdir + '/bg2.jpg')
bg = pygame.transform.scale(bg, (width, height))
bg_rect = bg.get_rect()


pygame.display.set_caption(gameName)     # Заголовок окна

#icon = pygame.image.load('ivon.png')    # загружаем файл с иконкой
#pygame.display.set_icon(icon)           # устанавливаем иконку в окно
clock = pygame.time.Clock()              # Создаем часы pygame

all_sprites = pygame.sprite.Group()      # Группа для ВСЕХ спрайтов
mobs = pygame.sprite.Group()             # Группа для мобов
bullets = pygame.sprite.Group()
grenades = pygame.sprite.Group()


def drawText(screen, text, size, x, y, color):
    fontname = './calibri.ttf'
    font = pygame.font.Font(fontname, size)
    textsprite = font.render(text, True, color)
    text_rect = textsprite.get_rect()
    text_rect.center = (x, y)
    screen.blit(textsprite, text_rect)

class Player(pygame.sprite.Sprite):
   def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load(imgdir + '/player/1.png')
       self.image = pygame.transform.scale(self.image, (100, 75))
       self.direction = Vector2(1, 0)
       self.rect = self.image.get_rect()
       self.points = 0
       self.magazin = 10

       self.speed = 5
       self.copy = self.image
       self.position = Vector2(self.rect.center)
       self.angle = 0

       self.anim_speed = 4
       self.frame = 0
       self.anim = []

       self.hp = 500
       self.max_hp = self.hp

       self.shoot_sound = pygame.mixer.Sound(snddir + '/shoot.wav')

       for i in range(1, 21):
           image = pygame.image.load(imgdir + f'/player/{i}.png')
           image = pygame.transform.scale(image, (100,75))
           self.anim.append(image)

   def rotate(self, rotate_speed):
       self.direction.rotate_ip(-rotate_speed)
       self.angle += rotate_speed
       self.image = pygame.transform.rotate(self.copy, self.angle)
       self.rect = self.image.get_rect(center = self.rect.center)

   def animation(self):
       self.image = self.anim[self.frame//self.anim_speed]
       self.frame += 1
       self.image = pygame.transform.rotate(self.image, self.angle)
       self.rect = self.image.get_rect(center = self.rect.center)
       if self.frame == self.anim_speed * len(self.anim):
           self.frame = 0

   def drawHP(self):
       hp_width = 100
       hp_height = 20

       color_red = (255, 0, 0)
       color_yellow = (255, 255, 0)
       color_green = (0, 255, 0)

       color = color_green
       if self.hp < 300:
           color = color_yellow
       if self.hp < 100:
           color = color_red

       rect = pygame.Rect(150, 15, hp_width, hp_height)
       fill_width = self.hp / self.max_hp * hp_width
       fill_rect = pygame.Rect(150, 15, fill_width, hp_height)

       pygame.draw.rect(screen, color, fill_rect)
       pygame.draw.rect(screen, WHITE, rect, 1)

   def update(self):
       self.drawHP()
       key = pygame.key.get_pressed()
       if key[pygame.K_RIGHT]:                              # Если клавиша вправо нажата
           self.rotate(-5)
       if key[pygame.K_LEFT]:                               # Если клавиша влево нажата
           self.rotate(5)
       if key[pygame.K_UP]:                                 # Если клавиша вправо нажата
           self.position += self.speed * self.direction
       if key[pygame.K_DOWN]:                               # Если клавиша влево нажата
           self.position -= self.speed * self.direction

       self.rect.center = self.position
       self.animation()

class Mob_left(pygame.sprite.Sprite):
   def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load(imgdir + '/enemy5/grenade.png')
       self.image = pygame.transform.scale(self.image, (40, 40))
       self.rect = self.image.get_rect()

       self.speedx = random.randrange(1, 4)           # Скорость моба
       self.speedy = random.randrange(-4, 4)
       self.rect.x = 0                                # Позиция моба
       self.rect.y = random.randrange(0, height)

       self.speed = 5
       self.copy = self.image
       self.position = Vector2(self.rect.center)
       self.angle = 0
       self.direction = Vector2(0, -1)

       self.hp = 100
       self.attack_sound = pygame.mixer.Sound(snddir + '/blow.wav')
       self.death_sound = pygame.mixer.Sound(snddir + '/blow.wav')

   def rotate(self, rotate_speed):
       self.direction.rotate_ip(-rotate_speed)
       self.angle += rotate_speed
       self.image = pygame.transform.rotate(self.copy, self.angle)
       self.rect = self.image.get_rect(center = self.rect.center)

   def update(self):
       self.rotate(30)
       self.rect.x += self.speedx
       self.rect.y += self.speedy

       if self.rect.x > width or self.rect.x > height or self.rect.x < 0:
           self.rect.x = 0
           self.rect.y = random.randrange(0, height)

class Mob_up(pygame.sprite.Sprite):
   def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load(imgdir + '/enemy1/1.png')
       self.image = pygame.transform.scale(self.image, (100, 75))
       self.rect = self.image.get_rect()

       self.speedx = random.randrange(1, 4)
       self.speedy = random.randrange(-4, 8)

       self.rect.y = 0
       self.rect.x = random.randrange(1, height)

       self.angle = 0
       self.anim_speed = 4
       self.frame = 0
       self.anim = []

       self.copy = self.image
       self.start = Vector2(0, 1)
       self.direction = Vector2(self.speedx, self.speedy)
       self.angle = self.start.angle_to(self.direction)

       self.hp = 100
       self.max_hp = self.hp

       self.attack_sound = pygame.mixer.Sound(snddir + '/zombie_attack.wav')
       self.death_sound = pygame.mixer.Sound(snddir + '/zombie_death1.wav')

       for i in range(1, 9):
           image = pygame.image.load(imgdir + f'/enemy1/{i}.png')
           image = pygame.transform.scale(image, (100, 75))
           self.anim.append(image)

   def animation(self):
       self.image = self.anim[self.frame//self.anim_speed]
       self.frame += 1
       self.image = pygame.transform.rotate(self.image, -self.angle)
       self.rect = self.image.get_rect(center = self.rect.center)
       if self.frame == self.anim_speed * len(self.anim):
           self.frame = 0

   def drawHP(self):
       hp_width = 30
       hp_height = 7

       rect = pygame.Rect(self.rect.x, self.rect.y, hp_width, hp_height)
       fill_width = self.hp / self.max_hp * hp_width
       fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, hp_height)

       pygame.draw.rect(screen, GREEN, fill_rect)
       pygame.draw.rect(screen, WHITE, rect, 1)

   def update(self):
        self.drawHP()
        self.animation()
        self.rect.x -= self.speedx
        self.rect.y += self.speedy

        if self.rect.x > width or self.rect.x > height or self.rect.x < 0:
            self.rect.y = 0
            self.rect.x = random.randrange(0, height)

            self.direction = Vector2(self.speedx, self.speedy)
            self.angle = self.start.angle_to(self.direction)

class Mob_Right(pygame.sprite.Sprite):
   def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load(imgdir + '/enemy2/1.png')
       self.image = pygame.transform.scale(self.image, (100, 75))
       self.rect = self.image.get_rect()

       self.speedx = random.randrange(1, 7)               # Скорость моба
       self.speedy = random.randrange(-7, 7)

       self.rect.x = width                                # Позиция моба
       self.rect.y = random.randrange(0, height)

       self.angle = 0
       self.anim_speed = 4
       self.frame = 0
       self.anim = []

       self.hp = 100

       self.attack_sound = pygame.mixer.Sound(snddir + '/zombie_attack.wav')
       self.death_sound = pygame.mixer.Sound(snddir + '/zombie_death1.wav')

       for i in range(1, 9):
           image = pygame.image.load(imgdir + f'/enemy2/{i}.png')
           image = pygame.transform.scale(image, (100, 75))
           self.anim.append(image)

   def animation(self):
       self.image = self.anim[self.frame//self.anim_speed]
       self.frame += 1
       self.image = pygame.transform.rotate(self.image, self.angle)
       self.rect = self.image.get_rect(center = self.rect.center)
       if self.frame == self.anim_speed * len(self.anim):
           self.frame = 0

   def update(self):
       self.animation()
       self.rect.x -= self.speedx
       self.rect.y += self.speedy

       if self.rect.x < 0 or self.rect.x > height:
           self.rect.x = width                          # Позиция моба
           self.rect.y = random.randrange(0, height)

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imgdir + '/shell.png')
        self.image = pygame.transform.scale(self.image, (5, 15))
        self.image = pygame.transform.rotate(self.image, player.angle -90)
        self.rect = self.image.get_rect()
        self.rect.center = Vector2(player.rect.center)
        self.speed = 30
        self.move = player.direction * self.speed

    def update(self):
        self.rect.center += self.move
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.anim_speed = 4
        self.frame = 0
        self.anim = []

        for i in range(9):
            image = pygame.image.load(imgdir + f'/explosion/{i}.png')
            image = pygame.transform.scale(image, (100, 100))
            self.anim.append(image)

        self.image = self.anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        if self.frame >= self.anim_speed * len(self.anim):
            self.kill()
        else:
            self.image = self.anim[self.frame // self.anim_speed]
            self.frame += 1


player = Player()                       # Создаем игрока на основании класса
all_sprites.add(player)                 # Добавляем игрока ко всем спрайтам

for i in range(3):                      # Цикл создания левых мобов
    mobleft = Mob_left()
    all_sprites.add(mobleft)
    mobs.add(mobleft)
    grenades.add(mobleft)

for i in range(5):                      # Цикл создания верхних мобов
    mob_up = Mob_up()
    all_sprites.add(mob_up)
    mobs.add(mob_up)

for i in range(10):                      # Цикл создания правых мобов
    mob_right = Mob_Right()
    all_sprites.add(mob_right)
    mobs.add(mob_right)

pygame.mixer.music.load(snddir + '/Music.wav')
pygame.mixer.music.play(loops = -1)
pygame.mixer.music.set_volume(0.2)

run = True
while run:
   clock.tick(fps)
   all_sprites.update()
   pygame.display.update()

   boom_player = pygame.sprite.spritecollide(player, grenades, False)
   if boom_player:
       for grenade in boom_player:
           player.hp -= 100
           expl = Explosion(grenade.rect.center)
           all_sprites.add(expl)
           grenade.kill()

   hits = pygame.sprite.spritecollide(player, mobs, False)
   if hits:
       player.hp -= 1
       for mob in hits:
           mob.attack_sound.play()

   shoots = pygame.sprite.groupcollide(bullets, mobs, True, False)
   if shoots:
       for mob in shoots.values():
           mob[0].hp -= 20
           if mob[0].hp < 0:
               mob[0].death_sound.play()
               mob[0].kill()
               player.points +=10

   if hits:
      #player.points += 10
      #print(player.points)
      pass

   screen.blit(bg, bg_rect)
   all_sprites.draw(screen)             # Рисуем все спрайты на экране

   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           run = False
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_SPACE:
               if player.magazin > 0:
                   player.shoot_sound.play()
                   bullet = Bullet()
                   all_sprites.add((bullet))
                   bullets.add(bullet)
                   player.magazin -= 1
           if event.key == pygame.K_r:
               player.magazin += 15

   if player.hp <= 0:
       run = False
       print('Игра окончена. Вы погибли.')

   drawText(screen, str(player.points), 30, 20, 20, RED)
   drawText(screen, str(player.magazin), 30, 100, 20, CYAN)
   drawText(screen, str(player.hp), 27, width -800, height -975, WHITE)
   pygame.display.flip()
pygame.quit()                           # Закрываем модуль pygame
