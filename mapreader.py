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

def load_map(filename: str) -> game_map:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        map = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(map, game_map)
    return map



def save_map(self, filename: str) -> None:
    """Save this map instance as a compressed file."""
    #save_data = lzma.compress(pickle.dumps(self))
    save_data = self.tiles#.copy(order='C')
    #print(save_data.flags)
    #print(save_data.shape)
    #print(self.engine.player.x, self.engine.player.y, ":\n",save_data[1])
    #print(self.engine.player.x+1, self.engine.player.y, ":\n",save_data[self.engine.player.x+1,self.engine.player.y])

    #save_data.shape[0]

    # for a in save_data:
    #     #print(a)
    #     for b in a:
    #         print(b[2][0])
    #         pass
    #         #for c in b[2]:
    #         #    print(c)
    #         #    pass

    
    for x in range(0,save_data.shape[0]):
        txt = ""
        for i in range(0,save_data.shape[1]):
            txt += chr(save_data[x,i][2][0])

        print (txt)
    
    #np.savetxt("levels/tiles.txt", save_data[[0,0],[0,1]], delimiter=";", fmt="%s",header="")
    #with open(filename, "wb") as f:
    #    f.write(save_data)

    #b = np.loadtxt("levels/tiles.txt",dtype=str,delimiter=";")
    #print("2-0,0: ",b[0,0])
