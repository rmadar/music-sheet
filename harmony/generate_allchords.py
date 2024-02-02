import sys
sys.path.append("../src")
import score_creator as sc
import harmony as ha

# Initialized the staff string
str_staff = ''

# Triads
for i, nature in enumerate(ha.possible_triads):
    C = ha.triad.build(ha.note('c'), nature)    
    str_staff += C.lilypond_str()+'1 \\bar ""'
str_staff += '\\break'

# Tetrads
for i, nature in enumerate(ha.possible_tetrads):
    C = ha.tetrad.build(ha.note('c'), nature)    
    str_staff += C.lilypond_str()+'1 \\bar ""'
    if i==6 : str_staff += '\\break'
str_staff += '\\break'
    
# Ninth chords
for i, nature in enumerate(ha.possible_ninth):
    C9 = ha.extended_chords.build(ha.note('c'), nature)    
    str_staff += C9.lilypond_str()+'1 \\bar ""'
    if i==5: str_staff += '\\break'


# Staff for chord names and for notes on treble key
staff_chords = sc.staff(str_staff, clef='chords', time=None, tempo=None)
staff_treble = sc.staff(str_staff, clef='treble', time=None, tempo=None)


# Create the score and the final sheet
score = sc.score([staff_chords, staff_treble])
sheet = sc.sheet(score, title='All Chords', composer='',
                 hide_BarNumber=True,
                 hide_TimeSignature=True)
sheet.save(fname=f'all_chords.ly')
