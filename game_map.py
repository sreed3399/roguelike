from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

from entity import Actor, Item
import tile_types
import pickle, lzma
import os

import tcod
from tcod import libtcodpy

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        
        self.engine = engine
        self.width, self.height = width, height
        
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        
        
        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player can currently see

        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player has seen before

        self.downstairs_location = (0,0)
        self.upstairs_location = (0,0)
        self.floorName = "floor"
    
    @property
    def gamemap(self) -> GameMap:
        return self

    

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_blocking_entity_at_location(
        self, location_x: int, location_y: int,
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height


    def convertCoords(self, x1, y1 , ent_x, ent_y ):
        

        x = ent_x - x1
        y = ent_y - y1

        #print(entity.name,x,y)
        return x,y
        
        
        pass
    
    def screenCenter_Coords(self,screenw, screenh, px,py):
        
        map_width = self.width
        map_height = self.height
        
                
        print("Map Shape:", map_width, map_height)
        print("Screen Shape:",screenw,screenh)
        print("Player Abs:", px, py)


        screenw_delta = screenw // 2 #39 + center + 39 = 79
        screenh_delta = screenh // 2 #21 + center + 21 = 43

        #Assume player is center screen
        cx = px
        cy = py

        # Adjust if player is too close to edge
        if px - screenw_delta < 0: 
            cx = screenw_delta
        if px + screenw_delta > map_width:
            cx = map_width - screenw_delta
        if py - screenh_delta < 0:
            cy = screenh_delta
        if py + screenh_delta > map_height:
            cy = map_height - screenh_delta
            
        return cx,cy
        
        pass



    def render(self, console: Console) -> None:
        
        #Screen Size
        #screen_width = console.width-1
        #screen_height = console.height-7

        print("H: ", self.engine.game_map.height, "W: ",self.engine.game_map.width)


        screen_width = self.engine.game_map.width
        screen_height = self.engine.game_map.height
       
        print("width:", screen_width," height:",screen_height)

        #print(screen_width,screen_height)
        #print("player loc:",player_x, player_y)

        screen_width_delta = screen_width // 2
        screen_height_delta = screen_height // 2

        #print(screen_width_delta,screen_height_delta)
        print("")
        print("===============")
        
        #screen_center = (39,21)
        
        player = self.engine.player
        player_x,player_y = self.engine.player.location

                                                     #79 ,             43,         
        center_x, center_y = self.screenCenter_Coords(screen_width, screen_height, player_x, player_y)

        #print("Center:",self.screenCenter_Coords(screen_width, screen_height, player_x,player_y))
        #print("x1:",self.screenCenter_Coords(screen_width, screen_height, 2, player_y))
        #print("x2:",self.screenCenter_Coords(screen_width, screen_height, screen_width-10, player_y))
        #print("y1:",self.screenCenter_Coords(screen_width, screen_height, player_x, 11))
        #print("y2:",self.screenCenter_Coords(screen_width, screen_height, player_x, screen_height-10))

        # Display Boundries
        screen_x_min = center_x - screen_width_delta # Zero - first index
        screen_x_max = center_x + screen_width_delta # 78  but 79 indices
        screen_y_min = center_y - screen_height_delta # Zero 
        screen_y_max = center_y + screen_height_delta # 42 but 43 indices

        print("screen corners - x1:",screen_x_min,", x2:",screen_x_max, ", y1:",screen_y_min,", y2:",screen_y_max)
        print("screen center:", center_x,center_y)


        print("validation min:",screen_x_min+screen_width_delta, screen_y_min+screen_height_delta)
        print("validation max:",screen_x_max-screen_width_delta, screen_y_max-screen_height_delta)
        print(screen_x_min+screen_width, screen_x_max)
        print("")
        print("player abs:", player_x,player_y)
        print("player screen:", self.convertCoords(screen_x_min, screen_y_min, player.x,player.y ))

        #screen_x_min = 0
        #screen_x_max = 78
        #screen_y_min = 0
        #screen_y_max = 42



        screen_vis = np.full(
            (screen_width, screen_height), fill_value=False, order="F"
        )  # Tiles the player has seen before

        screen_explore = np.full(
            (screen_width, screen_height), fill_value=False, order="F"
        )  # 

        #print("fullvis:",self.visible.shape)
        #print("fullexp:",self.explored.shape)
        #print("fullTiles:",self.tiles.shape)

        #print("vis:",screen_vis.shape)        
        #print("exp:",screen_explore.shape)
        



        # Only objects on screen.
        screen_vis = self.visible[screen_x_min:screen_x_max+1, screen_y_min : screen_y_max+1]
        screen_explore = self.explored[screen_x_min:screen_x_max+1, screen_y_min : screen_y_max+1]
        screen_tiles = self.tiles[screen_x_min:screen_x_max+1, screen_y_min : screen_y_max+1]
        
        print("vis:",screen_vis.shape)
        print("exp:",screen_explore.shape)
        print("tiles:",screen_tiles.shape)
                
        
        print("console",console.rgb[:screen_width,:screen_height].shape)

        console.rgb[0 : screen_width, 0 : screen_height] = np.select(
            condlist=[screen_vis, screen_explore],
            choicelist=[screen_tiles["light"], screen_tiles["dark"]],
            default=tile_types.SHROUD,
        )

        
        
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        # console.rgb[0 : self.width, 0 : self.height] = np.select(
        #     condlist=[self.visible, self.explored],
        #     choicelist=[self.tiles["light"], self.tiles["dark"]],
        #     default=tile_types.SHROUD,
        # )

        #self.engine.player.location()

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
                
                #print(entity.name,entity.x,entity.y, self.convertCoords(screen_x_min,screen_y_min, entity))
                #loc_x, loc_y = self.convertCoords(screen_x_min,screen_y_min, entity)
                #if screen_vis[loc_x,loc_y]:
                if self.visible[entity.x, entity.y]:

                    #if entity == self.engine.player:
                        #print(entity.name,entity.location)
                        #print(self.convertCoords(screen_x_min,screen_y_min, entity))
                    #console.print(loc_x, loc_y,string=entity.char, fg=entity.color,bg_blend=libtcodpy.BKGND_ALPHA(0))
                #loc_x, loc_y = self.convertCoords(screen_x_min, screen_y_min, entity)
                #print(entity.name,loc_x,loc_y)
                    loc_x, loc_y = self.convertCoords(screen_x_min, screen_y_min, entity.x,entity.y)
                    print("abs:",entity.name,entity.x,entity.y)
                    #if screen_vis[loc_x,loc_y]:
                            #loc_x, loc_y = self.convertCoords(screen_x_min, screen_y_min, entity)
                    print("screen",entity.name,loc_x,loc_y)
                    console.print(
                    x=loc_x, y=loc_y, string=entity.char, fg=entity.color,bg_blend=libtcodpy.BKGND_ALPHA(0)
                        #x=entity.x, y=entity.y, string=entity.char, fg=entity.color,bg_blend=libtcodpy.BKGND_ALPHA(0)
                        )
                        
            

    def save_map(self, filename: str = "player") -> None:
        """ Save this Engine instance as a compressed file. Saves current game state 
        Called by save function in main 
        """
        
        path = os.getcwd()+"/saves/" + self.engine.player.name + "/"
        savefile = (path + "/" +  str(self.engine.game_world.current_floor) + ".map")

        if not os.path.exists(path):
            os.mkdir(path)

        save_data = lzma.compress(pickle.dumps(self.engine.game_map))
        with open(savefile, "wb") as f:
            f.write(save_data)
        print("saved")

        
    # def save_map(self, path: str = "player") -> None: # added by Steve
    #     """Save this map instance as a compressed file.
    #     currently being used to load/unload maps that have been previously visited
    #     """
    #     path = "saves/" + self.engine.player.name
    #     if not os.path.exists(path):
    #         os.mkdir(path)
        
    #     save_data = self.tiles
    #     save_data.tofile(path + "/" +  str(self.engine.game_world.current_floor) + ".map")

    
    def load_map(self,filename: str) -> GameMap:
        """Load an Engine instance from a file."""
        with open(filename, "rb") as f:
            map = pickle.loads(lzma.decompress(f.read()))
        assert isinstance(map, GameMap)

        # for entity in map.entities:
        #     print(entity)
        
        return map  




class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """

    def __init__(
        self,
        *,
        engine: Engine,
        map_width: int,
        map_height: int,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,

        current_floor: int = 0
    ):
        self.engine = engine

        self.map_width = map_width
        self.map_height = map_height

        self.max_rooms = max_rooms

        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

        self.current_floor = current_floor


    def generate_floor(self) -> None:
        from procgen import generate_dungeon

        self.current_floor += 1

        self.engine.game_map = generate_dungeon(
            max_rooms=self.max_rooms,
            room_min_size=self.room_min_size,
            room_max_size=self.room_max_size,
            map_width=self.map_width,
            map_height=self.map_height,
            engine=self.engine,
        )

    def move_floor(self, tofloor: str = 2) -> None:
        
        self.engine.game_map.save_map()
        
        #print("Level:",self.engine.game_world.current_floor)
        for entity in self.engine.game_map.entities:
            print(entity.id,entity.location)
        # If file exists, load
        path = "saves/" + self.engine.player.name + "/2.map"
        if os.path.exists(path):
            print("exists")
            self.engine.game_map = self.engine.game_map.load_map(path)
            
            
            #print(self.engine.game_world.current_floor)
            for entity in self.engine.game_map.entities:
                #print(entity.id ,entity.location)
                pass

        else:
            self.generate_floor()
         
        return
    

