from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov
import os

import exceptions

from message_log import MessageLog
import render_functions


if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld
    


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            
            if entity.ai:
                try:
                    if entity.energy >=0:
                        entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=self.player.visionRange,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible


    def render(self, console: Console) -> None:
        print("Map Height: ", self.game_map.height)
        print("Map Width: " , self.game_map.width)
        print("visible Shape: " , self.game_map.visible.shape)


        self.game_map.render(console)
        



        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0,47),
        )

        render_functions.render_level_xp_bar(
            console=console,
            player_level=self.player.level.current_level,
            cur_xp=self.player.level.current_xp,
            needed_xp=self.player.level.experience_to_next_level,
            location=(0,48),
        )

        render_functions.render_names_at_mouse_location(console=console, x=21, y=44, engine=self)

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file. Saves current game state
        Called by save function in main """
        path = os.getcwd()+"/saves/"
        
        savefile = path + filename + ".sav"

        if not os.path.exists(path):
            os.mkdir(path)

        save_data = lzma.compress(pickle.dumps(self))
        with open(savefile, "wb") as f:
            f.write(save_data)


