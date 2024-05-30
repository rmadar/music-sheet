import sys
sys.path.append("../src")
import score_creator as sc
import harmony as ha

# Create the staff string
str_staff = ''
for i, nature in enumerate(ha.possible_thirteenth):
    print(nature)
    C9 = ha.extended_chords.build(ha.note('c'), nature)    
    str_staff += C9.lilypond_str()+'1 \\bar ""'
    if i==5: str_staff += '\\break'


# Staff for chord names and for notes on treble key
staff_chords = sc.staff(str_staff, clef='chords', time=None, tempo=None)
staff_treble = sc.staff(str_staff, clef='treble', time=None, tempo=None)


# Create the score and the final sheet
score = sc.score([staff_chords, staff_treble])
sheet = sc.sheet(score, title='Thirteenth Chords', composer='',
                 hide_BarNumber=True,
                 hide_TimeSignature=True)
sheet.save(fname=f'test_thirteenth_chords.ly')
