import os
import numpy as np
from numpy import random as rnd

############# TO DO ################
# - add few user parameters: double croche fracion, silence fraction, etc ...
# - remove unatural pattern coming from silence, such as "double-croche + soupire pointee",
#   which would be a stacato noire.
# ###################################

class sheet:

    def __init__(self, score=''):

        self.body = ''
        self.preamble = r'''
    
        \version "2.22.0"
        
        #(set-global-staff-size 20)
        
        \header {
        title = "Exercice de Lecture Clé de Fa"
        subtitle = " "
        composer = "Romain Madar"
        arranger = " "
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
        }
        '''

        if score:
            self.add_score(score)
        
        return 
    
    def add_score(self, score):
        self.body += score.body

    def lylipond_file(self, fname):
        f = open(fname, 'w')
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
    def __init__(self, staffs):
        self.body = '\\score {\n'
        for s in staffs:
            self.body += s.body
        self.body += '''
        \layout { }
        \midi {
        }
        }
        '''

class staff:
    
    def __init__(self, notes):
        '''
        Notes is a string following lylipond notation.
        '''

        self.clef  = 'bass'
        self.time  = '4/4'
        self.tempo = '4 = 90'
        self.midi  = 'electric bass (finger)'
        
        txt = '''
        \t\\new Staff
        \t{
        \t\t
        \\numericTimeSignature
        '''
        txt += '\t\t \\clef {}\n'.format(self.clef)
        txt += '\t\t \\time {}\n'.format(self.time)
        txt += '\t\t \\tempo {}\n'.format(self.tempo)
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

    Arguements:
    -----------
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

