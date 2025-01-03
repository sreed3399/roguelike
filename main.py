#!/usr/bin/env python3
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


# Standard Python Libraries
import traceback
#import time
#import imageio
from PIL import Image
import numpy as np
from pygame import mixer

# tcod - roguelike library
import tcod
import tcod.sdl.mouse
import tcod.sdl.render
from tcod import libtcodpy

# Program Modules
import color
import exceptions
import input_handlers
import setup_game
from load_resources import loadTiles, loadMusic

CONSOLE_SCREEN_WIDTH = 80
CONSOLE_SCREEN_HEIGHT = 50

SAMPLE_SCREEN_WIDTH = 20
SAMPLE_SCREEN_HEIGHT = 20
SAMPLE_SCREEN_X = 0
SAMPLE_SCREEN_Y = 0


# Mutable global names.
context: tcod.context.Context
tileset: tcod.tileset.Tileset
console_render: tcod.render.SDLConsoleRender  # Optional SDL renderer.
sample_minimap: tcod.sdl.render.Texture  # Optional minimap texture.
root_console = tcod.console.Console(CONSOLE_SCREEN_WIDTH, CONSOLE_SCREEN_HEIGHT, order="F")

sample_console = tcod.console.Console(SAMPLE_SCREEN_WIDTH, SAMPLE_SCREEN_HEIGHT, order="F")


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None: 
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


def main() -> None:
    screen_width = 80
    screen_height = 50

    loadMusic()
    tileset = loadTiles()
  
    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()
    

    ### Main Game Loop
    # with tcod.context.new_terminal(
        # screen_width,
        # screen_height,
        # tileset=tileset,
        # title="Super Plumber Man",
        # vsync=True,
        # renderer=tcod.context.RENDERER_SDL2,
    with tcod.context.new(
        console=root_console, 
        tileset=tileset,
        title="Super Plumber Man",
        
    ) as context:
        #root_console = tcod.console.Console(screen_width, screen_height, order="F")
        try:
            turn = 0
            while True:
                root_console.clear()
                
                handler.on_render(console=root_console)
                context.present(root_console,keep_aspect=True, integer_scaling=True)

                tcod.tileset.procedural_block_elements(tileset=tileset)

                try:
                    
                    if isinstance(handler, input_handlers.MainGameEventHandler):
                        if handler.engine.player.energy >= 0:
                            handler.engine.player.energy = 0
                        else:
                            for entity in set(handler.engine.game_map.actors):
                                entity.energy += entity.speed
                                if entity.energy >= 0:
                                    entity.energy = 0
                                
                                
                    #for event in tcod.event.wait(): # Wait pauses for input. # Get lets the loop process so things can still happen during turns
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
            save_game(handler, handler.engine.player.name)
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, handler.engine.player.name)
            raise
        
 
if __name__ == "__main__":
    main()