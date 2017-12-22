import sys, os, pygame, random
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Инициализируем переменные
# Начальное положение игрока
x_coord = 1
y_coord = 320
# Начальная скорость игрока
x_speed = 0
y_speed = 0
# Количество жизненной энергии игрока
score = 500
# Переменная-счетчик определяет когда
# фигуры изменяют направление движения
shag = 0
# Сдвиги по вертикали для фигур
go1 = 0
go2 = 0


def init_window():
    # Инициализируем pygame
    pygame.init()
    # Создаём игровое окно
    window = pygame.display.set_mode((620, 620))
    # Ставим свой заголовок окна
    pygame.display.set_caption('GeoGame')


# Функция отображения картинок
def load_image(name, colorkey=None):
    # Добавляем к имени картинки имя папки
    fullname = os.path.join('data', name)
    # Загружаем картинку
    image = pygame.image.load(fullname)
    image = image.convert()
    # Если второй параметр =-1 делаем прозрачным
    # цвет из точки 0,0
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def draw_background():
    # Получаем поверхность, на которой будем рисовать
    screen = pygame.display.get_surface()
    # и ее размер
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    # или загружаем картинку
    back, back_rect = load_image("sky.jpg")
    # и рисуем ее
    screen.blit(back, (0, 0))
    # переключаем буфер экрана
    pygame.display.flip()
    return back


# Класс описывающий летающие объекты
class Skything(pygame.sprite.Sprite):
    def __init__(self, img, cX, cY):
        # Создаем спрайт из картинки
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(img, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Перемещаем картинку в её начальные координаты
        self.rect.x = cX
        self.rect.y = cY


# Создаём дочерний класс Player
class Player(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "player.png", cX, cY)


# Создаём дочерний класс Figure
class Figure1(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "krug.png", cX, cY)


class Figure2(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "kvadrat.jpg", cX, cY)


class Money(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "money.png", cX, cY)


def input(events):
    global x_coord, y_coord, x_speed, y_speed, life
    # Перехватываем нажатия клавиш на клавиатуре
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit(0)
        # Когда нажаты стрелки изменяем скорость игрока
        # чтобы оно летело
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a: x_speed = -1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d: x_speed = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w: y_speed = -1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s: y_speed = 1
        # Когда стрелки не нажаты скорость ставим в ноль
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: x_speed = 0
            if event.key == pygame.K_RIGHT: x_speed = 0
            if event.key == pygame.K_UP: y_speed = 0
            if event.key == pygame.K_DOWN: y_speed = 0

    # Меняем положение игрока не выходя за рамки окна
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed
    if (x_coord < 0): x_coord = 0
    if (x_coord > 570): x_coord = 570
    if (y_coord < 0): y_coord = 0
    if (y_coord > 565): y_coord = 565


def action(bk, flag=0, flag2=0):
    global x_coord, y_coord, score, go1, go2
    screen = pygame.display.get_surface()
    # Создаём игрока и фигуры
    money = Money(310, 310)
    player = Player(1, 320)
    krug = Figure1(310, 310)
    kvadrat = Figure2(0, 0)

    # Добавляем их в два массива
    coin = []
    coin.append(money)

    figur = []
    figur.append(krug)
    figur.append(kvadrat)

    fon = []
    fon.append(player)

    # Рисуем их
    moneys = pygame.sprite.RenderPlain(coin)
    figures = pygame.sprite.RenderPlain(figur)
    players = pygame.sprite.RenderPlain(fon)
    timer = pygame.time.Clock()
    # Запускаем бесконечный цикл
    score2 = 0
    while 1:
        # Создаем паузу
        timer.tick(700)
        # Ждём нажатий клавиатуры
        input(pygame.event.get())
        # Проверяем столкновения
        blocks_hit_list = pygame.sprite.spritecollide(player, figures, False)
        blocks_hit_list2 = pygame.sprite.spritecollide(player, moneys, False)
        if len(blocks_hit_list2) > 0:
            score2 += 1
            money.rect.x = random.randint(0, 550)
            money.rect.y = random.randint(0, 550)
        # Если есть столкновения уменьшаем жизнь
        if len(blocks_hit_list) > 0:
            score -= len(blocks_hit_list)
            figures.draw(screen)
            players.draw(screen)
            if score < 1:
               # print(score2)
               # pygame.quit()
                screen = pygame.display.set_mode((620, 620))
                pygame.display.set_caption("GeoGame")
                helloText = "GAME OVER"
                scoreText = "Your score: " + str(score2)
                (x, y, fontSize) = (240, 250, 35)
                myFont = pygame.font.SysFont("None", fontSize)
                fontColor = (255, 255, 0)
                fontImage = myFont.render(helloText, True, (fontColor))
                fontImage2 = myFont.render(scoreText, True, (fontColor))
                mainLoop = True
                while mainLoop:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            mainLoop = False
                    draw_background()
                    screen.blit(fontImage, (x, y))
                    screen.blit(fontImage2, (239, 320))
                    pygame.display.update()

                pygame.quit()
                sys.exit(0)

        # Обновляем координатыssss
        player.rect.x = x_coord
        player.rect.y = y_coord

        # Изменяем положение фигур

        if flag == 0:
            deltax = random.choice([-1, 0, 1])
            deltay = random.choice([-1, 0, 1])
        if flag > 100:
            deltax = random.choice([-1, 0, 1])
            deltay = random.choice([-1, 0, 1])
            flag = 0

        krug.rect.x = krug.rect.x - deltax
        krug.rect.y = krug.rect.y - deltay
        flag += 1

        if (krug.rect.x <= 20): krug.rect.x += 1
        if (krug.rect.x >= 540): krug.rect.x -= 1
        if (krug.rect.y <= 20): krug.rect.y += 1
        if (krug.rect.y >= 540): krug.rect.y -= 1

        if flag2 == 0:
            deltax2 = random.choice([-1, 0, 1])
            deltay2 = random.choice([-1, 0, 1])
        if flag > 100:
            deltax2 = random.choice([-1, 0, 1])
            deltay2 = random.choice([-1, 0, 1])
            flag2 = 0

        kvadrat.rect.x = kvadrat.rect.x - deltax2
        kvadrat.rect.y = kvadrat.rect.y - deltay2
        flag2 += 1

        if (kvadrat.rect.x <= 20): kvadrat.rect.x += 1
        if (kvadrat.rect.x >= 540): kvadrat.rect.x -= 1
        if (kvadrat.rect.y <= 20): kvadrat.rect.y += 1
        if (kvadrat.rect.y >= 540): kvadrat.rect.y -= 1

        # Раз в 300 итераций
        # меняют направление
        # Заново прорисовываем объекты
        screen.blit(bk, (0, 0))
        font = pygame.font.Font(None, 25)
        white = (255, 255, 255)
        life = int(score / 10)
        ball = int(score2)
        text = font.render("Жизнь: " + str(life), True, white)
        text2 = font.render("Score: " + str(ball), True, white)
        # Рисуем надпись с жизнями
        screen.blit(text, [10, 10])
        screen.blit(text2, [200, 10])

        # Обновляем положение объектов
        figures.update()
        players.update()
        moneys.update()
        # Обновляем кадр
        moneys.draw(screen)
        figures.draw(screen)
        players.draw(screen)
        pygame.display.flip()


def main():
    init_window()
    bk = draw_background()
    action(bk)


if __name__ == '__main__':
    main()
