import sys
sys.path.append("../src")
import numpy as np
import score_creator as sc

# Store all possibilities from 16-th notes
pattern = {

    # 1 note
    '1 note - A': ['4'                         ],
    '1 note - B': ['r16', '16'  , 'r16', 'r16' ],
    '1 note - C': ['r8' , '8'                  ],
    '1 note - D': ['r16', 'r16' , 'r16', '16'  ],

    # 2 notes
    '2 notes - A ': ['r8' , '16' , '16'        ],
    '2 notes - B1': ['16' , '16' , 'r8'        ],
    '2 notes - B2': ['16' , '8.'               ],
    '2 notes - B3': ['16' , '8'  , 'r16'       ],
    '2 notes - C1': ['r16', '16' , '16' , 'r16'],
    '2 notes - C2': ['r16', '16' , '8'  ,      ],
    '2 notes - D ': ['8'  , '8'                ],
    '2 notes - E1': ['16' , 'r8' , '16'        ],
    '2 notes - E2': ['8'  , 'r16', '16'        ],
    '2 notes - E3': ['8.' , '16'               ],
    '2 notes - F1': ['r16', '16' , 'r16', '16' ],
    '2 notes - F2': ['r16', '8'  , '16'        ],

    # 3 notes
    '3 notes - A1': ['16' , '16' , '16' , 'r16'],
    '3 notes - A2': ['16' , '16' , '8'         ],
    '3 notes - B1': ['16' , 'r16', '16' , '16' ],
    '3 notes - B2': ['8'  , '16' , '16'        ],
    '3 notes - C1': ['16' , '16' , 'r16', '16' ],
    '3 notes - C2': ['16' , '8'  , '16'        ],
    '3 notes - D' : ['r16', '16' , '16' , '16' ],
    
    # 4 notes
    '4 notes' : ['16' , '16', '16', '16'],
}


# Starting point to perform combinations
readable_pattern = [

    # 1 note
    ['4'               ],
    ['8'  , 'r8'       ],
    ['r8' , '8'        ],
    ['r16', '8.'       ],
    ['r8' , 'r16', '16'],

    # 2 notes
    ['8.' , '16'],
    ['r16', '16' , '8'],
    ['16' , '8.'],
    ['r8' , '16' , '16'],
    ['r16', '8'  , '16'],
    ['16' , '16' , '16' , 'r16'],
    ['16' , '16' , '8'         ],
    ['8'  , '16' , '16'        ],
    ['16' , '8'  , '16'        ],
    ['r16', '16' , '16' , '16' ],
    
    # 4 notes
    ['16' , '16', '16', '16'],    
]

# Helper function
def score(note_list, title=''):
    '''
    note_list: list of string, following the lilypond notation.
    title    : title of the score
    return a score object.
    '''
    notes = ' '.join(note_list)
    staff = sc.staff(notes, clef='drum')
    return sc.score([staff], title=title)


#  ---------------------
#  ALL POSSIBLE PATTERNS
#  ---------------------

# Create a sheet that will contain all patterns
sheet = sc.sheet(title='Rythmic Patterns From 16th Notes')
for k, v in pattern.items():
    n  = [*v, 'r4', *v, 'r4'] * 2
    n += ['\\break']
    n += [*v, *v, 'r4', 'r4']
    n += [*v, *v, *v, 'r4' ]
    sheet.add_score(score(n, title='Pattern with {}'.format(k)))

# Save it
sheet.save(midi=False)


#  -----------------
#  TWO-WORDS PHRASES
#  -----------------

# Get a random list of N pair of random patterns
N, iMin, iMax = 20, 0, len(readable_pattern)
indices = np.random.randint(low=iMin, high=iMax, size=(20, 2))
notes = []
for index in indices:
    i1, i2 = index[0], index[1]
    w1, w2 = readable_pattern[i1], readable_pattern[i2] 
    n  = [*w1, *w2, 'r2'] * 2
    n += ['\\break']
    n += [*w1, *w2, *w1, *w2] * 2
    notes.append(n)

# Create the sheet
sheet = sc.sheet(title='Two-words Phrases From 16th-note Patterns')
for i, n in enumerate(notes):
    sheet.add_score(score(n, title='Phrase {}'.format(i)))

# Save it
sheet.save(midi=False)

