import time
from abc import ABC, abstractmethod
from src.Mappy import Mappy
from utils.PrintMemoryMiniMap import array_to_image

class GameBot(ABC):
    def __init__(self, tick_rate: float = 10.0):
        """
        Initialize the bot with a given tick rate (in Hz).
        """
        self.tick_rate = tick_rate
        self.running = False
        self.mappy = Mappy('Paint')
        self.mappy.setup()

    def start(self):
        """
        Start the main event loop.
        """
        self.running = True
        try:
            while self.running:
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
        """
        Stop the event loop.
        """
        self.running = False

    def update(self):
        rng_to_label = {
          (12, 11, 12) : 1,
          (83, 70, 64) : 2,
          (98, 96, 73) : 3
        }
        self.mappy.minimap.screenshot_minimap() 
        array_to_image(self.mappy.minimap.setup_internal_mini_map(rng_to_label, tolerance=30))
        print('printed')



if __name__ == "__main__":
    time.sleep(5)
    bot = GameBot(tick_rate=60.0)  # 5 ticks per second
    bot.start()