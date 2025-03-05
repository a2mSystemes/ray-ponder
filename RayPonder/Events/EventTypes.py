from enum import Enum
from evdev import ecodes


class EventTypes(Enum):
    
    """Keyboad event types"""
    PickUp = ecodes.KEY_F12
    Recording = ecodes.KEY_F11
    Playing = ecodes.KEY_F10
    FileSyn = ecodes.KEY_F9
    RecordTimeout = ecodes.KEY_F8
    
    
class EventVal(Enum):
    Pressed = 1
    Released = 0
    
class EventProducerType(Enum):
    Keyboard = ecodes.EV_KEY
    Timer = ecodes.EV_MAX
    Unknown = -1
    Player = 300
    Recorder = 301
        

class RayEventType(Enum):
    Unknown = 0
    PickUp = 1
    HangUp = 2
    MessagePlayFinished = 10
    RecordFinished = 20
    RecorderTimeout = 21
    
    