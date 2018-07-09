import sys
import pygame
import pyganim
from game_objects import Player, Background, Plasmoid, Meteor
from settings import SIZE, WHITE


#Процесс инициализации pygame. Запускается ядро pygame написанное на С
pygame.init()

#Поздороваемся и назовоём окно отображения 'hello world'
pygame.display.set_caption('my_game_2_v_1.0.0')

#Всё что показывается в игре содержится в переменной screen.
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

#Анимация в игре
explosion_anim = pyganim.PygAnimation(
    [('game_data/blue_explosion/1_{}.png'.format(i),50) for i in range(17)], loop = False
)


#Music
music = pygame.mixer.Sound('game_data/music/space.wav')
music.play(-1)


#Создадим группы в которых будем хранить все объекты
all_game_objects = pygame.sprite.Group()
plasmoids = pygame.sprite.Group()
meteors = pygame.sprite.Group()
explosions = []


#Добавляем объекты в нашу игру
player = Player(clock, plasmoids)
back = Background(clock)
plasmoid = Plasmoid(player.rect.midtop)


all_game_objects.add(back)
all_game_objects.add(player)
# all_game_objects.add(plasmoid)
# all_game_objects.add(Meteor())

#тело цикла для игры
while True:
    #Метод pygame.event.get() возвращает массив событий который происходит с окном
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    #Изменяем фон на белый и следующей командой отображаем экран
    screen.fill(WHITE)

    screen.blit(back.image, back.rect)

    # #Отображаем игрока на экран  - передаем в функцию информацию о его изображении
    # # и о его размерах
    # screen.blit(player.image, player.rect)

    Meteor.meteor_process(clock, meteors)

    # Даём возможность движения объектов
    all_game_objects.update()
    plasmoids.update()
    meteors.update()

    #Работа с пересечениями объектов
    meteors_plasmoids_collided = pygame.sprite.groupcollide(plasmoids, meteors, True, True)
    for obj in meteors_plasmoids_collided:
        explosion = explosion_anim.getCopy()
        explosion.play()
        explosions.append((explosion, (obj.rect.center)))

    player_meteor_collided = pygame.sprite.spritecollide(player, meteors, False)

    if player_meteor_collided:
        all_game_objects.remove(player)

    #Прорисовываем объекты на экран
    all_game_objects.draw(screen)
    plasmoids.draw(screen)
    meteors.draw(screen)

    #Отрисовываем взрывы
    for explosion, position in explosions.copy():
        if explosion.isFinished():
            explosions.remove((explosion, position))
        else:
            x, y = position
            explosion.blit(screen, (x - 128, y - 128))

    # #Увеличиваем скорость с течением времени
    # if pygame.time.get_ticks() >= 10000:
    #     back.speed += 0.5


    pygame.display.flip()
    #Ограничим кол-во кадров в секунду
    #а также решим проблему с черезмерно высокой скоростью движения
    clock.tick(60)
