# PhyEvents.py
import evdev
import threading
import queue
# from RayPonder.Events import EventProducerType, RayEventType
from RayPonder import Events



        

class PhyEventLoop:
    def __init__(self, queue, config):
        self.device_path = config['phy-event']['gpio-dev-input']
        self.pickup_state = int(config["phy-event"]["pickup-state"])
        print(f"PhyEventLoop() : current state {self.pickup_state}")
        self.device = evdev.InputDevice(self.device_path)
        self.event_queue = queue
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.read_events)
        self.thread.start()

    def read_events(self):
        while self.running:
            try:
                event = self.device.read_one()
                if event:
                    # print(event)
                    if (event.type == evdev.ecodes.EV_KEY and event.code == evdev.ecodes.KEY_F12):
                        print(f"PhyEventLoop() : Event received -> {event}")
                        key_ev = Events.RayEvent(producer=self, producer_type=Events.EventProducerType.Keyboard, ray_event=Events.RayEventType.HangUp)
                        if (event.value == self.pickup_state):
                            key_ev.ray_event = Events.RayEventType.PickUp
                            # print(f"ending value {key_ev.ray_event.name}")
                        print(f"PhyEventLoop() : sending -> {key_ev.ray_event.name}")
                        self.event_queue.put(key_ev)
            except queue.Empty:
                pass

    def stop(self):
        self.running = False
        self.thread.join()

    def get_event(self):
        try:
            return self.event_queue.get(timeout=1)
        except queue.Empty:
            return None

