# EventLoop.py
import time
import queue
from RayPonder import Player, Recorder
from RayPonder import Events
# from RayPonder.Events import PhyEventLoop, EventTypes, RayEventType


class EventLoop:
    def __init__(self, config):
        self.config = config
        self.event_queue = queue.Queue()
        self.phy_events = Events.PhyEventLoop(self.event_queue, self.config)
        self.player = Player(config, self.event_queue)
        self.player.start()
        self.recorder = Recorder(config, self.event_queue)
        self.recorder.start()

        # self.recorder = Recorder(config)

    def start(self):
        self.phy_events.start()

    def trigger_main_sequence(self):
        self.player.play()
        # self.player.start_playing()
    
    def stop_main_sequence(self):
        self.player.stop()
        # if( self.recorder.recording):
        #     print("stopping recording")
        
    def record(self):
        self.recorder.record()
        
    def stop_record(self):
        self.recorder.stop_recording()
        
    def run(self):
        try:
            while True:
                try:
                    event = self.event_queue.get(timeout=0.5)
                    if (event.ray_event == Events.RayEventType.PickUp):
                        # print("EventLoop() : phone was pickup")
                        self.trigger_main_sequence()
                        # print("playing OK")
                    elif (event.ray_event == Events.RayEventType.HangUp):
                        # print("EventLoop() : phone was Hang Up")
                        self.stop_main_sequence()
                        self.stop_record()
                    elif(event.ray_event == Events.RayEventType.MessagePlayFinished):
                        # print("EventLoop() : Audio message read. Ready to record")
                        self.record()
                    elif(event.ray_event == Events.RayEventType.RecorderTimeout):
                        # print("EventLoop() : Recorder timeout")
                        pass

                        # trigger main sequence
                        # print(f"event producer type {event.producer_type.name} value {event.value.name}")
                except queue.Empty:
                    pass
        except KeyboardInterrupt:
            print("EventLoop() : Arrêt de Player...")
            self.player.shutdown()
            while self.player.running:
                print('EventLoop() : error stopping player')
                time.sleep(0.5)
            print("EventLoop() : Arrêt de Recorder...")
            self.recorder.shutdown()
            while self.recorder.running:
                print("EventLoop() : error stopping recorder")
                time.sleep(0.5)
            print("EventLoop() : Arrêt de l'EventLoop...")
            self.stop()

    def stop(self):
        self.phy_events.stop()

