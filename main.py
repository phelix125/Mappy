from src.Mappy import Mappy
import logging
import os
from datetime import datetime

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{datetime.now():%Y-%m-%d}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler() 
    ]
)

def main():
  m = Mappy(application_name = 'Paint')
  
  
if __name__ == '__main__':  
  main()
