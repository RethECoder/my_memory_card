from pygame import *

' ' 'Required classes' ' '
#parent class for sprites 
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y,size_x,size_y,player_speed):
        super().__init__()
         #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#heir class for the player sprite (controlled by arrows)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        pass
    
lost = 0
score = 0
#heir class for the enemy sprite (moves by itself)
class Enemy(GameSprite):
    def update(self):
        #gerakkan ke bawah
        global lost
        self.rect.y += self.speed
        #kalau sudah di bawah, pindah lagi keatas naikkan nilai miss
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0      
            self.speed = randint(1,5)      
            lost +=1

#Game scene:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

#Game characters:
ship = Player('rocket.png', 5, win_height - 100, 80,100, 4)

from random import randint

monsters = sprite.Group()
for i in range(1, 4):
   monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
   monsters.add(monster)
   monster = Enemy('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(2, 5))
   monsters.add(monster)


game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 50)

#music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background,(0, 0))
        ship.update()
        monsters.update()

        score_text = font.render('Score:0', True, (255, 215, 0))
        window.blit(score_text,(10,20))
        miss_text = font.render('Missed:'+str(lost), True, (180, 0, 0))
        window.blit(miss_text,(10,50))

        ship.reset()
        monsters.draw(window)
        
    display.update()
    clock.tick(FPS)