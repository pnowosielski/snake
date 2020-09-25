from __future__ import print_function
import sys
import time
import WConio2
from collections import deque
import random

a = 50  # y
b = 100  # x
x = int(b / 2)
y = int(a / 2)
# inicjacja glowy weza
wonsz = deque()
score = 1

granica_poziom = ' _'
granica_pion = ' |'
field = ' .'
znak_weza = ' x'
bonus = ' $'
kamien = '--'
kill_water = '  '

sleep_time = 0.12
bonus_count = 20
kamien_count = 10
runda = 100

UP = ['w', 'up']
DOWN = ['s', 'down']
LEFT = ['a', 'left']
RIGHT = ['d', 'right']
POZIOM = []; POZIOM.extend(LEFT); POZIOM.extend(RIGHT)
PION = []; PION.extend(UP); PION.extend(DOWN)

plansza = [[field for j in range(a)] for i in range(b)]
for aa in range(a):
    plansza[0][aa] = granica_pion
    plansza[b - 1][aa] = granica_pion
for bb in range(b):
    plansza[bb][0] = granica_poziom
    plansza[bb][a - 1] = granica_poziom


def bonus_init(i=10):
    # for j in range(a):
    #     for k in range(b):
    #         if plansza[k][j] == bonus:
    #             plansza[k][j] = field
    #             WConio2.gotoxy(k * 2, j)
    #             WConio2.cputs("%s" % field)

    WConio2.textbackground(WConio2.GREEN)
    WConio2.textcolor(WConio2.WHITE)
    for ii in range(i):
        ra = random.choice(range(a - 2)) + 1
        rb = random.choice(range(b - 2)) + 1
        # plansza[rb][ra] = bonus
        if (plansza[rb][ra] != znak_weza):
            plansza[rb][ra] = bonus
            WConio2.gotoxy(rb * 2, ra)
            WConio2.textbackground(WConio2.BLACK)
            WConio2.cputs("%s" % bonus[0])
            WConio2.textbackground(WConio2.GREEN)
            WConio2.cputs("%s" % bonus[1])
            # WConio2.cputs("%s" % bonus)
    WConio2.textbackground(WConio2.BLACK)
    WConio2.textcolor(WConio2.GREEN)


def kamien_init(i=10):
    # for j in range(a):
    #     for k in range(b):
    #         if plansza[k][j] == kamien:
    #             plansza[k][j] = field
    #             WConio2.gotoxy(k * 2, j)
    #             WConio2.cputs("%s" % field)

    WConio2.textbackground(WConio2.RED)
    WConio2.textcolor(WConio2.WHITE)
    for ii in range(i):
        ra = random.choice(range(a - 2)) + 1
        rb = random.choice(range(b - 2)) + 1
        # plansza[rb][ra] = kamien
        if plansza[rb][ra] != znak_weza:
            plansza[rb][ra] = kamien
            WConio2.gotoxy(rb * 2, ra)
            WConio2.cputs("%s" % kamien)
    WConio2.textbackground(WConio2.BLACK)
    WConio2.textcolor(WConio2.GREEN)


def update_wonsz(nx, ny, increaseL=0):
    # rysuje glowe
    wonsz.append([nx, ny])
    plansza[nx][ny] = znak_weza
    WConio2.gotoxy(nx * 2, ny)
    WConio2.textcolor(WConio2.WHITE)
    WConio2.cputs("%s" % znak_weza)
    # ewentualnie kasuje ogon jak wonsz nie ma juz rosnac
    if (increaseL <= 0) and (len(wonsz) > 8):
        ogon = wonsz.popleft()
        plansza[ogon[0]][ogon[1]] = kill_water
        WConio2.gotoxy(ogon[0] * 2, ogon[1])
        WConio2.textcolor(WConio2.GREEN)
        WConio2.cputs("%s" % kill_water)
    elif (increaseL > 0) and (len(wonsz) > 8):
        increaseL = increaseL - 1
    return increaseL


def print_plansza():
    WConio2.textcolor(WConio2.GREEN)
    WConio2.gotoxy(0, 0)
    for j in range(a):
        for i in range(b):
            WConio2.cputs("%s" % plansza[i][j])  # print(" %s " % plansza[i][j], end='')
        WConio2.cputs("\n")  # print('\n')


def next_step(cx, cy, okey, nkey=None):
    """
    wyzanczenie nowego kierunku ruchu, lub zignorowanie wcisnietego klwisza
    :param cx: aktualnyX
    :param cy: aktualnyY
    :param okey: obecnyKierunek
    :param nkey: nowyKierunek
    :return: nowa pozycja i nowy kierunek
    """

    # zabezpieczenie przed naciskaniem byle jkich klwiszy
    if (nkey is None) or (nkey not in ['w', 'up', 's', 'down', 'a', 'left', 'd', 'right']):
        nkey = okey
    if ((nkey in UP) and (okey in DOWN)) or \
            ((nkey in DOWN) and (okey in UP)) or \
            ((nkey in LEFT) and (okey in RIGHT)) or \
            ((nkey in RIGHT) and (okey in LEFT)):
        nkey = okey  # zabezpieczenie przed 'cofaniem sie'

    xx = cx
    yy = cy

    if nkey in UP:
        xx = cx
        yy = cy - 1
        if yy < 0:
            yy = a -1

    if nkey in DOWN:
        xx = cx
        yy = (cy + 1) % a  # modulo - opcja na pojawianie sie weza z drugiej strony ekranu
    if nkey in LEFT:
        xx = (cx - 1)
        if xx < 0:
            xx = b-1
        yy = cy
    if nkey in RIGHT:
        xx = (cx + 1) % b
        yy = cy
    return xx, yy, nkey


def end_game():
    WConio2.textbackground(WConio2.LIGHTRED)
    WConio2.textcolor(WConio2.WHITE)
    WConio2.gotoxy(x*2,y )
    WConio2.cputs(' GAME OVER ')

    print_score(score, 0, 0)

    WConio2.gotoxy(t10, t11 - 1)
    WConio2.textbackground(WConio2.BLACK)
    WConio2.textattr(WConio2.NORM_ATTR)
    WConio2.setcursortype(1)
    sys.exit(1)


def debug(pozx=0, pozy=0, msg=""):
    WConio2.gotoxy(pozx, pozy)
    WConio2.cputs(msg)
    # time.sleep(0.2)


def print_score(score, pozx=0, pozy=0):
    WConio2.textcolor(WConio2.WHITE)
    WConio2.gotoxy(pozx, pozy)
    WConio2.cputs("Your scrore: " + str(score) + " ")


if __name__ == "__main__":
    WConio2.setcursortype(0)
    WConio2.textattr(WConio2.GREEN)
    WConio2.lowvideo()
    WConio2.clrscr()
    print_plansza()
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11 = WConio2.gettextinfo()

    nr = 0
    direction = 'up'
    increase = 0

    update_wonsz(x, y)  # young snake

    while True:
        if nr % runda == 0:  # kolejne dosypanie klamieni oraz bonusów + przyspieszenie weza
            bonus_init(bonus_count)
            kamien_init(kamien_count)
            kamien_count = nr // runda
            bonus_count = bonus_count // 2
            sleep_time = 0.02 if (sleep_time - 0.01) < 0.02 else (sleep_time - 0.01)
        nr += 1
        time.sleep(sleep_time)

        tmpx = x
        tmpy = y

        if WConio2.kbhit():
            x, y, direction = next_step(x, y, direction, WConio2.getkey())
        else:
            x, y, direction = next_step(x, y, direction)

        head_wonsz = plansza[x][y]

        # debug(100, 0, "   %s %s %s %s           " % (x, y, head_wonsz, direction))
        zaglodzenie = 0
        while (head_wonsz in [kamien, granica_pion, granica_poziom, znak_weza]) and zaglodzenie <30:
            # WConio2.gotoxy(tmpx*2,tmpy)
            # WConio2.textbackground(WConio2.BLUE)
            # WConio2.cputs("%s" % "??") ; time.sleep(0.1)
            # WConio2.textbackground(WConio2.BLACK)
            if direction in UP:
                new_direction = random.choice(POZIOM)
            if direction in DOWN:
                new_direction = random.choice(POZIOM)
            if direction in RIGHT:
                new_direction = random.choice(PION)
            if direction in LEFT:
                new_direction = random.choice(PION)
            x, y, direction = next_step(tmpx, tmpy, direction, new_direction)
            # debug(100,1,"   %s, %s, >>%s<<  new_direction: %s         " % (x, y, plansza[x][y], new_direction) )
            head_wonsz = plansza[x][y]
            zaglodzenie +=1

        increase = update_wonsz(x, y, increase)  # ### Przesuwanie wonsza ###

        if head_wonsz in [znak_weza, granica_pion, granica_poziom, kamien]:  # end game?
        # if head_wonsz in [znak_weza, kamien]:  # end game?
            end_game()

        if head_wonsz == field:
            score += 1

        if head_wonsz == bonus:
            # x, y, direction = next_step(x, y, direction)
            # increase = update_wonsz(x, y, increase + 8)
            increase += 8
            score += 20

        print_score(str(score) + " Level: " + str(nr // runda + 1))
