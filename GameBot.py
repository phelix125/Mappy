import time
from abc import ABC, abstractmethod
from src.Mappy import Mappy
from utils.PrintMemoryMiniMap import array_to_image

class GameBot(ABC):
    def __init__(self, tick_rate: float = 10.0):
        self.tick_rate = tick_rate
        self.running = False
        self.ticks = 0
        self.mappy = Mappy('Paint')
        self.mappy.setup()

    def start(self):
        
        self.running = True
        try:
            while self.running:
                self.ticks +=1
                start_time = time.time()
                self.update()
                elapsed = time.time() - start_time
                sleep_time = max(0, (1 / self.tick_rate) - elapsed)
                time.sleep(sleep_time)
        except KeyboardInterrupt:
            print("Bot interrupted.")
        finally:
            self.stop()

    def stop(self):
        self.running = False

    def update(self):
        rng_to_label = {
          (0, 0, 0) : 1,
          (132, 100, 53) : 2,
          (28, 138, 218) : 3
        }
        self.mappy.minimap.screenshot_minimap() 
        array_to_image(self.mappy.minimap.setup_internal_mini_map(rng_to_label))
        print('printed')



if __name__ == "__main__":
    time.sleep(3)
    bot = GameBot(tick_rate=0.5)
    bot.start()