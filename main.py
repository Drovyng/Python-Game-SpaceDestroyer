
# pip install windows-curses keyboard

import curses, keyboard, random

screen = curses.initscr()

def str2meteor(text:str):
    obj = []
    y = -1
    for line in text.split("\n"):
        y = y + 1
        x = -1
        for c in line:
            x = x + 1
            if c != ' ':
                obj.append([y, x])
    return obj

meteors_types = [
    str2meteor(
        " ### \n"+
        " ### \n"+
        " ### "
    ),
    str2meteor(
        " ### \n"+
        " # # \n"+
        " ### "
    ),
    str2meteor(
        "  ## \n"+
        "  ## "
    ),
    str2meteor(
        " ##  \n"+
        " ##  "
    ),
    str2meteor(
        " ### \n"+
        "#####\n"+
        "## ##\n"+
        "#####\n"+
        " ### "
    ),
    str2meteor(
        " ### \n"+
        "## ##\n"+
        "#   #\n"+
        "## ##\n"+
        " ### "
    ),
    str2meteor(
        "  #  \n"+
        " ### \n"+
        "#####\n"+
        " ### \n"+
        "  #  "
    ),
    str2meteor(
        "  #  \n"+
        " ### \n"+
        "## ##\n"+
        " ### \n"+
        "  #  "
    ),
]

pos = 26
posY = 0
projectiles = []
meteors = []
stars = [[y+random.random(), random.randint(0, 50)] for y in range(0, 31, 2)]
reload = 0
spawn_reload = 1
hp = 100
score = 0
paused = False
fire_mode = 0
fire_what = False
game_overed = False

def spawn_meteor():
    global meteors, meteors_types, spawn_reload
    obj = random.choice(meteors_types)
    spawn_reload = len(obj)*15 + 60
    x = random.randint(4, 41)
    meteors = meteors + [[30+part[0], x+part[1]] for part in obj]

def prt(y, x, text):
    screen.addstr(y, x+3, text)
#    if len(params) == 3 and params[0] >= 30: return

def pressed(key):
    return keyboard.is_pressed(key)

def fire():
    return random.choice(["$", "&", "[", "}", "!"])

#     /\
#    (  )
#    (  )
#   /|/\|\
#  /_||||_\
#
#  But vertical flip
#
# https://www.asciiart.eu/text-to-ascii-art
# "ANSI Shadow" - Font
#
paused_text = """
██████╗  █████╗ ██╗   ██╗███████╗███████╗██████╗ 
██╔══██╗██╔══██╗██║   ██║██╔════╝██╔════╝██╔══██╗
██████╔╝███████║██║   ██║███████╗█████╗  ██║  ██║
██╔═══╝ ██╔══██║██║   ██║╚════██║██╔══╝  ██║  ██║
██║     ██║  ██║╚██████╔╝███████║███████╗██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═════╝ 
""".split("\n")
gameover_text = """
 ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ ██╗
██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗██║
██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝██║
██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚═╝
╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║██╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝
""".split("\n")


def pause():
    global paused, game_overed
    if game_overed: return
    paused = not paused
    if paused:
        i = 0
        for line in paused_text:
            prt(11+i, 1, line)
            i = i + 1
        screen.refresh()

def game_over():
    global paused, game_overed
    paused = game_overed = True

    i = 0
    for line in gameover_text:
        prt(11+i, 17, line)
        i = i + 1
    screen.refresh()

keyboard.on_press_key("space", lambda pause1: pause())
keyboard.on_press_key("enter", lambda pause2: pause())

def firemode():
    global fire_mode
    fire_mode = (fire_mode + 1) % 4

keyboard.on_press_key("s", lambda firemode1: firemode())
keyboard.on_press_key("down", lambda firemode2: firemode())

while True:
    if paused or game_overed:
        curses.napms(100)
        continue

    curses.napms(16)
    screen.clear()

    if reload > 0: reload = reload - 1
    if spawn_reload > 0:
        spawn_reload = spawn_reload - 1
        if spawn_reload == 0:
            spawn_meteor()
    
    if pressed("a") or pressed("left"):
        pos = pos - 0.4
    if pressed("d") or pressed("right"):
        pos = pos + 0.4
    pos = min(max(pos, 0), 43)
    if reload == 0 and (pressed("w") or pressed("up")) and ((fire_mode==2 and score >= 1.1) or (fire_mode==3 and score >= 2.5) or fire_mode < 2):
        reload = 10
        if fire_mode == 1:
            fire_what = not fire_what
            projectiles.append([posY+6, int(pos)+(3 if fire_what else 4), 1, 1])
            reload = 5
        elif fire_mode == 2:
            projectiles.append([posY+6, int(pos)+3, 40, 1.5])
            projectiles.append([posY+5, int(pos)+3, 40, 1.5])
            projectiles.append([posY+6, int(pos)+4, 40, 1.5])
            projectiles.append([posY+5, int(pos)+4, 40, 1.5])
            score = score - 1.1
        elif fire_mode == 3:
            for i in range(5, 30):
                projectiles.append([posY+i, int(pos)+3, 40, 10])
                projectiles.append([posY+i, int(pos)+4, 40, 10])
            score = score - 2.5
            reload = 60
        else:
            projectiles.append([posY+6, int(pos)+3, 1, 1])
            projectiles.append([posY+6, int(pos)+4, 1, 1])

    for i in range(len(stars)):
        y, x = stars[i]
        py = int(y)
        y = y - 0.02
        if y < 30:
            prt(int(y), x, "*")
        if y < 0:
            x = random.randint(0, 50)
            y = 30 + random.random()
        stars[i] = [y, x]

    i = 0
    while i < len(meteors):
        y, x = meteors[i]
        y = y - 0.075
        if y < 0:
            hp = hp - random.randint(2, 5)
            meteors.remove(meteors[i])
            continue
        if y < 30:
            prt(int(y), x, "%")
        meteors[i] = [y, x]
        i = i + 1

    i = 0
    while i < len(projectiles):
        y, x, l, s = projectiles[i]
        y = y + 0.5 * s
        meteorsInt = [[int(m[0]), m[1]] for m in meteors]
        p1 = [int(y), x]
        p1 = meteorsInt.index(p1) if p1 in meteorsInt else -1
        if p1 != -1:
            meteors.remove(meteors[p1])
            score = score + 0.2
            l = l - 1
        if l == 0 or y >= 30:
            projectiles.remove(projectiles[i])
            continue
        projectiles[i] = [y, x, l, s]
        prt(int(y), x, "|")
        i = i + 1

    posI = int(pos)

    prt(posY, posI+6, fire())
    prt(posY, posI+1, fire())

    for i in [0,1,2,5,6,7]:
        prt(posY+1, posI+i, fire())

    prt(posY+2, posI, "\\_||||_/")
    prt(posY+3, posI+1,  "\\|\\/|/")
    prt(posY+4, posI+2,      "(  )")
    prt(posY+5, posI+2,      "(  )")
    prt(posY+6, posI+3,    "\\/")

    if hp < 0:
        hp = 0

    score = score + 0.002

    prt(1, 60, "STATS:")
    prt(3, 55, "HP:         "+(" " if hp < 100 else "")+(" " if hp < 10 else "")+str(hp))
    prt(5, 55, "SCORE:  " + (" " if score < 10000 else "") + (" " if score < 1000 else "") + (" " if score < 100 else "") + (" " if score < 10 else "") + f"{int(score)}.{int(score*10) % 10}")

    prt(7, 55,  f"FR-MD:   {["DOUBLE", "  FAST", " POWER", " LASER"][fire_mode]}")
    if fire_mode > 1:
        prt(8, 57,  f"*REQ SCORE*")

    prt(19, 58, "CONTROLS:")
    prt(21, 55, "S, ↓      FR-MD")
    prt(23, 55, "A, ←       LEFT")
    prt(24, 55, "D, →      RIGHT")
    prt(25, 55, "W, ↑      SHOOT")
    prt(27, 55, "SPACE     PAUSE")
    prt(28, 55, "ENTER     PAUSE")

    for i in range(30):
        prt(i, -2, "|")
        prt(i, 52, "|")
        prt(i, 72, "|")


    screen.refresh()

    if hp == 0:
        game_over()