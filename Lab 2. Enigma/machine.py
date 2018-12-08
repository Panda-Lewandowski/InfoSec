import string
from plugboard import Plugboard
from rotor import Rotor, create_reflector, create_rotor

KEYBOARD_CHARS = string.ascii_uppercase
KEYBOARD_SET = set(KEYBOARD_CHARS)

class EnigmaError(Exception):
    pass

class EnigmaMachine:
    def __init__(self, rotors='I II III', ring_settings=None,
            reflector='B', plugboard_settings=None):
        
        if isinstance(rotors, str):
            rotors = rotors.split()

        num_rotors = len(rotors)
        if num_rotors not in (3, 4):
            raise EnigmaError("invalid rotors list size")

        if ring_settings is None:
            ring_settings = [0] * num_rotors
        elif isinstance(ring_settings, str):
            strings = ring_settings.split()
            ring_settings = []
            for s in strings:
                if s.isalpha():
                    ring_settings.append(ord(s.upper()) - ord('A'))
                elif s.isdigit():
                    ring_settings.append(int(s) - 1)
                else:
                    raise EnigmaError('invalid ring setting: %s' % s)

        if num_rotors != len(ring_settings):
            raise EnigmaError("# of rotors doesn't match # of ring settings")

        rotor_list = [create_rotor(r[0], r[1]) for r in zip(rotors, ring_settings)]

        self.rotors = rotor_list
        self.rotor_count = len(rotors)
        self.reflector = create_reflector(reflector)
        self.plugboard = Plugboard(plugboard_settings)

    def set_display(self, val):
        if len(val) != self.rotor_count:
            raise EnigmaError("Incorrect length for display value")

        for i, rotor in enumerate(reversed(self.rotors)):
            rotor.set_display(val[-1 - i])

    def key_press(self, key):
        if key not in KEYBOARD_SET:
            raise EnigmaError('illegal key press %s' % key)

        self._step_rotors()

        signal_num = ord(key) - ord('A')
        lamp_num = self._electric_signal(signal_num)
        return KEYBOARD_CHARS[lamp_num]

    def _step_rotors(self):
        rotor1 = self.rotors[-1]
        rotor2 = self.rotors[-2]
        rotor3 = self.rotors[-3]

        rotate2 = rotor1.notch_over_pawl() or rotor2.notch_over_pawl()
        rotate3 = rotor2.notch_over_pawl()

        rotor1.rotate()
        if rotate2:
            rotor2.rotate()
        if rotate3:
            rotor3.rotate()

    def _electric_signal(self, signal_num):
        pos = self.plugboard.signal(signal_num)

        for rotor in reversed(self.rotors):
            pos = rotor.signal_in(pos)

        pos = self.reflector.signal_in(pos)

        for rotor in self.rotors:
            pos = rotor.signal_out(pos)

        return self.plugboard.signal(pos)

    def process_text(self, text):
        result = []
        for key in text:
            c = key.upper()

            if c not in KEYBOARD_SET: 
                if c == '=' or c in string.digits:
                    result.append(c)
                    continue
                else:
                    raise EnigmaError('illegal symbol')
                    
            result.append(self.key_press(c))

        return ''.join(result)
    