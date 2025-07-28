import time
from src.Mappy import Mappy
from utils.PrintMemoryMiniMap import array_to_image

def test_image_maze_generation(runs:int, tolerance):
    m = Mappy()
    m.setup()
    m.minimap.screenshot_minimap()
    rng_to_label = {
    (12, 11, 12) : 1,
    (83, 70, 64) : 2,
    (98, 96, 73) : 3
    }
    
    start = time.time()
    for _ in range(runs):
        m.minimap.setup_internal_mini_map(rng_to_label, tolerance=tolerance)
    end = time.time()
    
    print(f'Compeleted {runs} in {end-start} seconds, Avg run: {(end-start) / runs}')
    

test_image_maze_generation(100, 20)