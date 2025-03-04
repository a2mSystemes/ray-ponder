# RayPonder/record.py
import pyaudio
import wave
import threading
from pynput import keyboard
import time
import os

# Paramètres d'enregistrement
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 15 * 60  # 15 minutes
temp_folder = './temp_audio/'

if not os.path.exists() or not os.path.isdir():
    try:
        os.mkdir(temp_folder)
    except OSError:
        print("impossible de créer le dossier temp_audio")
else:
    print("dossier temp_audio existant")

# Création d'un objet PyAudio
p = pyaudio.PyAudio()

# Ouvrir le flux audio
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Variable pour stocker l'état de l'enregistrement
recording = True


def record_audio():
    global recording
    frames = []
    while recording:
        # print("recording")
        # time.sleep(0.5)
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def on_press(key):
    global recording
    if key == keyboard.Key.f12:
        recording = False
        return False

def main():
        # Démarrer la surveillance des appuis sur les touches du clavier
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    # Démarrer l'enregistrement
    record_thread = threading.Thread(target=record_audio)
    record_thread.start()



    # Attendre la fin de l'enregistrement
    # record_thread.join()
    listener.join()

if __name__ == "__main__":
    main()