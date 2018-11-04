import string
import collections
from data import ROTORS, REFLECTORS

ALPHA_LABELS = string.ascii_uppercase
WIRING_FREQ_SET = set((letter, 1) for letter in ALPHA_LABELS)

class RotorError(Exception):
    pass

class Rotor:
    def __init__(self, model_name, wiring, ring_setting=0, stepping=None):
        self.name = model_name
        self.wiring_str = wiring.upper()
        self.ring_setting = ring_setting
        self.pos = 0
        self.rotations = 0

        if len(self.wiring_str) != 26:
            raise RotorError("invalid wiring length")

        for c in self.wiring_str:
            if c not in ALPHA_LABELS:
                raise RotorError("invalid wiring: %s" % wiring)
        
        input_set = set(collections.Counter(self.wiring_str).items())
        if input_set != WIRING_FREQ_SET:
            raise RotorError("invalid wiring frequency")
        
        if not isinstance(ring_setting, int) or not (0 <= ring_setting < 26):
            raise RotorError("invalid ring_setting")

        self.entry_map = [ord(pin) - ord('A') for pin in self.wiring_str]
        
        self.exit_map = [0] * 26
        for i, v in enumerate(self.entry_map):
            self.exit_map[v] = i

        self.display_map = {}
        for n in range(26):
            self.display_map[chr(ord('A') + n)] = (n - self.ring_setting) % 26

        self.pos_map = {v : k for k, v in self.display_map.items()}

        self.step_set = set()
        if stepping is not None:
            for pos in stepping:
                if pos in self.display_map:
                    self.step_set.add(pos)
                else:
                    raise RotorError("stepping: %s" % pos)
        
        self.set_display('A')

    def set_display(self, val):
        s = val.upper()
        if s not in self.display_map:
            raise RotorError("bad display value %s" % val)

        self.pos = self.display_map[s]
        self.display_val = s
        self.rotations = 0

    def notch_over_pawl(self):    
        return self.display_val in self.step_set

    def rotate(self):
        self.pos = (self.pos + 1) % 26
        self.display_val = self.pos_map[self.pos]
        self.rotations += 1

    def signal_in(self, n):
        pin = (n + self.pos) % 26

        contact = self.entry_map[pin]

        return (contact - self.pos) % 26

    def signal_out(self, n):
        contact = (n + self.pos) % 26

        pin = self.exit_map[contact]

        return (pin - self.pos) % 26


def create_rotor(model, ring_setting=0):
    if model in ROTORS:
        data = ROTORS[model]
        return Rotor(model, data['wiring'], ring_setting, data['stepping'])

    raise RotorError("Unknown rotor type: %s" % model)


def create_reflector(model):
    if model in REFLECTORS:
        return Rotor(model, wiring=REFLECTORS[model])

    raise RotorError("Unknown reflector type: %s" % model)