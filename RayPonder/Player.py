# RayPonder/Player.py
import threading
import pyaudio
import wave
import time

import threading
from RayPonder import Events




class Player():
    def __init__(self, config, queue):
        self.evt_qu = queue
        self.config = config
        # TODO mettre filename dans fichier de config
        self.filename = './messages/Cabine6.wav'
        self.p = pyaudio.PyAudio()
        self.playing = False
        self.stopped = True
        self.running = False
        self.stream = None
        self.open_stream()
        # self.reading = False


    def open_stream(self):
        with (wave.open(self.filename, 'rb')) as wf:
            self.stream = self.p.open(
                format=self.p.get_format_from_width( wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(), output=True
            )
        
    def start(self):
        self.running = True
        self.thread = threading.Thread( target=self.run, name="Player")
        self.thread.start()
        
    def run(self):
        self.running = True
        while self.running:
            # print("player running")
            if self.playing:
                # print(f"Playing {self.filename}")
                self._play_audio()
            elif self.stopped:
                pass
                # print(f"player stopped")
            time.sleep(0.1)
            
    def _play_audio(self):
        wf = wave.open(self.filename, 'rb')
        data = wf.readframes(1024)
        if(self.stream is not None and self.stream.is_stopped()):
            self.open_stream()
        
        while len(data) > 0 and self.playing:
            # print(f"playing {self.playing}")
            self.stream.write(data)
            data = wf.readframes(1024)
            # print(f"PLAYER() : playing -> {self.playing}")
            # print(f"remaining {wf.tell()}")
        if(wf.tell() == wf.getnframes()):
            #need to send a message to say we can record....
            print("PLAYER() : sending EndOfMessage")
            evt = Events.RayEvent(producer=self, ray_event=Events.RayEventType.MessagePlayFinished)
            self.evt_qu.put(evt)
        self.stream.stop_stream()
        self.stop()

        
        

    def play(self):
        self.playing = True
        self.stopped = False
        print(f"PLAYER() : playing {self.playing}, stopped {self.stopped}")
        # print(f"not self.running {not self.running}")
        

    def stop(self):
        self.playing = False
        self.stopped = True
        print(f"PLAYER() : playing {self.playing}, stopped {self.stopped}")
        

    def clean_up(self):
        self.running = False
        self.stop = self.playing = False
        print(f"PLAYER() :playing : {self.playing}, stopped : {self.stopped}")
        self.p.terminate()
        self.stream.close()
        print("PLAYER() : Player closed gracefully")

    def shutdown(self):
        self.clean_up()
        self.thread.join()
    
