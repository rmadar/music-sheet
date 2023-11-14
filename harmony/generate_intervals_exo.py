import sys
sys.path.append("../src")
import numpy as np
import score_creator as sc
import harmony as ha


# Get N random triads (fondamental = pitch + alteration, nature)
N = 200
fonds = ha.generate_random_piches(N)
inter = np.random.choice(a=ha.possible_intervals, size=N)
all_inter = [ha.interval.build(f, i) for (f, i) in zip(fonds, inter)]

# Loop over treble and bass clef
for clef in ['treble', 'bass']:        

    # Lower all notes from 1 octave for the bass clef
    intervals = [i for i in all_inter]    
    if clef=='bass':
        intervals = [i.shift_octave(-2) for i in all_inter]

    # Create the lilypond string to be feed into a score
    intervals_str = [i.lilypond_str() for i in intervals]

    # Loop over the chords and build
    #  - staff string with notes but no chord names
    #  - staff string without note with chord names
    #  - switch every 5 chords and break the line
    str_staff_intervals  = ''
    str_staff_corr  = ''
    for i, c_array in enumerate(np.array_split(intervals, int(N/6))):
        if i%2 == 0:
            str_staff_intervals += '\n\\undo \\hide NoteHead \\undo \\hide Accidental \\override NoteHead.no-ledgers = ##f '
            str_staff_intervals += ' '.join([s.lilypond_str() for s in c_array])
            str_staff_intervals += ' \\break\n '

            str_staff_corr += '\override NoteHead.color = #black \override Accidental.color = #black '
            str_staff_corr += ' '.join([s.lilypond_str(with_name=True, name_color='red') for s in c_array])
            str_staff_corr +=  ' \\break\n '
        
        else :
            str_staff_intervals += '\n\\hide NoteHead \\hide Accidental \\override NoteHead.no-ledgers = ##t '
            str_staff_intervals += ' '.join([s.lilypond_str(with_name=True) for s in c_array])
            str_staff_intervals += ' \\break\n '
            
            str_staff_corr += '\override NoteHead.color = #red \override Accidental.color = #red '
            str_staff_corr += ' '.join([s.lilypond_str(with_name=True) for s in c_array])
            str_staff_corr += ' \\break\n '


    # Create the 2 staffs
    staff_intervals = sc.staff(str_staff_intervals, clef=clef, time=None, tempo=None)
    staff_corr      = sc.staff(str_staff_corr     , clef=clef, time=None, tempo=None)    
    
    # Mettre cette portee dans une partition
    score = sc.score([staff_intervals])
    score_corr = sc.score([staff_corr])
    
    # Creer le fichier final contenant cette partition
    sheet = sc.sheet(score, title='Intervales', composer='',
                     hide_BarNumber=True,
                     hide_TimeSignature=True)
    
    # Creer le fichier final contenant cette partition
    sheet_corr = sc.sheet(score_corr, title='Intervales - CORRECTION', composer='',
                          hide_BarNumber=True,
                          hide_TimeSignature=True)

    # Save it
    sheet.save(fname=f'intervals_exercises_{clef}-clef.ly')
    sheet_corr.save(fname=f'intervals_exercises_{clef}-clef_CORRECTION.ly')
