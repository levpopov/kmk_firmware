import keypad

from kmk.scanners import DiodeOrientation, Scanner


class KeypadScanner(Scanner):
    '''
    Translation layer around a CircuitPython 7 keypad scanner.

    :param pin_map: A sequence of (row, column) tuples for each key.
    :param kp: An instance of the keypad class.
    '''

    def __init__(self):
        # for split keyboards, the offset value will be assigned in Split module
        self.offset = 0
        self.coord_mapping = tuple(range(self.key_count))
        self.curr_event = keypad.Event()

    @property
    def key_count(self):
        return self.keypad.key_count

    def scan_for_changes(self):
        '''
        Scan for key events and return a key report if an event exists.

        The key report is a byte array with contents [row, col, True if pressed else False]
        '''
        ev = self.curr_event
        has_event = self.keypad.events.get_into(ev)
        if has_event:
            if self.offset:
                return keypad.Event(ev.key_number + self.offset, ev.pressed)
            else:
                return ev


class MatrixScanner(KeypadScanner):
    '''
    Row/Column matrix using the CircuitPython 7 keypad scanner.

    :param row_pins: A sequence of pins used for rows.
    :param col_pins: A sequence of pins used for columns.
    :param direction: The diode orientation of the matrix.
    '''

    def __init__(
        self,
        row_pins,
        column_pins,
        *,
        columns_to_anodes=DiodeOrientation.COL2ROW,
        interval=0.02,
        max_events=64,
    ):
        self.keypad = keypad.KeyMatrix(
            row_pins,
            column_pins,
            columns_to_anodes=(columns_to_anodes == DiodeOrientation.COL2ROW),
            interval=interval,
            max_events=max_events,
        )
        super().__init__()


class KeysScanner(KeypadScanner):
    '''
    GPIO-per-key 'matrix' using the native CircuitPython 7 keypad scanner.

    :param pins: An array of arrays of CircuitPython Pin objects, such that pins[r][c] is the pin for row r, column c.
    '''

    def __init__(
        self,
        pins,
        *,
        value_when_pressed=False,
        pull=True,
        interval=0.02,
        max_events=64,
    ):
        self.keypad = keypad.Keys(
            pins,
            value_when_pressed=value_when_pressed,
            pull=pull,
            interval=interval,
            max_events=max_events,
        )
        super().__init__()
