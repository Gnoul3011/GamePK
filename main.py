import pygame
from pygame import mixer
from fighter import Fighter

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

# Hàm vẽ chữ
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for drawing background
def draw_bg(scaler_bg):
    screen.blit(scaler_bg,(0, 0))
    
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
start_button = Button(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 3, start_img)
exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, exit_img)
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
            main_menu = False
        if exit_button.draw():
            run = False

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
                
    #update display
    pygame.display.update()
                
#exit pygame
pygame.quit()