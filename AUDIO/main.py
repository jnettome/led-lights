# wget https://www.myinstants.com/media/sounds/rickrolled_2.mp3

import pygame

def play_mp3(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for the music to finish playing.
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    play_mp3("./rickrolled_2.mp3")