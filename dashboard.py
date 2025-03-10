import sys
import pygame
from button import Button
import subprocess

pygame.init()

SCREENWIDTH = 800
SCREENHEIGHT = 640

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 50)

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("TLS GAME")

BG = pygame.image.load(r"C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Picture\Mainpage Hangman.png")
BG = pygame.transform.scale(BG, (SCREENWIDTH, SCREENHEIGHT))  # Resize to fit screen if needed

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(r"C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Picture\font.ttf", size)

def play():


    while True:
        pygame.mixer.music.fadeout(400)
        subprocess.run(["python", r"C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Client-Hangman-TLS-Hazami.py"])
        print('Congratulations!, You completed all the questions!')
        main_menu()
     
def about():
    while True:
        
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        BG = pygame.image.load(r"C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Picture\About Hangman Rule.png")
        BG = pygame.transform.scale(BG, (SCREENWIDTH, SCREENHEIGHT))  # Resize to fit screen if needed  
        SCREEN.blit(BG, (0, 0))

        OPTIONS_BACK = Button(image=None, pos=(SCREENWIDTH // 2, 600), 
                            text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer.Sound(r'C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Music\Mouse Click Sound Effect.wav').play()
                    main_menu()

        pygame.display.update()

def main_menu():
    # Load the background music (place this outside of the game loop)
    pygame.mixer.music.load(r'C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Music\KM\Pixel Music Intro.mp3')
    pygame.mixer.music.play(-1, 0)  # Play the music in a loop

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("HANGMAN", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 6))

        PLAY_BUTTON = Button(image=pygame.image.load(r"C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Picture\Play Rect.png"), pos=(SCREENWIDTH // 2, 250), 
                            text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        ABOUT_BUTTON = Button(image=pygame.image.load(r"C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Picture\Play Rect.png"), pos=(SCREENWIDTH // 2, 390), 
                            text_input="ABOUT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(r"C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Picture\Quit Rect.png"), pos=(SCREENWIDTH // 2, 540), 
                            text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, ABOUT_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(r'C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Music\Mouse Click Sound Effect.wav').play()
                    play()
                if ABOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(r'C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Music\Mouse Click Sound Effect.wav').play()
                    about()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.Sound(r'C:\Users\zamic\Documents\UPM\TLS_GAME\TLS_GAME\Music\Mouse Click Sound Effect.wav').play()
                    pygame.time.delay(500)
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()