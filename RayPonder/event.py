import evdev



def check_f12(event):
    print("test")
    if event.code == evdev.ecodes.KEY_F12:
        return True  # F12 key was pressed  *
    
        
if __name__ == "__main__":
    evdev.main()
    