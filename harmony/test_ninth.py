import sys
sys.path.append("../src")
import score_creator as sc
import harmony as ha


str_staff = ''
for nature in ha.possible_ninth:
    C9 = ha.extended_chords.build(ha.note('c'), nature)
    
    str_staff += C9.lilypond_str()+'1'

staff_chords = sc.staff(str_staff, clef='chords', time=None, tempo=None)
staff_treble = sc.staff(str_staff, clef='treble', time=None, tempo=None)
score = sc.score([staff_chords, staff_treble])
sheet = sc.sheet(score, title='Ninth Chords', composer='',
                 hide_BarNumber=True,
                 hide_TimeSignature=True)
sheet.save(fname=f'test_ninth_chords.ly')
