
#importing modules required for the game 
import pygame
from pygame.locals import *
import random

# Initializing Pygame module
pygame.init()

#game window dimensions

#width and height of the game window
WID, HHT = 500, 360
#displaying main window
Game_window = pygame.display.set_mode((WID, HHT))
#game window name
pygame.display.set_caption("CATCH THE PINKY")
#setting background image to give a pleasant look
bg=pygame.image.load("i.png")
Game_window.blit(bg,(0,0))

# flowers(pinky and blacky) moving speed and falling time interval
flower_falling_speed = 3
flower_falling_time_interval = 1000  # in milliseconds

# Game variables
lives = 0
game_finished = False

# Set up the clock to manage time
clock = pygame.time.Clock()
#Display font settings
font = pygame.font.SysFont(None, 48)

pygame.mixer.music.load("music.mp3.mp3")
pygame.mixer.music.set_volume(1.5)
pygame.mixer.music.play(-1)
#images loading to display in the game
basket = pygame.image.load('bas.png')
pinky= pygame.image.load('singlepinky.png')
blacky = pygame.image.load('black.png')

#scaling the images for fitting in the gamewindow
basket = pygame.transform.scale(basket, (80, 50))
pinky = pygame.transform.scale(pinky, (20, 20))
blacky = pygame.transform.scale(blacky, (20, 20))


# basket position and its moving speed
basket_pos = [WID // 2 - basket.get_width() // 2, HHT - basket.get_height() - 10]
basket_moving_speed = 5


# to add flower continously untill the game stops 
MORE_FLOWER = pygame.USEREVENT + 1
pygame.time.set_timer(MORE_FLOWER, flower_falling_time_interval)

# Flowers list
bouquet = []


# Main Game event loop
falling = True
while falling:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            falling = False
        #creating a dictionary to make flowers falls randomly with any of the two colors
        elif event.type == MORE_FLOWER:
            flower = {
                "x": random.randint(0, WID - pinky.get_width()),
                "y": -pinky.get_height(),
                "color": "pink" if random.random() < 0.8 else "black"
            }
            bouquet.append(flower)
    #deciding the input keys for moving the basket 
    #a-left
    #l-right

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and basket_pos[0] > 0:
        basket_pos[0] -= basket_moving_speed
    if keys[pygame.K_l] and basket_pos[0] < WID - basket.get_width():
        basket_pos[0] += basket_moving_speed
    Game_window.blit(bg,(0,0))

    
    #deciding whether to end the game or to continue
    if not game_finished:
        #creating basket object 
        basket_rect = pygame.Rect(basket_pos[0], basket_pos[1], basket.get_width(), basket.get_height())
        Game_window.blit(basket, basket_pos)
        #making the flowers to appear on the window by random 
        for flower in bouquet[:]:
            flower["y"] += flower_falling_speed
            flow_img = pinky if flower["color"] == "pink" else blacky
            flower_rect = pygame.Rect(flower["x"], flower["y"], flow_img.get_width(),flow_img.get_height())
            Game_window.blit(flow_img, (flower["x"], flower["y"]))
            
            #to check whether the flower hits the basket

            if basket_rect.colliderect(flower_rect):
                if flower["color"] == "pink":
                    lives += 1
                else:
                    game_finished = True
                bouquet.remove(flower)
            elif flower["y"] > HHT:
                bouquet.remove(flower)

        lives_text = font.render(f'lives: {lives}', True, (255, 0, 0))
        Game_window.blit(lives_text, (5, 10))
    #to print the final window of the game with its final score
    else:
        game_over_text = font.render('Better luck next time', True, (255, 0, 0))
        Bouquet_text_ = font.render(f'Bouquet has:{lives} flowers', True, (0, 0,255))
        Game_window.blit(game_over_text, (WID // 2 - 150, HHT // 2 - 50))
        Game_window.blit(Bouquet_text_, (WID // 2 - 150, HHT // 2 + 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()



