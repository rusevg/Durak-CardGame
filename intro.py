import os
from time import sleep
import pygame

os.system('cls||clear')

file = r'logo.mp3'
pygame.mixer.init()
track = pygame.mixer.music.load(file)
pygame.mixer.music.play()

os.system("mode con cols=100 lines=15")


def intro():
    a1 = '\t                    \t\t\t\t\t\t                      '
    a2 = '\t▀▄█▀█▀█▄▀  ███████  \t\t\t\t\t\t  ▀▄█▀█▀█▄▀  ███████  '
    a3 = '\t ▀▀███▀▀   ██▄█▄██  \t\t\t\t\t\t   ▀▀███▀▀   ██▄█▄██  '
    a4 = '\t█▀█████▀█ █▀█████▀█ \t\t\t\t\t\t  █▀█████▀█ █▀█████▀█ '
    a5 = '\t█ █████ █ █ ▄███▄ █ \t\t\t\t\t\t  █ █████ █ █ ▄███▄ █ '
    a6 = '\t▀ ▀█▀█▀ ▀ ▀ ▀█▀█▀   \t\t\t\t\t\t  ▀ ▀█▀█▀ ▀ ▀ ▀█▀█▀   '
    a7 = '\t                    \t\t\t\t\t\t                      '

    for i in [a1, a2, a3, a4, a5, a6, a7]:
        print(i)
    print('\n\n\t\t\t\t     WELCOME TO DURKO GAME STUDIOS')
    print('\t\t\t\t\t ©2022 RusittoO inc.')
    an = ('|', '/', '-', '\\')
    ian = 0
    counter = 0
    while counter < 70:
        print('\t\t\t\t\t     LOADING...', an[ian], sep='', end='\r')
        sleep(0.1)
        ian += 1
        if ian is len(an):
            ian = 0
        counter += 1
