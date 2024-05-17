from typing import Tuple




class races:
    
    def __init__(self,     
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
    ):
        self.name = name
        self.char = char
        self.color = color
        




class mario(races):

    def __init__(self, char: str = "?", color: Tuple[int, int, int] = (255, 255, 255), name: str = "<Unnamed>"):
              
        super().__init__(char, color, name)