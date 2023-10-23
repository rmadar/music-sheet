import harmony as ha

# Short cuts
n = ha.note
chord = ha.tetrad

# Defning chords
C   = chord(n('c'), n('e'), n('g'), n('b'))
D   = chord(n('d'), n('f'), n('a', 'b'), n('c', octave=6))
Fm1 = chord(n('f'), n('a', 'b'), n('c', octave=6), n('e', 'b', octave=6))
Fm2 = chord.build(n('f'), 'min_7')

FdimTriad = ha.triad(n('f'), n('a', 'b'), n('c', 'b', octave=6))
Fdim = chord.build_from_triad(FdimTriad, n('e','bb', octave=6) ) 

# Printing their names
print(C, D, Fm1, Fm2, Fdim)
print(C.lilypond_str(), D.lilypond_str(), Fm1.lilypond_str(),
      Fm2.lilypond_str(), Fdim.lilypond_str())
