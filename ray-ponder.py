# ray-ponder.py
import configparser
#from configobj import ConfigObj
from RayPonder.EventLoop import EventLoop
import threading
import os
import sys


def main():

    config = configparser.ConfigParser()
    config.read('ray-ponder.conf')
    root = config['general']['root']
    if(os.path.exists(root) ):
        print("ROOT EXISTS OK")          
    else:
        print("ERROR !!!\nRoot folder does not exists. Check config file.")
        sys.exit(20)
    event_loop = EventLoop(config)
    event_loop.start()
    event_loop.run()

if __name__ == "__main__":
    main()
    # threading.main_thread().join()
