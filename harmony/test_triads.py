import harmony as ha

# Short cuts
n = ha.note
chord = ha.triad

# Defning chords
C  = chord(n('c'), n('e'), n('g'))
D  = chord(n('d'), n('f'), n('a', 'b'))
Fm = chord.build(n('f'), 'minor') 

# Printing their names
print(C, D, Fm)
print(C.lilypond_str(), D.lilypond_str(), Fm.lilypond_str())
