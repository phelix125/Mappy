
from src.MiniMap import MiniMap
class Mappy():
    def __init__(self, application_name: str):
        self.minimap = MiniMap(application_name = application_name)

        pass
    
    def setup(self):
        self.minimap.setup()


    
    def locate_map(self):
        pass