
from src.MiniMap import MiniMap
import logging
import sys

class Mappy():
    def __init__(self, application_name: str):
        self.minimap = MiniMap(application_name = application_name)

        pass
    
    def setup(self):
        self.minimap.setup()


    
    def predict(self):
        if(not self.minimap.HAS_VALID_CONFIG):
            logging.error("Mappy setup hasn't been completed")
            sys.exit(1)