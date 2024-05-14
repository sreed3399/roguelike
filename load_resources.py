
from PIL import Image
import numpy as np
from pygame import mixer

import color
import tcod

imagePath = "resources/images/"
mapPath = "resources/maps/"
soundPath = "resources/sounds/"
tilePath = "resources/tiles/"

def loadTiles():
    
    tileset = tcod.tileset.load_tilesheet(
        tilePath+"tiles-2x.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    tileset = tcod.tileset.load_truetype_font(tilePath+"courier-bold.ttf",16,16)
    
    image = Image.open(tilePath+"koopa.png")
    tileset.set_tile(100000,np.array(image))

    image = Image.open(tilePath+"goomba.png")
    tileset.set_tile(100001,np.array(image))

    image = Image.open(tilePath+"mario.png")
    tileset.set_tile(100002,np.array(image))

    image = Image.open(tilePath+"yoshi.png")
    tileset.set_tile(100003,np.array(image))
    
    image = Image.open(tilePath+"dung_wall.png")
    tileset.set_tile(100010,np.array(image))
    
    image = Image.open(tilePath+"down_pipe.png")
    tileset.set_tile(100011,np.array(image))

    image = Image.open(tilePath+"up_pipe.png")
    tileset.set_tile(100012,np.array(image))

    image = Image.open(tilePath+"dung_floor.png")
    #tileset.set_tile(ord("."),np.array(image))

    return tileset




def loadMusic():
    mixer.init()
    mixer.music.load(soundPath+"Mushroom Kingdom Mayhem.mp3")
    mixer.music.play(-1)


class sounds():

    mixer.init()
    hit = mixer.Sound(soundPath+"sword-hit.wav")
    hit.set_volume(0.25)
        
    miss = mixer.Sound(soundPath+"sword-miss.wav")
    miss.set_volume(0.25)     

    #def loadActionSounds():
        #mixer.init()
        

    def playSound(snd):
        getattr(sounds,snd).play()
    