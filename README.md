# dirty-key-remapper

Quick script for grabbing keys from one device and writing as another.
Used specifically for remapping Razer Tartarus Pro keys on Ubuntu 20.04.

Largely untested. I'll fix bugs as I find them. YMMV

## How to use

Install [evdev](https://python-evdev.readthedocs.io/en/latest/index.html): `pip3 install evdev`


Choose the input device from /dev/inputs/
```py
in_dev = evdev.InputDevice('/dev/input/by-id/usb-Razer_Razer_Tartarus_Pro-if01-event-kbd')
```

Specify your key remappings in the `remap` dict. Note that order matters. You can map to keys or to functions. 
```py
remap = {
    'KEY_C, KEY_X, KEY_Z, KEY_LEFTSHIFT': close,
    'KEY_LEFTSHIFT, KEY_Z': 'KEY_RIGHTCTRL, KEY_Z',
    'KEY_LEFTSHIFT, KEY_X': 'KEY_RIGHTCTRL, KEY_RIGHTSHIFT, KEY_Z'
}
```

Run with `sudo python3 remapper.py`

By default pressing C-X-Z-LSHIFT (19-18-17-16 on the Tartarus) will execute the close command and terminate the program. You can change this in the remap dict.
