import io
import numpy as np
import pickle
import lzma

import game_map

#index,character,tile,


def save_map(self, filename: str) -> None:
    """Save this Engine instance as a compressed file."""
    save_data = lzma.compress(pickle.dumps(self))
    with open(filename, "wb") as f:
        f.write(save_data)

def load_map(filename: str) -> game_map
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        map = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(map, game_map)
    return map