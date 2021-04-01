import os
import numpy as np
from numpy import random as rnd

class sheet:

    def __init__(self, score='', title=''):

        self.body = ''
        self.preamble = r'''
    
        \version "2.22.0"
        
        #(set-global-staff-size 20)
        
        \header {
        '''
        if title:
            self.preamble += 'title = "{}"'.format(title)

        self.preamble += '''
          subtitle = " "
          composer = "Romain Madar"
          arranger = " "
          tagline  = ""
        }
        
        \layout {
          indent = 0\cm
          \context {
           \Score
           \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/16)
          }
        }
        
        \paper {
          top-margin = 20
          bottom-margin = 20
          left-margin = 15
          right-margin = 15
          system-system-spacing.basic-distance = #15
          score-markup-spacing.basic-distance  = #25
          score-system-spacing.basic-distance  = #25
        }
        '''

        if score:
            self.add_score(score)
        
        return 
    
    def add_score(self, score):
        self.body += score.body

    def lylipond_file(self, fname):
        f = open(fname, 'w')
        f.write(self.preamble)
        f.write(self.body)
        f.close()
        
    def save(self, fname='sheet.ly', midi=True):
        self.lylipond_file(fname)
        os.system("lilypond {}".format(fname))
        if midi:
            name_base = fname.replace(".ly", "")
            os.system("rm -f {}.mp3".format(name_base))
            cmd = "timidity {}.midi -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k {}.mp3"
            os.system(cmd.format(name_base, name_base))


class score:
    def __init__(self, staffs, title=''):
        self.body = '\\score {\n'
        for s in staffs:
            self.body += s.body

        if title:
            self.body += '\\header {'
            self.body += 'piece = "{}"'.format(title)
            self.body +='}'

        self.body += '''
        \layout { }
        \midi {
        }
        }
        '''
        

class staff:
    
    def __init__(self, notes, clef='bass', time='4/4',
                 tempo='4=90', midi=None):
        '''
        Arguments:
        ----------
          - 'notes' [string]: music following lylipond notation.
          - 'clef'  [string]: clef for this staff (drum will create a 'DrumStaff')
          - 'time'  [string]: time signature of the staff (e.g. 4/4)
          - 'tempo' [string]: tempo for the staff (e.g. 4=90)
          - 'midi'  [string]: midi instrument 
        '''

        self.clef  = clef
        self.time  = time
        self.tempo = tempo
        self.midi  = midi
        
        txt = '\t\\new Staff'
        if clef.lower() == 'drum':
            txt = '\t\\new DrumStaff'
        txt += ''' 
        \t{
        \t\t
        \\numericTimeSignature
        '''
        if clef.lower() != 'drum':
            txt += '\t\t \\clef {}\n'.format(self.clef)
        txt += '\t\t \\time {}\n'.format(self.time)
        txt += '\t\t \\tempo {}\n'.format(self.tempo)
        if midi:
            txt += '\t\t \\set Staff.midiInstrument = #"{}"\n'.format(self.midi)
        txt += '''
        \\override Score.BarNumber.break-visibility = ##(#t #t #t)
        \t\t{
        \t\t\t
        '''
        txt += notes
        txt += '''
        \t\t}
        \t}
        '''
        self.body = txt
        


# Dictionnaire key=nombre de temps, value=code dans lilypond
durees = {
    4   : '1'  , # ronde
    2   : '2'  , # blanche
    3   : '2.' , # blanche pointee
    1   : '4'  , # noire
    1.50: '4.' , # noire pointee
    0.50: '8'  , # croche
    0.75: '8.' , # croche pointee
    0.25: '16' , # double-croche
}

notes = [
    'e,' ,
    'f,' ,
    'g,' ,
    'a,' , # la
    'b,' , # si
    'c'  , # do
    'd'  , # re
    'e'  , # mi
    'f'  , # fa
    'g'  , # sol
    'a'  , # la
    'b'  , # si
    'c\'',
    'd\'',
    'e\'', 
    'f\'', 
    'g\'', 
    'a\'', 
    'b\'',
]

# Store all possibilities from 16-th notes
rythm_pattern_16th = {

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

# Genere un temps
def un_temps(nNoteMax=4, noirePointee=True, triolet=False, sextuplet=False):
    '''
    Cette function retourne le placement rythmique d'un temps, selon
    le nombre de notes aleatoire jouees dans ce temps. Ici, un silence
    est consideree comme une "note". Le niveau de difficulte peut etre 
    parametrise, avec le nombre max de note par temps (4, double-croche),
    la presence de noire pointee ou de triolets (TODO), ou de sextuplets (TODO).

    Return:
    -------
      * liste de durees dont la somme fait 1. La taille de cette list
        depend de la segmentation du temps.

    Arguments:
    ----------
      * nNoteMax      [int]: nombre maximum de notes par temps 
      * noirePointee [bool]: inclure ou non des pattern avec 
                             noires pointees + double-croche.
      * triolet      [bool]: inclure des triolets   TO-DO
      * sextuplet    [bool]: inclure des sextuplets TO-DO
    '''

    if nNoteMax>4:
        raise NameError("Cant play more than four note")
    
    # Number of "notes" between 1 and 4
    nNotes = np.random.randint(low=1, high=nNoteMax+1)
    
    # Container for the result, valant une noire par defaut
    tps = [durees[1]]

    # Quatre notes dans le tps, necessairement 4 double-croches
    if nNotes == 4 :
        tps = [durees[0.25]]*4
        
    # Trois notes: 1 croche + 2 double
    if nNotes == 3 :
        x = rnd.random()
        if x < 0.33:
            tps = [durees[0.25], durees[0.25], durees[0.50]]
        elif x < 0.66:
            tps = [durees[0.25], durees[0.50], durees[0.25]]
        else:
            tps = [durees[0.50], durees[0.25], durees[0.25]]
            
    # Deux notes: deux croches ou une croche pointee + double-croche
    if nNotes == 2:
        
        # Deux croches
        tps = [durees[0.50], durees[0.50]]

        # croche pointee + double-croche
        if noirePointee and rnd.random() < 0.5:
            if rnd.random() < 0.5:
                tps = [durees[0.25], durees[0.75]]
            else:
                tps = [durees[0.75], durees[0.25]]
        
    # Deux double croches: 
    if nNotes == 1:
        tps = [durees[1]]

    # Return the result
    return tps

