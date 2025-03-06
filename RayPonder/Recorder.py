# RayPonder/Recorder.py
import pyaudio
import wave
import os
from datetime import datetime
import threading
import time
from RayPonder import Events
import uuid

class Recorder:
    def __init__(self, config = None, queue = None):
        self.config = config['recorder']
        self.queue = queue
        self.recording = False
        self.running = False
        self.p = pyaudio.PyAudio()
        self.generate_uuid = self.config.getboolean('add-uuid')
        self.dest_dir = os.path.join(config['general']['root'], self.config['dest-dir'])
        self.file_name_format = self.config['strftime-template'] + self.config['file-prepend'] 
        # print(f"RECORDER() : dest dir {self.dest_dir}")
        # print(f"RECORDER() : file name format {self.file_name_format}")
        # print(f"RECORDER() : filename example {self.format_name()}")
        self.chunk_size = 1024
        self.framerate = int(self.config['framerate'])
        self.max_duration = int(self.config['recode-timeout']) * 60 # in seconds
        self.channels = int(self.config['channels'])

    def format_name(self):
        filename = datetime.now().strftime(self.file_name_format)
        if self.generate_uuid:
            f_id = uuid.uuid4().hex
            filename = filename + "_" + f_id[0:6] 
            # print(f"uuid {f_id} \n{filename}")
        return filename + self.config['file-ext']

    def start(self):
        self.running = True
        self.thread = threading.Thread( target=self.run, name="Recorder")
        self.thread.start()


    def run(self):
        self.running = True
        while self.running:
            # print("player running")
            if self.recording:
                # print(f"Playing {self.filename}")
                self._record()
            time.sleep(0.1)



    def _record(self):
        # self.max_duration = max_duration
        duration = int(self.framerate / self.chunk_size * self.max_duration)
        stream = self.p.open(format=pyaudio.paInt32,
                              channels=self.channels,
                              rate=self.framerate,
                              input=True,
                              frames_per_buffer=self.chunk_size)
        f_name = self.format_name()
        filename = os.path.join(self.dest_dir, f_name)
        print(f"RECORDER() : recording to {filename}")
        buff = []
        timeout = True
        while self.recording:
            data = stream.read(self.chunk_size)
            buff.append(data)
            duration -= 1
            # print(f"RECORDER() : remaining {self.get_remaining(duration)}") 
            if(not self.recording):
                timeout = False
                # print("RECORDER() : stop recording")
                break
            if(duration == 0):
                self.recording = False
            # wf.writeframes(data)
        if(timeout):
            evt_timeout = Events.RayEvent(producer=self, 
                                   producer_type=Events.EventProducerType.Recorder, 
                                   ray_event=Events.RayEventType.RecorderTimeout)
            self.queue.put(evt_timeout)
        stream.stop_stream()
        stream.close()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt32))
        wf.setframerate(48000)
        wf.writeframes(b''.join(buff))
        wf.close()
        
        
    def get_remaining(self, duration):
        pass
    
    def stop_recording(self):
        self.recording = False
        
    def record(self):
        # print("RECORDER() : Start Recording")
        self.recording = True

        
    def clean_up(self):
        if(self.recording):
            self.stop_recording()
        self.running = False
        self.p.terminate()
        print("RECORDER() : Player closed gracefully")
                
    def shutdown(self):
        self.clean_up()
        self.thread.join()
        


if __name__ == "__main__":
    recorder = Recorder()
    recorder._record()
