import sys
sys.path.append("../src")
import numpy as np
import score_creator as sc

def get_random_note(note_collection):
    return note_collection[np.random.randint(low=0, high=len(note_collection))]

# Pattern rythmique simples bases sur des noires et des croches.
rythm_simple = [

    # 0 note
    ['r4'],

    # 1 noire
    ['4'],

    # 1 croche
    #['8'  , 'r8'],
    ['r8' , '8' ],

    # 2 croches
    ['8', '8'],
]

# Notes simples
notes_simple = ['d', 'f']#, 'a']

# Get random rythm sentences
nSentences, nBars, iMin, iMax = 20, 8, 0, len(rythm_simple)
i_rythm = np.random.randint(low=iMin, high=iMax, size=(nSentences, 4*nBars))

# Create the sheet
sheet = sc.sheet(title='Exercices de lecture')

# Loop over all sentences
for i, Rs in enumerate(i_rythm):

    sentence = ''
    
    # Loop over notes and rythm in the sentence
    for r in Rs:
        rythms = rythm_simple[r]
        for rythm in rythms:
            note = ''
            if 'r' not in rythm:
                note = get_random_note(notes_simple)
            sentence += '{}{} '.format(note, rythm)

    score = sc.score([sc.staff(sentence, tempo='4=50')], title='Exercice {}'.format(i+1))
    sheet.add_score(score)

# Save it
sheet.save(fname='lecture.pdf', midi=False)
