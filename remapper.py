import sys
import evdev
from evdev import UInput, ecodes as e

in_dev = evdev.InputDevice('/dev/input/by-id/usb-Razer_Razer_Tartarus_Pro-if01-event-kbd')
out_dev = evdev.InputDevice('/dev/input/by-id/usb-Microsoft_Natural®_Ergonomic_Keyboard_4000-if01-event-kbd')

in_dev.grab()
ui = UInput.from_device(out_dev)


def close():

    ui.close()
    in_dev.ungrab()
    in_dev.close()
    out_dev.close()
    print('Exiting')
    sys.exit()


remap = {
    'KEY_C, KEY_X, KEY_Z, KEY_LEFTSHIFT': close,
    'KEY_LEFTSHIFT, KEY_Z': 'KEY_RIGHTCTRL, KEY_Z',
    'KEY_LEFTSHIFT, KEY_X': 'KEY_RIGHTCTRL, KEY_RIGHTSHIFT, KEY_Z'
}

active_keys = []

for event in in_dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        key = evdev.events.KeyEvent(event)
        if key.keystate == key.key_up and key.keycode in active_keys:
            active_keys.pop(active_keys.index(key.keycode))
            continue
        elif key.keystate == key.key_down and key.keycode not in active_keys:
            active_keys.append(key.keycode)

        if ', '.join(active_keys) in remap.keys():
            mapped = remap[', '.join(active_keys)]
            if callable(mapped):
                mapped()
            else:
                for key in mapped.split(', '):
                    ui.write(e.EV_KEY, evdev.ecodes.ecodes[key], 1)
                for key in mapped.split(', '):
                    ui.write(e.EV_KEY, evdev.ecodes.ecodes[key], 0)
                ui.syn()
