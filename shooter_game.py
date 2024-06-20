#Создай собственный Шутер!

from pygame import *

mixer.init()

from random import *

font.init()

window = display.set_mode((700,500))
display.set_caption('shooter')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
clock = time.Clock()

mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

miss = 0

class game_sprite(sprite.Sprite):
    def __init__(self,x,y,width,height,speed,player_image):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def blit(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class player(game_sprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 20:
            self.rect.x -= self.speed
    def fire(self):
        blt = bullet(self.rect.centerx,self.rect.top,5,10,20,'bullet.png')
        bullets.add(blt)
        fire_sound.play()

class enemy(game_sprite):
    def update(self):
        global miss 
        self.rect.y += self.speed
        if self.rect.y > 710:
            self.rect.x = randint(20,630)
            self.rect.y = 0
            miss += 1
class bullet(game_sprite):
    def update(self): 
        self.rect.y -= self.speed
        if self.rect.y <  0:
            self.kill()

enemies = sprite.Group()
for i in range(5):
    Enemy = enemy(randint(20,630),0,70,50,randint(1,6),'ufo.png')
    enemies.add(Enemy)

rocket = player(330,430,50,60,10,'rocket.png')

C_D_O = 0

bullets = sprite.Group()

lose = font.SysFont('Arial',80).render('ИГРА ОКОНЧЕНА!',True,(255,0,0))
win = font.SysFont('Arial',80).render('ИГРА ВЫИГРАНА!',True,(0,255,0))

finish = False
game = True
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    if not finish:

        window.blit(background,(0,0))

        rocket.blit()
        rocket.move()

        enemies.update()
        enemies.draw(window)

        total_score = font.SysFont('Arial', 25).render('Счёт:'+str(C_D_O),True,(255,255,255))
        missed_score = font.SysFont('Arial', 25).render('Пропущено:'+str(miss),True,(255,255,255))
        window.blit(total_score,(10,20))
        window.blit(missed_score,(10,40))

        if C_D_O >= 10:
            window.blit(win,(130,200))
            finish = True

        collides =  sprite.groupcollide(enemies,bullets,True,True)
        for i in collides:
            C_D_O += 1
            Enemy = enemy(randint(20,630),0,70,50,randint(1,6),'ufo.png')
            enemies.add(Enemy)

        if sprite.spritecollide(rocket,enemies,False) or miss >= 3:
            window.blit(lose,(130,200))
            finish = True

        bullets.update()
        bullets.draw(window)

    display.update()
    time.delay(50)