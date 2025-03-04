# ray-ponder.py
from RayPonder import player, record

def main():
    # Jouer un fichier audio
    player.play_message()

    # Démarrer l'enregistrement
    record.record_audio()

if __name__ == "__main__":
    main()