"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
import os
import fnmatch
from typing import Optional


import tcod
from tcod import libtcodpy

import color
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers
import time




# Load the background image and remove the alpha channel.

background_image = tcod.image.load("resources/images/mario.png")[:, :, :3]
kb = tcod.event.KeySym
kb_mod = tcod.event.Modifier

#def new_game(charName: str="Mario", charRace:str = "Mario", charClass: str = "Mario") -> Engine:
def new_game(**kwargs) -> Engine:
    """Return a brand new game session as an Engine instance."""

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)

    player.name = kwargs['charName']
    player.charRace = kwargs['charRace']
    player.charClass = kwargs['charClass']

    if kwargs['charRace'] == "yoshi":
        player.char = entity_factories.yoshi_chr


    player.speed = 200
    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )
    

    
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)
    player.dv = 20

    
    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine



class LoadSavedGameMenu(input_handlers.BaseEventHandler):

    def __init__(self,parent_handler: MainMenu) -> None:
        self.dir_path = os.getcwd()+"/saves/"
        self.saves = fnmatch.filter(os.listdir(self.dir_path),"*.sav")
        self.parent = parent_handler
    
    def on_render(self, console: tcod.console.Console) -> None:
       
        
        #print(self.saves, len(self.saves))

        y = 5
        x = 5
        height = 50
        width = 80


        console.draw_frame(
            x=x,
            y=y,
            width=width-10,
            height=height-10,
            #title=self.TITLE,
            clear=True,
            fg=color.orange,
            bg=(0, 0, 0),
            decoration="╔═╗║ ║╚═╝",
        )

        txt = "║ Choose Save File ║"

        centerTitle = int(width/2 - len(txt)/2)        
        console.print(centerTitle , y , txt)

        if len(self.saves) > 0:
            for i, save in enumerate(self.saves):
                item_key = chr(ord("a") + i)
                
                item_string = f"({item_key}) {save}"

                console.print(x + 1, y + i + 1, item_string)
        else:
            console.print(x + 1, y + 1, "(Empty)")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.ActionOrHandler]:
        #player = self.engine.player
        key = event.sym
        index = key - kb.a

        if event.sym in (kb.q, kb.ESCAPE):
            return self.parent

        if 0 <= index <= 26:
            try:
                selected_item = self.saves[index] 
            except IndexError:
                self.engine.message_log.add_message("Invalid entry.", color.invalid)
                return None
            return input_handlers.MainGameEventHandler(load_game(self.dir_path+selected_item))
        #return super().ev_keydown(event)



class CharGen1(input_handlers.BaseEventHandler):

    def __init__(self,parent_handler: MainMenu) -> None:
    #     #self.dir_path = os.getcwd()+"/saves/"
    #     #self.saves = fnmatch.filter(os.listdir(self.dir_path),"*.sav")
        self.parent = parent_handler
    
    def on_render(self, console: tcod.console.Console) -> None:
       
        #print("on render")
        #print(self.saves, len(self.saves))

        y = 5
        x = 5
        height = 50
        width = 80



        console.draw_frame(
            x=x,
            y=y,
            width=width-10,
            height=height-10,
            #title=self.TITLE,
            clear=True,
            fg=color.orange,
            bg=(0, 0, 0),
            decoration="╔═╗║ ║╚═╝",
        )

        txt = "║ Choose a Character Race ║"

        self.races = ["mario","yoshi","bowser","koopa"]

        centerTitle = int(width/2 - len(txt)/2)        
        console.print(centerTitle , y , txt)

        if len(self.races) > 0:
            for i, opts in enumerate(self.races):
                item_key = chr(ord("a") + i)
                
                item_string = f"({item_key}) {opts}"

                console.print(x + 1, y + i + 1, item_string)
        else:
            console.print(x + 1, y + 1, "(Empty)")

    def ev_keydown(self, event: tcod.event.KeyDown):# -> Optional[input_handlers.ActionOrHandler]:
        #player = self.engine.player
        key = event.sym
        index = key - kb.a

        if event.sym in (kb.q, kb.ESCAPE):
            return self.parent

        if 0 <= index <= 26:
            try:
                                
                selected_item = self.races[index]
                #race_chr = getattr(entity_factories,selected_item+"_chr")
                #print("gen1:",selected_item)
                

            except IndexError:
                self.engine.message_log.add_message("Invalid entry.", color.invalid)
                return None

            return CharGen2(self,charRace=selected_item)
            
        #return super().ev_keydown(event)


class CharGen2(input_handlers.BaseEventHandler):

    def __init__(self,parent_handler: MainMenu,**kwargs) -> None:
    #     #self.dir_path = os.getcwd()+"/saves/"
    #     #self.saves = fnmatch.filter(os.listdir(self.dir_path),"*.sav")
        self.parent = parent_handler
        self.newGameVars = kwargs
        print(type(self.newGameVars))
    
    def on_render(self, console: tcod.Console) -> None:
 
        y = 5
        x = 5
        height = 50
        width = 80

        console.draw_frame(
            x=x,
            y=y,
            width=width-10,
            height=height-10,
            #title=self.TITLE,
            clear=True,
            fg=color.orange,
            bg=(0, 0, 0),
            decoration="╔═╗║ ║╚═╝",
        )

        txt = "║ Choose Class for your Character ║"

        self.charClasses = ["mario","yoshi","bowser","koopa"]

        centerTitle = int(width/2 - len(txt)/2)        
        console.print(centerTitle , y , txt)

        if len(self.charClasses) > 0:
            for i, opts in enumerate(self.charClasses):
                item_key = chr(ord("a") + i)
                
                item_string = f"({item_key}) {opts}"

                console.print(x + 1, y + i + 1, item_string)
        else:
            console.print(x + 1, y + 1, "(Empty)")


    def ev_keydown(self, event: tcod.event.KeyDown):# -> Optional[input_handlers.ActionOrHandler]:
        
        key = event.sym
        index = key - kb.a

        if event.sym in (kb.q, kb.ESCAPE):
            return self.parent

        if 0 <= index <= 26:
            try:
                                
                selected_item = self.charClasses[index]

                self.newGameVars["charClass"] = selected_item
                print(self.newGameVars)

                #race_chr = getattr(entity_factories,selected_item+"_chr")
                #print("gen1:",selected_item)

            except IndexError:
                self.engine.message_log.add_message("Invalid entry.", color.invalid)
                return None

            
            return CharGen3(self, **self.newGameVars)
            


class CharGen3(input_handlers.BaseEventHandler):
    
    
    def __init__(self,parent_handler: MainMenu,**kwargs) -> None:
        self.parent = parent_handler
        self.newGameVars = kwargs
        print(self.newGameVars)
        self.buffer = kwargs['charRace']


    def on_render(self, console: tcod.Console) -> None:
       
        #print("on render")
        #print(self.saves, len(self.saves))

        y = 5
        x = 5
        height = 50
        width = 80

        

        console.draw_frame(
            x=x,
            y=y,
            width=width-10,
            height=height-10,
            #title=self.TITLE,
            clear=True,
            fg=color.orange,
            bg=(0, 0, 0),
            decoration="╔═╗║ ║╚═╝",
        )

        txt = "║ Enter your name ║"


        centerTitle = int(width/2 - len(txt)/2)        
        console.print(centerTitle , y , txt)

        
        console.print(x + 3, y + 5, self.buffer)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.ActionOrHandler]:
    #def ev_keydown(self, event: tcod.event) -> Optional[input_handlers.ActionOrHandler]:
        #player = self.engine.player
        key = event.sym
        modifier = event.mod

        if key == (kb.BACKSPACE):
            self.buffer = self.buffer[:-1]

        if key == (kb.ESCAPE):
            return self.parent
        
        if key == (kb.RETURN):
            
            
            self.newGameVars['charName'] = self.buffer
            return input_handlers.MainGameEventHandler(new_game(**self.newGameVars))
        
        index = key - kb.a

        if modifier & kb_mod.SHIFT: # if a shift is held
            
            if 0 <= index <= 26: 
                #print (chr(key))
                self.buffer += str.capitalize(chr(key))
                return

        if 0 <= index <= 26: 
            #print (chr(key))
            self.buffer += chr(key)


    # Handled in KeyDown to avoid issue where selection from previous menu enters a letter
    # def ev_textinput(self, event: tcod.event.TextInput) -> Optional[input_handlers.ActionOrHandler]:   
    #     text = event.text
        
    #     #self.buffer += text


class TextInput(input_handlers.BaseEventHandler):

    #buffer = "Mario"

    def __init__(self) -> None:
        self.buffer = "tests"

    def on_render(self, console: tcod.console.Console) -> None:
        
        console.print(5,5,self.buffer)
        

    def dispatch(self, event, *args, **kwargs):
        #saved_args = locals()
        #print(saved_args)


        #for event in tcod.event.get():
            
        match event:
            case tcod.event.Quit():
                raise SystemExit()
            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                return self.parent
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RETURN):
                return input_handlers.MainGameEventHandler(new_game())
            case tcod.event.KeyDown(sym=tcod.event.KeySym.BACKSPACE):
                print("back")
                self.buffer = self.buffer[:-1]  # Remove last symbol
                return
            case tcod.event.TextInput(text=text):
                self.buffer += text  # Append text input
                return
                
    




class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""



    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)
        #console.draw_semigraphics(test_image, 0, 0)

        
        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "Super Plumber Man: Quest of Unknown",
            fg=color.menu_title,
            bg=color.black,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Steve Reed",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game","[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (kb.q, kb.ESCAPE):
            raise SystemExit()
        elif event.sym == kb.c:
            try:
                return LoadSavedGameMenu(self)
                                
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == kb.n:
            print("new game")
            
            #return input_handlers.MainGameEventHandler(new_game())
            

            return CharGen1(self)
            #return CharGen2(self)
            
            #print(name,race)

            #input_handlers.MainGameEventHandler(new_game())
        return None



