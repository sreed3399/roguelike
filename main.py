#!/usr/bin/env python3
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


# Standard Python Libraries
import traceback
import time
import imageio
from PIL import Image
import numpy as np
from pygame import mixer

# tcod - roguelike library
import tcod
import load_resources

# Program Modules
import color
import exceptions
import input_handlers
import setup_game

def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


def main() -> None:
    screen_width = 80
    screen_height = 50

    # var = mixer.init()
    # mixer.music.load("resources/sounds/Mushroom Kingdom Mayhem.mp3")
    # mixer.music.play(-1)

    load_resources.loadMusic()
    tileset = load_resources.loadTiles()


    # tileset = tcod.tileset.load_tilesheet(
    #     #"dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    #     "tiles/tiles-2x.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    # )

    # tileset = tcod.tileset.load_truetype_font("tiles/courier-bold.ttf",16,16)
    
    # image = Image.open("tiles/koopa.png")
    # tileset.set_tile(100000,np.array(image))

    # image = Image.open("tiles/goomba.png")
    # tileset.set_tile(100001,np.array(image))

    # image = Image.open("tiles/mario.png")
    # tileset.set_tile(100002,np.array(image))

    # image = Image.open("tiles/yoshi.png")
    # tileset.set_tile(100003,np.array(image))
    
    # image = Image.open("tiles/dung_wall.png")
    # tileset.set_tile(100010,np.array(image))
    
    # image = Image.open("tiles/down_pipe.png")
    # tileset.set_tile(100011,np.array(image))

    # image = Image.open("tiles/up_pipe.png")
    # tileset.set_tile(100012,np.array(image))

    # image = Image.open("tiles/dung_floor.png")
    # #tileset.set_tile(ord("."),np.array(image))

 
    

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()
    
    

    ### Main Game Loop
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Super Plumber Man",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        try:
            turn = 0
            while True:
                root_console.clear()
                                                
                handler.on_render(console=root_console)
                context.present(root_console)
                
                                
                try:
                    #for event in tcod.event.wait():
                    if isinstance(handler, input_handlers.MainGameEventHandler):
                        if handler.engine.player.energy >= 0:
                            handler.engine.player.energy = 0
                        else:
                            for entity in set(handler.engine.game_map.actors):
                                entity.energy += entity.speed
                                if entity.energy >= 0:
                                    entity.energy = 0
                                
                                #print(entity.name,entity.energy,entity.speed)
                    for event in tcod.event.get():
                        #print(event)        
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                        #print(handler)
 

                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise
          


if __name__ == "__main__":
    main()