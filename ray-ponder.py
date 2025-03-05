# ray-ponder.py
import configparser
#from configobj import ConfigObj
from RayPonder.EventLoop import EventLoop
import threading

def main():

    config = configparser.ConfigParser()
    config.read('ray-ponder.conf')
    event_loop = EventLoop(config)
    event_loop.start()
    event_loop.run()

if __name__ == "__main__":
    main()
    # threading.main_thread().join()
