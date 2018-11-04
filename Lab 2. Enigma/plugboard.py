import collections
import copy
from itertools import chain
import string

HEER_LABELS = string.ascii_uppercase
MAX_PAIRS = 10

class PlugboardError(Exception):
    pass

class Plugboard:
    def __init__(self, settings=None):
        self.wiring_map = list(range(26))
        self._backup_map = list(range(26))

        if not settings:
            return 

        wiring_pairs = []
        
        # detect which syntax is being used
        if settings.find('/') != -1:
            # Kriegsmarine syntax
            pairs = settings.split()
            for p in pairs:
                try:
                    m, n = p.split('/')
                    m, n = int(m), int(n)
                except ValueError:
                    raise PlugboardError('invalid pair: %s' % p)

                wiring_pairs.append((m - 1, n - 1))
        else:
            # Heer/Luftwaffe syntax
            pairs = settings.upper().split()

            for p in pairs:
                if len(p) != 2:
                    raise PlugboardError('invalid pair: %s' % p)

                m = p[0]
                n = p[1]
                if m not in HEER_LABELS or n not in HEER_LABELS:
                    raise PlugboardError('invalid pair: %s' % p)

                wiring_pairs.append((ord(m) - ord('A'), ord(n) - ord('A')))

        if len(wiring_pairs) > MAX_PAIRS:
            raise PlugboardError('Please specify %d or less pairs' % MAX_PAIRS)

        counter = collections.Counter(chain.from_iterable(wiring_pairs))
        path, count = counter.most_common(1)[0]
        if count != 1:
            raise PlugboardError('duplicate connection: %d' % path)

        for pair in wiring_pairs:
            m = pair[0]
            n = pair[1]
            if not (0 <= m < 26) or not (0 <= n < 26):
                raise PlugboardError('invalid connection: %s' % str(pair))

            self.wiring_map[m] = n
            self.wiring_map[n] = m

    def signal(self, n):
        return self.wiring_map[n]