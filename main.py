import json
import pygame
import random
from pygame import mixer
from fighter import Fighter
from network_online import Network_Online
from player import Player
from network_io import Network_IO
mixer.init()
pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Game Multiplayer")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
#Khai báo biến Kingdom.IO-------------------------------------------------------
#Constant
PLAYER_RADIUS = 10
START_VEL = 9
BALL_RADIUS = 5

#Font
NAME_FONT = pygame.font.SysFont("comicsans", 20)
TIME_FONT = pygame.font.SysFont("comicsans", 30)
SCORE_FONT = pygame.font.SysFont("comicsans", 26)

#Color
COLORS = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0),
          (0, 255, 128), (0, 255, 255), (0, 128, 255), (0, 0, 255), (0, 0, 255),
          (128, 0, 255), (255, 0, 255), (255, 0, 128), (128, 128, 128), (0, 0, 0)]
#-------------------------------------------------------------------------------
# Dynamic Variables
players = {}
balls = []
# Biến đếm và cập nhật countdown
intro_count = 3 
last_count_update = pygame.time.get_ticks()

# Điểm số và các biến liên quan
score = [0, 0] 
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [76,56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

MARTIALHERO_SIZE = 200
MARTIALHERO_SCALE = 3.45
MARTIALHERO_OFFSET = [85, 71.5]
MARTIALHERO_DATA = [MARTIALHERO_SIZE, MARTIALHERO_SCALE, MARTIALHERO_OFFSET]

KNIGHT_SIZE = 180
KNIGHT_SCALE = 3.45
KNIGHT_OFFSET = [78, 62.7]
KNIGHT_DATA = [KNIGHT_SIZE, KNIGHT_SCALE, KNIGHT_OFFSET]

# Load âm nhạc và âm thanh
pygame.mixer.music.load("assets/audio/music1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)
knight_fx = pygame.mixer.Sound("assets/audio/knight.mp3")
knight_fx.set_volume(0.75)
KO_fx = pygame.mixer.Sound("assets/audio/ko.mp3")
KO_fx.set_volume(0.5)
P1_win_fx = pygame.mixer.Sound("assets/audio/player-1-wins.mp3")
P1_win_fx.set_volume(0.25)
P2_win_fx = pygame.mixer.Sound("assets/audio/player-2-wins.mp3")
P2_win_fx.set_volume(0.25)

# Các biến menu và map
main_menu = True
map_menu = False
map_selected = False
sound_played = False
map_selected_index = None  # Thêm biến lưu chỉ số map được chọn
player_selection = 0

#load background image
title = pygame.image.load("assets/images/background/NameGame.png").convert_alpha()
bg_image_main = pygame.image.load("assets/images/background/background9.jpg").convert_alpha()  

choose_character_1 = pygame.image.load("assets/images/background/character1.png").convert_alpha()
choose_character_1 = pygame.transform.scale(choose_character_1, (275, 275))
choose_character_2 = pygame.image.load("assets/images/background/character2.png").convert_alpha()
choose_character_2 = pygame.transform.scale(choose_character_2, (250, 250))
choose_character_3 = pygame.image.load("assets/images/background/character3.png").convert_alpha()
choose_character_3 = pygame.transform.scale(choose_character_3, (200, 200))
choose_character_4 = pygame.image.load("assets/images/background/character4.png").convert_alpha()
choose_character_4 = pygame.transform.scale(choose_character_4, (250, 250))  

#Map image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
bg_image1 = pygame.image.load("assets/images/background/background1.jpg").convert_alpha()
bg_image2 = pygame.image.load("assets/images/background/background8.jpg").convert_alpha()
bg_image3 = pygame.image.load("assets/images/background/background7.jpg").convert_alpha()
bg_image4 = pygame.image.load("assets/images/background/background4.jpg").convert_alpha()
bg_image5 = pygame.image.load("assets/images/background/background6.jpg").convert_alpha() 

bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
start_img = pygame.image.load('assets/images/background/start.png').convert_alpha()
exit_img = pygame.image.load('assets/images/background/exit.png').convert_alpha()
restart_img = pygame.image.load('assets/images/background/restart.png').convert_alpha()
main_menu_img = pygame.image.load('assets/images/background/main_menu.png').convert_alpha()


#load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
martialhero_sheet = pygame.image.load("assets/images/martialhero/Sprites/martialhero.png").convert_alpha()
knight_sheet = pygame.image.load("assets/images/knight/Sprites/knight.png").convert_alpha()

#load vitory image
P1Victory_img = pygame.image.load("assets/images/icons/p1win.png").convert_alpha()
P2Victory_img = pygame.image.load("assets/images/icons/p2win.png").convert_alpha()
K_O_img = pygame.image.load("assets/images/icons/K.O.png").convert_alpha()

#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
MARTIALHERO_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]
KNIGHT_ANIMATION_STEPS = [11, 8, 3, 7, 7, 4, 11]  

#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 50)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4]), int(str[5])
    
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4])+ "," + str(tup[5])

# Hàm vẽ giao diện chơi online
def redrawWindow(win, player, player2):
    win.fill((255, 255, 255))
    draw_bg(pygame.transform.scale(bg_image1, (SCREEN_WIDTH, SCREEN_HEIGHT)))
    player.draw(win)
    player2.draw(win)
    player.draw_health_bar(win,20,20)
    player.draw_mana_bar(win,20,55)
    player2.draw_health_bar(win,580,20)
    player2.draw_mana_bar(win,580,55)
    pygame.display.update()
#Kết nối server chơi online
def play_online():
    run = True
    n = Network_Online()
    startPos = read_pos(n.getData())
    p = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0), 1, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    p.health = startPos[2]
    p2 = Player(0, 0, 100, 100, (255, 0, 0), 2, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    clock = pygame.time.Clock()
    intro_count = 3 
    last_count_update = pygame.time.get_ticks()

    while run:
        clock.tick(60)
        # Nhận dữ liệu từ mạng
        p2Pos = read_pos(n.send(make_pos((p.x, p.y, p.health, p.mana, p.action, p.frame_index))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.health = p2Pos[2]
        p2.mana = p2Pos[3]
        p2.action = p2Pos[4]
        p2.frame_index = p2Pos[5]
       
        p2.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if intro_count <= 0:
            p.move(SCREEN_WIDTH, SCREEN_HEIGHT, p2, False)
        else:
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 50)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        p.update()
        redrawWindow(screen, p, p2)


    
#Kết nối chơi Kingdom.IO
def convert_time(t):
    if type(t) == str:
        return t

    if int(t) < 60:
        return str(t) + "s"
    else:
        minutes = str(t // 60)
        seconds = str(t % 60)

        if int(seconds) < 10:
            seconds = "0" + seconds

        return minutes + ":" + seconds
    
def redraw_window_io(players, balls, game_time, score):
    screen.fill((255, 255, 255))  # fill screen white, to clear old frames
    
    # draw all the orbs/balls
    for ball in balls:
        pygame.draw.circle(screen, ball[2], (ball[0], ball[1]), BALL_RADIUS)

    # draw each player in the list
    for player in sorted(players, key=lambda x: players[x]["score"]):
        p = players[player]
        pygame.draw.circle(screen, p["color"], (p["x"], p["y"]), PLAYER_RADIUS + round(p["score"]))
        # render and draw name for each player
        text = NAME_FONT.render(p["name"], 1, (0, 0, 0))
        screen.blit(text, (p["x"] - text.get_width() / 2, p["y"] - text.get_height() / 2))

    # draw scoreboard
    sort_players = list(reversed(sorted(players, key=lambda x: players[x]["score"])))
    title = TIME_FONT.render("Scoreboard", 1, (0, 0, 0))
    start_y = 25
    x = SCREEN_WIDTH - title.get_width() - 10
    screen.blit(title, (x, 5))

    ran = min(len(players), 3)
    for count, i in enumerate(sort_players[:ran]):
        text = SCORE_FONT.render(str(count + 1) + ". " + str(players[i]["name"]), 1, (0, 0, 0))
        screen.blit(text, (x, start_y + count * 20))

    # draw time
    text = TIME_FONT.render("Time: " + convert_time(game_time), 1, (0, 0, 0))
    screen.blit(text, (10, 10))
    # draw score
    text = TIME_FONT.render("Score: " + str(round(score)), 1, (0, 0, 0))
    screen.blit(text, (10, 15 + text.get_height()))
    
def draw_name_input():
    input_box = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 25, 200, 50)
    font = pygame.font.SysFont("comicsans", 30)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    play_button = pygame.Rect(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 + 50, 100, 50)
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                if play_button.collidepoint(event.pos) and 0 < len(text) < 20:
                    return text
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if 0 < len(text) < 20:
                            return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((255, 255, 255))
        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        play_text = font.render("Play", True, (0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), play_button)
        screen.blit(play_text, (play_button.x + (play_button.width - play_text.get_width()) // 2,
                            play_button.y + (play_button.height - play_text.get_height()) // 2))

        pygame.display.flip()

def  play_online_io(name):
    global players
    # start by connecting to the network
    server = Network_IO()
    current_id = server.connect(name)
    balls, players, game_time = server.send("get")

    # setup the clock, limit to 30fps
    clock = pygame.time.Clock()

    run = True

    # Initialize movement direction
    dx, dy = START_VEL, 0

    while run:
        clock.tick(30)  # 30 fps max
        player = players[current_id]
        vel = START_VEL - round(player["score"] / 14)
        if vel <= 1:
            vel = 1

        # get key presses
        keys = pygame.key.get_pressed()

        data = ""
        # Update direction based on key presses
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx, dy = -vel, 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx, dy = vel, 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dx, dy = 0, -vel

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dx, dy = 0, vel

        # Update player position based on direction
        if 0 <= player["x"] + dx <= SCREEN_WIDTH:
            player["x"] += dx
        if 0 <= player["y"] + dy <= SCREEN_HEIGHT:
            player["y"] += dy

        data = "move " + str(player["x"]) + " " + str(player["y"])

        # send data to server and receive back all players information
        balls, players, game_time = server.send(data)

        for event in pygame.event.get():
            # if user hits red x button close window
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # if user hits a escape key close program
                if event.key == pygame.K_ESCAPE:
                    run = False

        # redraw window then update the frame
        redraw_window_io(players, balls, game_time, player["score"])
        pygame.display.update()

    server.disconnect()
    pygame.quit()
    quit()
   
# Hàm vẽ chữ
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for drawing background
def draw_bg(scaler_bg):
    screen.blit(scaler_bg,(0, 0))

# Hàm vẽ map select
def draw_map(map_list):
    for i, map_image in enumerate(map_list):
        x = 150 + (i % 3) * 250
        y = 100 + (i // 3) * 180
        scaler_bg = pygame.transform.scale(map_image, (200, 120))
        screen.blit(scaler_bg, (x, y))
        if map_selected_index == i:  # Vẽ border cho map được chọn
            pygame.draw.rect(screen, (255, 255, 0), (x - 5, y - 5, 210, 130), 3)

# Hàm vẽ nền cho map được chọn
def draw_map_select(map_image):
    draw_bg(pygame.transform.scale(map_image, (SCREEN_WIDTH, SCREEN_HEIGHT)))
    
# Hàm vẽ thanh máu và mana
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))
            
def draw_mana_bar(mana, x, y):
    ratio = mana / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 204, 8))
    pygame.draw.rect(screen, BLUE, (x, y, 200 * ratio, 5))

def character_selection_screen():
    global player_selection
    selected_character = None
    while selected_character is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if warrior_button_rect.collidepoint(x, y):
                    selected_character = "Warrior"
                    player_selection = 1
                elif wizard_button_rect.collidepoint(x, y):
                    selected_character = "Wizard"
                    player_selection = 2
                elif martialhero_button_rect.collidepoint(x, y):
                    selected_character = "Hero"
                    player_selection = 3
                elif knight_button_rect.collidepoint(x, y):
                    selected_character = "Knight"
                    player_selection = 4

        if player_selection == 1:
            screen.fill((0, 0, 0), (SCREEN_WIDTH / 2 - 170, 50, 340, 50))
            draw_text("Select Player "+ str(player_selection), count_font, RED, SCREEN_WIDTH / 2 - 170, 50)
        elif player_selection == 2:
            screen.fill((0, 0, 0), (SCREEN_WIDTH / 2 - 170, 50, 340, 70))
            draw_text("Select Player "+ str(player_selection), count_font, RED, SCREEN_WIDTH / 2 - 170, 50)
        else:
            draw_text("Select Player ", count_font, RED, SCREEN_WIDTH / 2 - 170, 50)

       
        warrior_button_rect = pygame.Rect(50, 100, 200, 200)
        screen.blit(choose_character_1, warrior_button_rect)
        if player_selection == 1:
            draw_text("Warrior", count_font, RED, 120, 270)
        else:
            draw_text("Warrior", count_font, WHITE, 120, 270)


        wizard_button_rect = pygame.Rect(580, 50, 200, 200)
        screen.blit(choose_character_2, wizard_button_rect)
        if player_selection == 2:
            draw_text("Wizard", count_font, RED, 620, 270)
        else:
            draw_text("Wizard", count_font, WHITE, 620, 270)
        
        martialhero_button_rect = pygame.Rect(580, 350, 200, 200)
        screen.blit(choose_character_3, martialhero_button_rect)
        if player_selection == 3:
            draw_text("Hero", count_font, RED, 620, 520)
        else:
            draw_text("Hero", count_font, WHITE, 620, 520)
        
        knight_button_rect = pygame.Rect(50, 350, 200, 200)
        screen.blit(choose_character_4, knight_button_rect)
        if player_selection == 4:
            draw_text("Knight", count_font, RED, 120, 520)
        else:
            draw_text("Knight", count_font, WHITE, 120, 520)
          

        pygame.display.update()
        clock.tick(FPS)

    return selected_character  


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        
    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check mouse over and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        #draw button
        screen.blit(self.image, self.rect)
        
        return action
    
# Tạo nhân vật và các button
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

title_game = Button(SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 15, title)
start_button = Button(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 4, start_img)
start_button_online = Button(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 2.5, start_img)
start_button_io = Button(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 1.85, start_img)
exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 1.5, exit_img)
restart_button = Button(SCREEN_WIDTH // 2 - 165, SCREEN_HEIGHT // 2 - 50, restart_img)
main_menu_button = Button(SCREEN_WIDTH // 2 + 65, SCREEN_HEIGHT // 2 - 50, main_menu_img)

# game loop 
run = True
while run:
    
    clock.tick(FPS)
    
    #draw background
    draw_bg(pygame.transform.scale(bg_image_main, (SCREEN_WIDTH,SCREEN_HEIGHT)))
    
    if main_menu:
        title_game.draw()
        if start_button.draw():
            map_menu = True
            main_menu = False
        if start_button_online.draw():
            main_menu = False
            play_online()
        if start_button_io.draw():
            main_menu = False
            name = draw_name_input()
            play_online_io(name)
        if exit_button.draw():
            run = False
    elif map_menu:
        draw_text("Choose your map", count_font, WHITE,SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 15)
        draw_map([bg_image, bg_image1, bg_image2, bg_image3, bg_image4, bg_image5])  # Thêm 3 bản đồ mới
        # Thêm phần xử lý khi map được chọn
        if map_selected_index is not None:
            map_selected = True
            map_menu = False
            character_selection=True 
    elif character_selection:
        selected_character_p1 = character_selection_screen()
        if selected_character_p1 == "exit":
            run = False
        else:
            if selected_character_p1 == "Warrior":
                fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            elif selected_character_p1 == "Wizard":
                fighter_1 = Fighter(1, 200, 310, False, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
            elif selected_character_p1 == "Hero":
                fighter_1 = Fighter(1, 200, 310, False, MARTIALHERO_DATA, martialhero_sheet, MARTIALHERO_ANIMATION_STEPS, sword_fx)
            elif selected_character_p1 == "Knight":
                fighter_1 = Fighter(1, 200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, knight_fx)


        selected_character_p2 = character_selection_screen()
        if selected_character_p2 == "exit":
            run = False
        else:
            if selected_character_p2 == "Warrior":
                fighter_2 = Fighter(2, 700, 310, True, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            elif selected_character_p2 == "Wizard":
                fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
            elif selected_character_p2 == "Hero":
                fighter_2 = Fighter(2, 700, 310, True   , MARTIALHERO_DATA, martialhero_sheet, MARTIALHERO_ANIMATION_STEPS, sword_fx)
            elif selected_character_p2 == "Knight":
                fighter_2 = Fighter(2, 700, 310, True, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, knight_fx)
                

        character_selection = False     
    elif not map_menu and not main_menu and not character_selection:
        # Lấy hình ảnh của map được chọn
        map_image = [bg_image, bg_image1, bg_image2, bg_image3, bg_image4, bg_image5][map_selected_index]
        draw_map_select(map_image) 
        #show player status
        draw_health_bar(fighter_1.health, 20, 20)
        draw_text("HP: " + str(fighter_1.health), score_font, WHITE, 180, 15)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("HP: " + str(fighter_2.health), score_font, WHITE, 740, 15)
        draw_mana_bar(fighter_1.mana, 20, 55)
        draw_mana_bar(fighter_2.mana, 580, 55)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)
        
        #update countdown
        if intro_count <= 0:
            #move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            #display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 50)
            #update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        #update fighters lam cho chuyen dong animation
        fighter_1.update()
        fighter_2.update()
        
        #draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)
        
        #check for player defeat
        WINNING_SCORE = 3
        game_over = False
        if round_over == False:
            if fighter_1.alive ==False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive ==False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        elif score[0] == WINNING_SCORE:
            screen.blit(P1Victory_img, (360, 150))
            round_over = True
            if restart_button.draw():
                fighter_1.reset(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                fighter_2.reset(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                score = [0, 0]
                round_over = False
        elif score[1] == WINNING_SCORE:
            screen.blit(P2Victory_img, (360, 150))     
            round_over = True
            if restart_button.draw():
                if selected_character_p1 == "Warrior":
                    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                elif selected_character_p1 == "Wizard":
                    fighter_1 = Fighter(1, 200, 310, False, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                elif selected_character_p1 == "Hero":
                    fighter_1 = Fighter(1, 200, 310, False, MARTIALHERO_DATA, martialhero_sheet, MARTIALHERO_ANIMATION_STEPS, sword_fx)
                elif selected_character_p1 == "Knight":
                    fighter_1 = Fighter(1, 200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, knight_fx)
                if selected_character_p2 == "Warrior":
                    fighter_2 = Fighter(2, 700, 310, True, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                elif selected_character_p2 == "Wizard":
                    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                elif selected_character_p2 == "Hero":
                    fighter_2 = Fighter(2, 700, 310, True   , MARTIALHERO_DATA, martialhero_sheet, MARTIALHERO_ANIMATION_STEPS, sword_fx)
                elif selected_character_p2 == "Knight":
                    fighter_2 = Fighter(2, 700, 310, True, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, knight_fx)  
                score = [0, 0]
                round_over = False
            if main_menu_button.draw():
                main_menu = True
                score = [0, 0]
                round_over = False
        else:
            #display victory image
            # screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time >ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                if selected_character_p1 == "Warrior":
                    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                elif selected_character_p1 == "Wizard":
                    fighter_1 = Fighter(1, 200, 310, False, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                elif selected_character_p1 == "Hero":
                    fighter_1 = Fighter(1, 200, 310, False, MARTIALHERO_DATA, martialhero_sheet, MARTIALHERO_ANIMATION_STEPS, sword_fx)
                elif selected_character_p1 == "Knight":
                    fighter_1 = Fighter(1, 200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, knight_fx)
                if selected_character_p2 == "Warrior":
                    fighter_2 = Fighter(2, 700, 310, True, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                elif selected_character_p2 == "Wizard":
                    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                elif selected_character_p2 == "Hero":
                    fighter_2 = Fighter(2, 700, 310, True   , MARTIALHERO_DATA, martialhero_sheet, MARTIALHERO_ANIMATION_STEPS, sword_fx)
                elif selected_character_p2 == "Knight":
                    fighter_2 = Fighter(2, 700, 310, True, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, knight_fx)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if map_menu:
                # Lấy vị trí của chuột khi click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Kiểm tra xem chuột có nằm trong vùng của map không
                for i, map_image in enumerate([bg_image, bg_image1, bg_image2, bg_image3, bg_image4, bg_image5]):
                    map_area = pygame.Rect(150 + (i % 3) * 250, 100 + (i // 3) * 180, 200, 120)  # Cập nhật vùng cho 6 map
                    if map_area.collidepoint(mouse_x, mouse_y):
                        # Lưu chỉ số của map được chọn
                        map_selected_index = i
                        break
    #update display
    pygame.display.update()
                
#exit pygame
pygame.quit()