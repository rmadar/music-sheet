import sys
sys.path.append("../src")
import score_creator as sc
import harmony as ha


# Write C major chords
chords_Cmajor = [
    ha.triad(ha.note('c'), ha.note('e'), ha.note('g')), 
    ha.triad(ha.note('d'), ha.note('f'), ha.note('a')), 
    ha.triad(ha.note('e'), ha.note('g'), ha.note('b')), 
    ha.triad(ha.note('f'), ha.note('a'), ha.note('c', octave=6)), 
    ha.triad(ha.note('g'), ha.note('b'), ha.note('d', octave=6)), 
    ha.triad(ha.note('a'), ha.note('c', octave=6), ha.note('e', octave=6)), 
    ha.triad(ha.note('b'), ha.note('d', octave=6), ha.note('f', octave=6)), 
]

#  Create the lilypond string to be feed into a score
chords_str   = [chord.lilypond_str() for chord in chords_Cmajor]
staff_str_chords = '\\repeat unfold 7 { s1 } \\break ' + '1 \\bar "" '.join(chords_str)
staff_str_notes  = 'c\' \\bar "" d\' \\bar "" e\' \\bar "" f\' \\bar "" g\' \\bar "" a\' \\bar "" b\' '
staff_str_notes += '1 \\bar "" '.join(chords_str)

# Creer une portee a partir de ces notes
staff_chords = sc.staff(staff_str_chords, clef='chords', time=None, tempo=None)
staff_notes  = sc.staff(staff_str_notes , clef='treble', time=None, tempo=None)

# \repeat unfold 8 { s1 }

# Mettre cette portee dans une partition
score = sc.score([staff_chords, staff_notes])


# Creer le fichier final contenant cette partition
sheet = sc.sheet(score, title='Gamme de Do Majeur', composer='',
                 hide_BarNumber=True,
                 hide_TimeSignature=True
                 )

# Save it
sheet.save(midi=False)
