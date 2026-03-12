import os

"""Utility helpers for working with simple 'macro' event streams.

The previous version of this file contained two hard‑coded lists and an
incomplete ``addLists`` helper.  In the context of the project a "macro"
is simply a sequence of input events (mouse moves, key presses, etc.)
each of which is recorded together with a timestamp or a time delta.  One
common operation is to take two independent macro recordings and merge them
so that they can be replayed simultaneously: the resulting stream should
contain every event from both recordings in chronological order.

Below are helpers that demonstrate how this can be done generically.  A
more fully‑featured version could parse the InformaalTask recording format
shown previously, but here we just use simple tuples for clarity.
"""


"""Example macros for demonstration.  Each tuple consists of an absolute
timestamp (milliseconds from start) and a string describing the event.

Coordinate events use a comma between the x and y values (``MOVE 100,100``)
to match the format you mentioned; the parser/formatter treats everything
after the first space as the payload so the comma is preserved intact.
"""

macro_a = [
    (0,  'MOVE 100,100'),
    (120, 'MOUSE_DOWN left'),
    (240, 'MOUSE_UP left'),
]

macro_b = [
    (50,  'KEY_DOWN A'),
    (180, 'KEY_UP A'),
    (300, 'KEY_DOWN B'),
]


def merge_macros(m1, m2):
    """Return a new list containing all events from ``m1`` and ``m2`` sorted
    by their timestamp.  If the inputs are given as lists of
    ``(time, data)`` tuples then the result will be the same format.

    This is essentially the same as merging two sorted lists; if you are
    working with time deltas instead of absolute timestamps you may want to
    convert them first with :func:`deltas_to_absolute` (below) and, after
    merging, convert back with :func:`absolute_to_deltas`.
    """

    # both lists are assumed to already be sorted by time
    i, j = 0, 0
    merged = []
    while i < len(m1) and j < len(m2):
        if m1[i][0] <= m2[j][0]:
            merged.append(m1[i])
            i += 1
        else:
            merged.append(m2[j])
            j += 1
    # append any leftovers
    merged.extend(m1[i:])
    merged.extend(m2[j:])
    return merged


class Macro:
    """Simple container for a sequence of timestamped events.

    ``events`` is a list of ``(time_ms, data)`` tuples and is always sorted
    by time.  You can merge two macros with the ``+`` operator, which will
    create a new :class:`Macro` containing events from both inputs in the
    proper order.  The :meth:`run` method will replay the macro, calling an
    optional callback for each event.
    """

    def __init__(self, events=None):
        self.events = sorted(events or [], key=lambda x: x[0])

    @classmethod
    def from_deltas(cls, deltas):
        return cls(deltas_to_absolute(deltas))

    @classmethod
    def from_file(cls, path):
        return cls(parse_recording(path))

    def __add__(self, other):
        if not isinstance(other, Macro):
            return NotImplemented
        return Macro(merge_macros(self.events, other.events))

    def run(self, callback=None):
        """Iterate through events, waiting between them to simulate real time.

        ``callback`` is an optional function called with ``(time, event)``
        for each entry; if omitted the events are simply printed.
        """

        import time

        if not self.events:
            return
        start = self.events[0][0]
        last = start
        for t, ev in self.events:
            # compute how long to wait from the previous event
            wait = (t - last) / 1000.0
            if wait > 0:
                time.sleep(wait)
            if callback:
                callback(t, ev)
            else:
                print(f"[{t}ms] {ev}")
            last = t


def deltas_to_absolute(deltas):
    """Convert a list of ``(delta, event)`` into ``(time, event)`` where
    ``time`` is the accumulated sum of all previous deltas."""

    result = []
    total = 0
    for dt, ev in deltas:
        total += dt
        result.append((total, ev))
    return result


def absolute_to_deltas(abs_events):
    """Convert ``(time, event)`` pairs back to ``(delta, event)`` format."""

    if not abs_events:
        return []
    result = []
    prev = abs_events[0][0]
    result.append((prev, abs_events[0][1]))
    for t, ev in abs_events[1:]:
        result.append((t - prev, ev))
        prev = t
    return result


def format_recording(abs_events):
    """Take a list of ``(time_ms, event)`` pairs and return a list of
    strings in the original ``TYPE|DURATION|DATA`` format.

    The ``event`` portion is expected to begin with the event type, a
    literal colon, and then any remaining data (e.g. ``"KEY_DOWN:e"``).
    If no colon is present the entire string is treated as the type and the
    data field is left empty.  The durations in the output are deltas, so
    the returned lines can be written straight back to a recording file.
    """

    lines = []
    prev_time = 0
    for t, ev in abs_events:
        # compute delta from previous event time
        dt = t - prev_time
        prev_time = t

        # split the stored event string into type and data.  we expect the
        # internal representation to contain either a colon separating the
        # pieces (``"KEY_DOWN:A"``) or a space separated type and payload
        # (``"MOVE 100 200"``).
        if ':' in ev:
            typ, data = ev.split(':', 1)
        else:
            parts = ev.split(' ', 1)
            typ = parts[0]
            data = parts[1] if len(parts) > 1 else ''

        # keep the entire remainder of the string as the data payload; a
        # move event like "MOVE 100 100" will therefore produce "100 100"
        # in the output, and a key event like "KEY_DOWN A" will produce
        # "A".  the earlier version tried to drop anything after the first
        # space, which accidentally truncated coordinates.

        lines.append(f"{typ}|{dt}|{data}")
    return lines


def write_recording(path, abs_events):
    """Write a merged/modified macro back to disk in recording format.

    ``abs_events`` should be a list of ``(time, event)`` tuples; the
    function will convert to deltas and write the appropriate text lines.
    """

    with open(path, 'w', encoding='utf-8') as f:
        for line in format_recording(abs_events):
            f.write(line + '\n')


def parse_recording(path):
    """Read an InformaalTask recording file and return a list of `(time,
    event_string)` pairs.

    The file format is described in the comment header of the sample the
    user provided: each non‑comment line contains ``TYPE|DURATION|DATA``.  The
    ``DURATION`` field is the number of milliseconds since the previous
    event; this function accumulates them into absolute times.
    """

    events = []
    time = 0
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            # allow a leading hashtag on a real macro line; users often
            # copy/paste text with a '#' prefix but still want the event to be
            # parsed.  We therefore strip at most one leading '#' before
            # processing.  A line consisting solely of '#' (or '#' plus
            # whitespace) will be ignored.
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                # remove a single leading hash and any following whitespace;
                # this leaves "#KEY_DOWN|0|a" -> "KEY_DOWN|0|a" but will
                # still drop "##comment" (empty after stripping) if the user
                # truly wants a comment.
                line = line[1:].lstrip()
                if not line:
                    continue
            parts = line.split('|', 2)
            if len(parts) < 3:
                # malformed line, just skip it
                continue
            typ, dur, data = parts
            try:
                dt = int(dur)
            except ValueError:
                dt = 0
            time += dt
            events.append((time, f"{typ}:{data}"))
    return events


def parse_recording_lines(lines):
    """Parse an iterable of recording lines (strings) and return the same
    output as :func:`parse_recording`.  This is useful for testing or for
    when you already have the lines in memory rather than in a file.

    Example::

        >>> lines = ['KEY_DOWN|0|e', 'KEY_UP|316|e', 'KEY_DOWN|20|t']
        >>> parse_recording_lines(lines)
        [(0, 'KEY_DOWN:e'), (316, 'KEY_UP:e'), (336, 'KEY_DOWN:t')]
    """

    events = []
    time = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            line = line[1:].lstrip()
            if not line:
                continue
        parts = line.split('|', 2)
        if len(parts) < 3:
            continue
        typ, dur, data = parts
        try:
            dt = int(dur)
        except ValueError:
            dt = 0
        time += dt
        events.append((time, f"{typ}:{data}"))
    return events


def sheet_to_macro(sheet, keymap, bpm):
    """Convert simple sheet-music instructions into a :class:`Macro`.

    ``sheet`` is an iterable of ``(note, beats)`` pairs, where ``note`` is
    either a key present in ``keymap`` or ``None``/``'REST'`` to indicate a
    pause.  ``keymap`` maps note names to the corresponding keyboard event
    string (e.g. ``{'C4': 'A', 'D4': 'S'}``).  ``bpm`` is the tempo in beats
    per minute; durations are converted to milliseconds using
    ``60000 / bpm`` as the length of one beat.

    The generated macro contains ``KEY_DOWN``/``KEY_UP`` events for each
    note, spaced according to the specified durations.  Rests simply advance
    the current time without emitting events.
    """

    beat_ms = 60000.0 / bpm
    events = []
    current_time = 0
    first = True
    for note, beats in sheet:
        # allow a few ways to express a rest
        if note is None or note == 'REST':
            current_time += int(beat_ms * beats)
            continue
        # insert a small padding before each new key (but not before the very
        # first one) so that the macro playback has a 20 ms gap between presses.
        if not first:
            current_time += 20
        first = False

        original_note = note
        key = keymap.get(note)
        # if the exact note isn't in the map, try transposing up by octaves
        # until we either find a binding or reach a reasonable limit.
        if key is None:
            for octave in range(1, 6):
                # move note name up an octave (e.g. C2 -> C3)
                if note[-1].isdigit():
                    base = note[:-1]
                    num = int(note[-1]) + octave
                    note = f"{base}{num}"
                else:
                    note = original_note
                key = keymap.get(note)
                if key is not None:
                    print(f"transposed {original_note} -> {note} to match keymap")
                    break
        if key is None:
            # still unknown: skip and warn
            print(f"warning: no keybind for note {original_note!r}, skipping")
            current_time += int(beat_ms * beats)
            continue
        duration_ms = int(beat_ms * beats)
        events.append((current_time, f"KEY_DOWN:{key}"))
        current_time += duration_ms
        events.append((current_time, f"KEY_UP:{key}"))
    return Macro(events)


def parse_sheet_lines(lines):
    """Parse a very simple textual sheet-music format.

    Each non-blank line should be ``NOTE DURATION`` where DURATION is in
    beats (can be float).  Example::

        C4 1
        D4 0.5
        REST 0.5

    Returns a list of ``(note, beats)`` tuples as expected by
    :func:`sheet_to_macro`.  Blank lines and lines starting with ``#`` are
    ignored.
    """

    result = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        note = parts[0]
        try:
            beats = float(parts[1])
        except ValueError:
            continue
        result.append((note, beats))
    return result




def parse_keybinds(text):
    """Convert a block of lines like ``X  = C4`` into a dictionary.

    Lines may be separated by newline and can include blanks or comments
    starting with ``#``.  The left-hand side is the key you press on the
    keyboard; the right-hand side is a note name.  Example::

        1  = C3
        !  = C#3

    The returned dictionary maps *note names* to the corresponding key
    string (the inverse of the raw input).  This is the format expected
    by :func:`sheet_to_macro` where the mapping is used to look up which
    key to emit for each note.
    """
    km = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            key, note = line.split('=', 1)
            km[note.strip()] = key.strip()
    return km



def musicxml_to_macro(path, keymap, bpm, padding=0):
    """Produce a :class:`Macro` directly from a MusicXML/MIDI file.

    This helper combines ``musicxml_to_sheet`` and ``sheet_to_macro`` logic but
    respects the musical offsets so that voices and chords play simultaneously.
    ``keymap`` is as for :func:`sheet_to_macro`, and ``bpm`` gives the tempo.
    ``padding`` can be used to insert an extra millisecond gap before each
    key press, similar to the behaviour in :func:`sheet_to_macro` (useful if
    your macro runner needs a minimum separation).  The default is zero
    because offsets already space events appropriately.
    """
    # convert the score to a list of (offset, note, beats) triples
    sheet = musicxml_to_sheet(path)
    beat_ms = 60000.0 / bpm
    events = []
    for offset, note, beats in sheet:
        # ignore rests
        if note is None or note == 'REST':
            continue
        original_note = note
        key = keymap.get(note)
        if key is None:
            for octave in range(1, 6):
                if note[-1].isdigit():
                    base = note[:-1]
                    num = int(note[-1]) + octave
                    note = f"{base}{num}"
                else:
                    note = original_note
                key = keymap.get(note)
                if key is not None:
                    print(f"transposed {original_note} -> {note} to match keymap")
                    break
        if key is None:
            print(f"warning: no keybind for note {original_note!r}, skipping")
            continue
        start_ms = int(offset * beat_ms)
        dur_ms = int(beats * beat_ms)
        # apply optional padding before each press
        if padding:
            start_ms += padding
        events.append((start_ms, f"KEY_DOWN:{key}"))
        events.append((start_ms + dur_ms, f"KEY_UP:{key}"))
    # sort so overlapping voices are ordered by time
    events.sort(key=lambda x: x[0])
    return Macro(events)
    """Parse a MusicXML or MIDI file into a simple sheet representation.

    The original implementation returned just ``(note, beats)`` pairs in the
    order encountered, which made it impossible to distinguish timing or
    allow simultaneous notes.  This version includes the starting offset
    (measured in quarter-beats) for each note so that later stages can sort
    and schedule events correctly.

    The returned list contains tuples of ``(offset, note, beats)``.  ``offset``
    is the distance from the beginning of the score in quarter notes (i.e.
    one beat = 1.0).  ``note`` is the pitch name with octave, and ``beats`` is
    the duration in quarter lengths.  Rests are not explicitly represented –
    gaps between offsets imply silence.

    Requires the ``music21`` library (``pip install music21``).
    """
    try:
        from music21 import converter
    except ImportError:
        raise ImportError("music21 is required to parse MusicXML/MIDI; install it with `pip install music21`")

    score = converter.parse(path)
    sheet = []
    # ``score.flat.notes`` may contain Note and Chord objects; expand chords
    # into their constituent pitches but preserve the starting offset so that
    # notes that begin at the same moment remain simultaneous.
    for element in score.flat.notes:
        start = float(element.offset)
        dur = float(element.quarterLength)
        if element.isChord:
            for p in element.pitches:
                sheet.append((start, p.nameWithOctave, dur))
        else:
            sheet.append((start, element.nameWithOctave, dur))
    return sheet
def _demo():
    # demonstrate the Macro class and merger using the hardcoded examples
    m1 = Macro(macro_a)
    m2 = Macro(macro_b)
    print('macro 1:', m1.events)
    print('macro 2:', m2.events)
    combined = m1 + m2
    print('combined events:', combined.events)

    # run the merged macro (prints with delays)
    print('running merged macro...')
    combined.run()

    # also show conversion to deltas if desired
    print('combined as deltas:', absolute_to_deltas(combined.events))

    # demonstrate parsing from raw lines such as the format the user
    # highlighted in their last message
    raw = [
        'KEY_DOWN|0|e',
        'KEY_UP|316|e',
        'KEY_DOWN|20|t',
    ]
    print('\nparsed example lines:', parse_recording_lines(raw))
    # merge two small recordings and run them
    r1 = Macro(parse_recording_lines(raw))
    r2 = Macro(macro_b)
    combo = r1 + r2
    print('running combined example recordings...')
    combo.run()

    # write the merged events back out in the original text format
    out_path = 'merged.txt'
    write_recording(out_path, combo.events)
    print(f"wrote merged macro to {out_path}")

    # show sheet-music conversion using a complete keybind map
    keymap_text = '''
1  = C3
!  = C#3
2  = D3
@  = D#3
3  = E3
4  = F3
$  = F#3
5  = G3
%  = G#3
6  = A3
^  = A#3
7  = B3

8  = C4
*  = C#4
9  = D4
(  = D#4
0  = E4
q  = F4
Q  = F#4
w  = G4
W  = G#4
e  = A4
E  = A#4
r  = B4

t  = C5
T  = C#5
y  = D5
Y  = D#5
u  = E5
i  = F5
I  = F#5
o  = G5
O  = G#5
p  = A5
P  = A#5
a  = B5

s  = C6
S  = C#6
d  = D6
D  = D#6
f  = E6
g  = F6
G  = F#6
h  = G6
H  = G#6
j  = A6
J  = A#6
k  = B6

l  = C7
L  = C#7
z  = D7
Z  = D#7
x  = E7
c  = F7
C  = F#7
v  = G7
V  = G#7
b  = A7
B  = A#7
n  = B7
m  = C8
'''
    keymap = parse_keybinds(keymap_text)
    sheet = [('C4', 1), ('D4', 0.5), ('E4', 1), ('REST', 0.5), ('C4', 2)]
    print('\nexample sheet:', sheet)
    macro_from_sheet = sheet_to_macro(sheet, keymap, bpm=120)
    print('generated macro from sheet:', macro_from_sheet.events)
    print('running sheet-derived macro...')
    macro_from_sheet.run()

    # if you have a MusicXML/MIDI file (perhaps after OCR) you can convert it
    # directly and then produce a macro.  this requires the ``music21`` package
    # and a file named ``example.musicxml`` in the working directory.
    try:
        xml_sheet = musicxml_to_sheet('Aria Math.mxl')
        print('\nmusicxml converted to sheet:', xml_sheet)
        xml_macro = sheet_to_macro(xml_sheet, keymap, bpm=120)
        print('macro from MusicXML:', xml_macro.events)
    except Exception as e:
        print('skipping MusicXML demo (', e, ')')


def main():
    """Command‑line entry point.

    If two file paths are given on the command line the script will read
    both recordings, merge them, and write the result to a file.  The
    optional third argument specifies the output path (default
    ``merged.txt``).  If no arguments are provided the built‑in demo runs.
    """

    import sys

    if len(sys.argv) >= 3:
        # explicit source files provided on the command line
        if sys.argv[1] == '--sheet':
            # sheet format: script.py --sheet sheet.txt keymap.txt bpm out.txt
            sheet_path = sys.argv[2]
            keymap_path = sys.argv[3]
            bpm = float(sys.argv[4])
            out = sys.argv[5] if len(sys.argv) >= 6 else 'merged.txt'
            # read keymap file: lines of ``KEY NOTE``.  invert while
            # reading so that we produce a note->key map the same way
            # :func:`parse_keybinds` would.
            km = {}
            with open(keymap_path, encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        km[parts[1]] = parts[0]
            sheet = parse_sheet_lines(open(sheet_path, encoding='utf-8'))
            macro_obj = sheet_to_macro(sheet, km, bpm)
            write_recording(out, macro_obj.events)
            print(f"wrote sheet-based macro to {out}")
        else:
            path1 = sys.argv[1]
            path2 = sys.argv[2]
            out = sys.argv[3] if len(sys.argv) >= 4 else 'merged.txt'
            m1 = Macro.from_file(path1)
            m2 = Macro.from_file(path2)
            merged = m1 + m2
            write_recording(out, merged.events)
            print(f"merged {path1} + {path2} -> {out}")
    else:
        # no arguments: if the files example1.txt/example2.txt are present
        # merge them automatically, otherwise fall back to the built-in demo
        default1 = 'example1.txt'
        default2 = 'example2.txt'
        if os.path.exists(default1) and os.path.exists(default2):
            print(f"found {default1} and {default2}, merging to merged.txt")
            m1 = Macro.from_file(default1)
            m2 = Macro.from_file(default2)
            merged = m1 + m2
            write_recording('merged.txt', merged.events)
            print('merged -> merged.txt')
        else:
            _demo()


if __name__ == '__main__':
    main()
