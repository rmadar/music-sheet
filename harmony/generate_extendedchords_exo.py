import sys
sys.path.append("../src")
import numpy as np
import score_creator as sc
import harmony as ha


# Get N random triads (fondamental = pitch + alteration, nature)
N = 200
fonds = ha.generate_random_piches(N)
possible_chords = ha.possible_ninth+ha.possible_eleventh+ha.possible_thirteenth
naturs = np.random.choice(a=possible_chords, size=N)

# Generate the chords
all_chords = [ha.extended_chords.build(f, n) for f, n in zip(fonds, naturs)]

# Loop over treble and bass clef
for clef in ['treble', 'bass']:        

    # Lower all notes from 1 octave for the bass clef
    chords = [c for c in all_chords]
    if clef=='bass':
        chords = [c.shift_octave(-2) for c in all_chords]

    # Create the lilypond string to be feed into a score
    chords_str = [chord.lilypond_str() for chord in chords]

    # Loop over the chords and build
    #  - staff string with notes but no chord names
    #  - staff string without note with chord names
    #  - switch every 5 chords and break the line
    str_staff_chords = ''
    str_staff_notes  = ''
    str_staff_chords_correc = ''
    str_staff_notes_correc  = ''
    n_per_line = 5
    for i, c_array in enumerate(np.array_split(chords_str, int(N/n_per_line))):
        if i%2 == 0 :
            str_staff_chords += ' 1 \\bar ""'.join(c_array)
            str_staff_chords += '\\break'
            str_staff_notes  += f'\\repeat unfold {c_array.size} ' + ' { \\bar "" s1 }'
        else:
            str_staff_notes  += ' 1 \\bar ""'.join(c_array)
            str_staff_notes  += '\\break'
            str_staff_chords += f'\\repeat unfold {c_array.size} ' + ' { \\bar "" s1 }'

        if i%2 == 0:
            # Find a way to put color
            str_staff_notes_correc  += '\override NoteHead.color = #red \override Accidental.color = #red ' + '1 \\bar ""'.join(c_array)
            str_staff_notes_correc  += '\\break'
            str_staff_chords_correc += '\override ChordName.color = #black ' + '1 \\bar ""'.join(c_array)
            str_staff_chords_correc += '\\break'
        else:
            str_staff_notes_correc  += '\override NoteHead.color = #black \override Accidental.color = #black ' + '1 \\bar ""'.join(c_array)
            str_staff_notes_correc  += '\\break'
            str_staff_chords_correc += '\override ChordName.color = #red ' + '1 \\bar ""'.join(c_array)
            str_staff_chords_correc += '\\break'


    # Create the two staffs
    staff_chords = sc.staff(str_staff_chords, clef='chords', time=None, tempo=None)
    staff_notes  = sc.staff(str_staff_notes , clef=clef    , time=None, tempo=None)
    
    # For the correction
    staff_chords_corr = sc.staff(str_staff_chords_correc, clef='chords', time=None, tempo=None)
    staff_notes_corr  = sc.staff(str_staff_notes_correc , clef=clef    , time=None, tempo=None)
    
    # Mettre cette portee dans une partition
    score = sc.score([staff_chords, staff_notes])
    score_corr = sc.score([staff_chords_corr, staff_notes_corr])
    
    # Creer le fichier final contenant cette partition
    sheet = sc.sheet(score, title='Extended Chords', composer='',
                     hide_BarNumber=True,
                     hide_TimeSignature=True)
    
    # Creer le fichier final contenant cette partition
    sheet_corr = sc.sheet(score_corr, title='Extended Chords - CORRECTION', composer='',
                          hide_BarNumber=True,
                          hide_TimeSignature=True)

    # Save it
    sheet.save(fname=f'extendedchords_exercies_{clef}-clef.ly')
    sheet_corr.save(fname=f'extendedchords_exercies_{clef}-clef_CORRECTION.ly')
