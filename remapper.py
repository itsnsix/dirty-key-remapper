import sys
import evdev
from evdev import UInput, ecodes as e

in_dev = evdev.InputDevice('/dev/input/by-id/usb-Razer_Razer_Tartarus_Pro-if01-event-kbd')

in_dev.grab()
ui = UInput()


def close():

    ui.close()
    in_dev.ungrab()
    in_dev.close()
    print('Exiting')
    sys.exit()


remap = {
    'KEY_C, KEY_X, KEY_Z, KEY_LEFTSHIFT': close,
    'KEY_LEFTSHIFT, KEY_Z': 'KEY_LEFTCTRL, KEY_Z',
    'KEY_LEFTSHIFT': 'KEY_LEFTCTRL',
    'KEY_C': 'KEY_M',
    'KEY_X': 'KEY_E',
    'KEY_A': 'KEY_B',
    'KEY_S': 'KEY_LEFTCTRL, KEY_T',
    'KEY_F': 'KEY_ENTER',
    'KEY_CAPSLOCK': "KEY_LEFTSHIFT",
    'KEY_LEFTSHIFT, KEY_X': 'KEY_LEFTCTRL, KEY_RIGHTSHIFT, KEY_Z'
}

active_keys = []
last_down = []

for event in in_dev.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        key = evdev.events.KeyEvent(event)

        if key.keystate == key.key_up:
            ui.write(e.EV_KEY, e.ecodes[key.keycode], 0)

            if key.keycode in active_keys:
                active_keys.pop(active_keys.index(key.keycode))

            for down_key in last_down:
                ui.write(e.EV_KEY, e.ecodes[down_key], 0)
            last_down = []

        elif key.keystate == key.key_down and key.keycode not in active_keys:
            active_keys.append(key.keycode)
            if ', '.join(active_keys) in remap.keys():

                for down_key in last_down:
                    ui.write(e.EV_KEY, e.ecodes[down_key], 0)
                last_down = []

                mapped = remap[', '.join(active_keys)]
                if callable(mapped):
                    mapped()
                else:
                    for key in mapped.split(', '):
                        last_down.append(key)
                        ui.write(e.EV_KEY, e.ecodes[key], 1)

            else:
                last_down.append(key.keycode)
                ui.write(e.EV_KEY, e.ecodes[key.keycode], 1)

        elif key.keystate == key.key_hold:
            continue

        ui.syn()
