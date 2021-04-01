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
          tagline  = "Generated with https://github.com/rmadar/music-sheet"
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
        


