import pygame as pg
from settings import WIDTH, HEIGHT
import random

clock = pg.time.Clock()

#Создаём класс игрока и наследуемся явно и неявно от класса спрайт в пигейме
class Player(pg.sprite.Sprite):
    max_speed = 10
    shouting_cooldown = 150

    def __init__(self, clock, plasmoids):
        super(Player, self).__init__()

        self.clock = clock
        self.plasmoids = plasmoids

        self.image = pg.image.load('game_data/player.png')
        self.rect = self.image.get_rect() #устанавливаем размеры объекта равные размеру картинки
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.current_speed = 0
        self.current_shouting_cooldown = 0
        self.plasmoid_sound = pg.mixer.Sound('game_data/sounds/plasma_bolt.wav')

    def update(self):
        #команда захвата нажатых клавиш
        key = pg.key.get_pressed()

        if key[pg.K_LEFT]:
            self.current_speed = -self.max_speed
        elif key[pg.K_RIGHT]:
            self.current_speed = self.max_speed
        else:
            self.current_speed = 0
        #Задаём смещение относительно текущей точки
        self.rect.move_ip((self.current_speed, 0))

        self.shouting()

    def shouting(self):
        #Захват нажатия клавиш
        key = pg.key.get_pressed()

        if key[pg.K_SPACE] and self.current_shouting_cooldown <= 0:
            self.plasmoid_sound.play()
            self.plasmoids.add(Plasmoid(self.rect.midtop))
            self.current_shouting_cooldown = self.shouting_cooldown
        else:
            self.current_shouting_cooldown -= self.clock.get_time()
        for plasmoid in list(self.plasmoids):
            if plasmoid.rect.bottom < 0:
                self.plasmoids.remove(plasmoid)

class Background(pg.sprite.Sprite):
    speed = 4

    def __init__(self, clock):
        super(Background, self).__init__()

        self.clock = clock

        self.image = pg.image.load('game_data/background.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT

    def update(self):
        # self.rect.bottom += 2
        #
        # if self.rect.bottom >= self.rect.height:
        #     self.rect.bottom = HEIGHT
        self.rect.move_ip((0, self.speed))

        if self.rect.bottom >= self.rect.height:
            self.rect.bottom = HEIGHT


class Plasmoid(pg.sprite.Sprite):
    speed = -7

    def __init__(self, position):
        super(Plasmoid, self).__init__()

        self.image = pg.image.load('game_data/plasmoid.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = position

    def update(self):
        self.rect.move_ip((0, self.speed))

class Meteor(pg.sprite.Sprite):
    cooldown = 1200
    curent_cooldown = 0
    speed = 7

    def __init__(self):
        super(Meteor, self).__init__()

        image_name = 'game_data/meteor{}.png'.format(random.randint(1, 6))
        self.image = pg.image.load(image_name)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (random.randint(0, WIDTH), 0)

    def update(self):
        self.rect.move_ip((0, self.speed))

    @staticmethod
    def meteor_process(clock, meteors):
        if Meteor.curent_cooldown <= 0:
            meteors.add(Meteor())
            Meteor.curent_cooldown = Meteor.cooldown
        else:
            Meteor.curent_cooldown -= clock.get_time()

        for meteor in list(meteors):
            if (meteor.rect.right < 0 or
                meteor.rect.left > WIDTH or
                meteor.rect.top > (HEIGHT)):
                meteors.remove(meteor)
