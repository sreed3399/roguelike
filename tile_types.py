from typing import Tuple

import numpy as np  # type: ignore
from color import *

wall_chr = chr(100010)
down_chr = chr(100011)

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    #return np.array((walkable, transparent, dark), dtype=tile_dt)
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), white, black), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("."), stone_fg_dark, stone_bg_dark),
    light=(ord("."), stone_fg_light, stone_bg_light),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(wall_chr), stone_fg_dark, black),
    light=(ord(wall_chr), stone_fg_light, black),
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(down_chr), (200, 200, 200), (black)),
    light=(ord(down_chr), (255, 255, 255), (black)),
)