from macro import musicxml_to_sheet, musicxml_to_macro, sheet_to_macro, parse_keybinds, format_recording, write_recording

sheet = musicxml_to_sheet('Aria Math.mxl')
# sheet now contains (offset, note, beats) triples
print('notes in score:', sorted(set(n for _,n,_ in sheet)))
print('count', len(sheet))

# paste the keybind mapping text here, exactly as you listed earlier
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
macro = sheet_to_macro(sheet, keymap, bpm=85)
write_recording('aria_converted.txt', macro.events)