import numpy as np
import copy

# Accepted pitch
possible_pitchs = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
tons_steps = [1, 1, 0.5, 1, 1, 1, 0.5]
N_pitch = len(possible_pitchs)

# Accepted alterations
alteration_values = {
    'b' : -0.5,
    '#' : +0.5,
    'bb': -1.0,
    '##': +1.0,
    'natural': 0,
}
possible_alterations = [k for k in alteration_values.keys()]

# Interval values (ton)
interval_values = {
    'un' :    0,
    '2m' :  0.5,
    '2M' :    1,
    '2+' :  1.5,
    '3m' :  1.5,
    '3M' :    2,
    '4J' :  2.5,
    '4+' :    3,
    '5-' :    3,
    '5J' :  3.5,
    '5+' :    4,
    '6m' :    4,
    '6M' :  4.5,
    '7-' :  4.5,
    '7m' :    5,
    '7M' :  5.5,
    '8J' :    6,
    '9m' :  6.5,
    '9M' :  7.0,
    '9+' :  7.5,
    '11-':  8.0,
    '11J':  8.5,
    '11+':  9.0,
    '13m': 10.0,
    '13M': 10.5,
}

possible_intervals = [k for k in interval_values.keys()]

# Triade/tetrads names
possible_triads   = ['maj', 'min', 'aug', 'dim', 'sus2', 'sus4']
possible_tetrads  = ['maj_7', 'maj_maj7', 'min_7' , 'min_maj7', 'sus4_7' ]
possible_tetrads += ['aug_7', 'aug_maj7', 'ddim_7', 'dim_7', 'dim_maj7'  ]
possible_tetrads += ['maj_6', 'min_6'   , 'min_min6']

# Ninth chords
possible_ninth  = ['maj_add9', 'maj_maj9', 'maj_69' ]
possible_ninth += ['maj_9'   , 'maj_7b9' , 'maj_7d9']
possible_ninth += ['min_9'   , 'ddmin_9' , 'min_maj9', 'min_69']
possible_ninth += ['sus4_9'  , 'sus4_b9' ]

# Eleventh chords
possible_eleventh  = ['maj_maj7_d11', 'maj_maj9_d11']
possible_eleventh += ['maj_7_d11', 'maj_9_d11', 'maj_7_b9_d11', 'maj_7_d9_d11' ]
possible_eleventh += ['min_7_add11', 'min_11', 'ddmin_11' ]

# Thirteenth chords
possible_thirteenth  = ['maj_maj7_add13', 'maj_maj13', 'maj_maj13_d11']
possible_thirteenth += ['maj_7_add13', 'maj_13', 'maj_13_b9', 'maj_13_d9', 'maj_7_b13_d9', 'maj_7_b13_b9' ]
possible_thirteenth += ['min_7_add13', 'min_13']
possible_thirteenth += ['sus4_13', 'sus4_9_b13', 'sus4_7_b9_b13']


# Scale/modes names
nice_scales_names = {
    'major'         : 'Major',
    'minor_natural' : 'Natural Minor' ,
    'minor_harmonic': 'Harmonic Minor',
    'minor_melodic' : 'Melodic Minor' ,
    'major_penta'   : 'Pentatonic Major',
    'minor_penta'   : 'Pentatonic Minor',
    'major_blues'   : 'Blues Major',
    'minor_blues'   : 'Blues Minor',
    'ionian'        : 'Ionian (I) Mode',
    'dorian'        : 'Dorian (II) Mode',
    'phrygian'      : 'Phyrigian (III) Mode',
    'lydian'        : 'Lydian (IV) Mode',
    'myxolidian'    : 'Myxolidian (V) Mode',
    'eolian'        : 'Eolian (VI) Mode',
    'lorcian'       : 'Locrian (VI) Mode',
}
possible_scales = [k for k in nice_scales_names.keys()]

# Scales/modes composition
scales_intervals = {
    'major'         : ['un', '2M', '3M', '4J', '5J', '6M', '7M'],
    'minor_natural' : ['un', '2M', '3m', '4J', '5J', '6m', '7m'],
    'minor_harmonic': ['un', '2M', '3m', '4J', '5J', '6m', '7M'],
    'minor_melodic' : ['un', '2M', '3m', '4J', '5J', '6M', '7M'],
    'major_penta'   : ['un', '2M', '3M', '5J', '6M'],
    'minor_penta'   : ['un', '3m', '4J', '5J', '7m'],
    'major_blues'   : ['un', '2M', '2+', '3M', '5J', '6M'],
    'minor_blues'   : ['un', '3m', '4J', '4+', '5J', '7m'],
    'ionian'        : ['un', '2M', '3M', '4J', '5J', '6M', '7M'],
    'dorian'        : ['un', '2M', '3m', '4J', '5J', '6M', '7m'],
    'phrygian'      : ['un', '2m', '3m', '4J', '5J', '6M', '7m'],
    'lydian'        : ['un', '2M', '3M', '4+', '5J', '6M', '7M'],
    'myxolidian'    : ['un', '2M', '3M', '4J', '5J', '6M', '7m'],
    'eolian'        : ['un', '2M', '3m', '4J', '5J', '6m', '7m'],
    'lorcian'       : ['un', '2m', '3m', '4J', '5-', '6m', '7m' ],
}


# Generating randoms note removing Si#/Cb and Mi#/Fab
def generate_random_piches(N, w_fonds=[1]*7, w_alter=[1, 1, 1]):
    '''
    Generate random pitches (both note+alteration),
    removing Si# (Do), Dob (Si), Mi# (Fa) and Fab (Mi).
     - w_fonds = weights for each note (7 elements)
     - w_alter = weights for each alteration (3 elements = natural, #, b)
    '''

    # Convert the weight into numpy array
    w_fonds = np.array( w_fonds )
    w_alter = np.array( w_alter )
    
    # Fondmantals
    w_fonds = w_fonds / w_fonds.sum()
    fonds = np.random.choice(a=possible_pitchs, size=N*10, p=w_fonds)

    # Alterations
    w_alter = w_alter / w_alter.sum()
    alters = np.random.choice(a=['natural', '#' , 'b' ], size=N*10, p=w_alter)

    # Notes
    notes = []
    for i, (f, a) in enumerate(zip(fonds, alters)):

        # note
        n = note(f, a)

        # Removing E#, Fb, Cb and B#
        if n.is_Esharp() or n.is_Fflat() or n.is_Cflat() or n.is_Bsharp():
            continue
        else: 
            notes.append(n)
            
        if len(notes)==N:
            break
            
    # Checking the array has the proper wanted size
    # after filtering
    if len(notes) != N:
        raise NameError('harmony::generate_random_piches():: Not enough generated pitches')
        
    # Return the result
    return notes


class note:

    # Constructor of the note
    def __init__(self, pitch, alteration='natural', octave=5):

        '''
        pitch      [string]: do re mi fa sol la si (international notation)
        alteration [string]: natural, b, #, bb, ## (default = 'natural')
        octave     [int]   : octave of the pitch (default 5: middle octave on piano)
        '''
        
        if pitch not in possible_pitchs:
            raise NameError(f'{pitch} is not supported, only {possible_pitchs} are.')

        if alteration not in possible_alterations:
            raise NameError(f'{alteration} is not supported, only {possible_alterations} are.')

        self.pitch = pitch
        self.alteration = alteration
        self.octave = octave


    # Overloading string conversion
    def __str__(self):
        octave_str = ''
        if self.octave>4:
            octave_str = '\'' * (self.octave - 4)
        if self.octave<4:
            octave_str = ',' * (4 - self.octave)
        if self.alteration=='natural':
            return f'{self.pitch}{octave_str}'
        else:
            return f'{self.pitch}{octave_str}{self.alteration}'

    # Get a string usable for lilypond    
    def lilypond_str(self):
        '''
        String suited for lilypond
        '''

        # Alteration
        alt = ''
        if self.alteration == '#' : alt = 'is'
        if self.alteration == 'b' : alt = 'es'
        if self.alteration == '##': alt = 'isis'
        if self.alteration == 'bb': alt = 'eses'

        # Octave
        octave = ''
        if self.octave>4: octave = '\'' * (self.octave - 4)
        if self.octave<4: octave = ','  * (4 - self.octave)

        # Return the result
        return f'{self.pitch}{alt}{octave}'


    def is_Esharp(self):
        return ('e' in self.pitch) and self.alteration=='#'

    def is_Fflat(self):
        return ('f' in self.pitch) and self.alteration=='b'

    def is_Bsharp(self):
        return ('b' in self.pitch) and self.alteration=='#'
    
    def is_Cflat(self):
        return ('c' in self.pitch) and self.alteration=='b'

    # Change the octave of the note
    def shift_octave(self, i):
        '''
        Shift the note from i octave (positive or negative integer)
        '''
        return note(self.pitch, self.alteration, self.octave+i)
    

    # Compute the absolute distance (in tone) wrt the first C on a piano
    def absolute_tons(self):
        '''
        Return the absolute number of tons with respect
        to the first C of a piano
        '''
        i = possible_pitchs.index(self.pitch)
        rel_ton = sum(tons_steps[:i])  + alteration_values[self.alteration]
        return self.octave * 6 + rel_ton


    # Compute the difference (in tons) between self and other
    def diff(self, other):
        '''
        Return the number of tons between the object and
        the note 'other'.

        e.g. to get the number of ton between la# and c:
        >>> la = ha.note('la', '#')
        >>> do = ha.note('c', octave=5)
        >>> ntons = la.diff(do) 
        '''
        return self.absolute_tons() - other.absolute_tons()
        
        
    # Get the pitch corresponding to an interval
    def note_of(self, interval, descending=False):

        '''
        Return the note correponding to a given interval of
        the current note.

        e.g. to get the 3m of a LA:
        >>> la = ha.note('la')
        >>> 3rdm = la.note_of('3m') 
        '''

        # Check that the interval is supported
        if interval not in possible_intervals:
            NameError(f'{interval} is not supported, only {possible_intervals} are.')

        # If unisson return the same note
        if interval == 'un':
            return self

        # If octave return the same note shifted by 1 octave
        if interval == '8J':
            return self.shift_octave(+1)

                
        # Number of notes to be incremented (eg. 1 for a second)
        # quality = diminished, just, augemented, major, minor
        if len(interval) == 2:
            index_to_add = int(interval[0])-1
            quality = interval[1]
        elif len(interval) == 3:
            index_to_add = int(interval[0:2])-1
            quality = interval[2]
        else:
            txt  = 'note_of()::ERROR "interval" neither 2 or 3 caracters while'
            txt += '                 it should of 2 (e.g. "7M") or 3 (e.g. "11+")'
            raise NameError(txt)
        
            
        # get the index of the current note
        index = possible_pitchs.index(self.pitch)

        # Getting the new pitch name
        new_pitch, new_octave  = '', self.octave

        # In case of ascending interval
        if not descending:
            new_index = index + index_to_add
            if new_index < N_pitch  :
                new_pitch = possible_pitchs[new_index]
            elif new_index < 2*N_pitch: # If the note is one octave higher (e.g. 11th of C' would be F'')
                new_pitch = possible_pitchs[new_index-N_pitch]
                new_octave = self.octave + 1
            elif new_index < 3*N_pitch: # If the note is two octaves higher (e.g. 11th of G' would be E''')
                new_pitch = possible_pitchs[new_index-2*N_pitch]
                new_octave = self.octave + 2
            else:
                txt  = f'\nNote::note_of():: Cannot be more than two octaves, while\n'
                txt += f'                    it seems to be the case for the {interval} of {self}.'
                raise NameError()
                
        # In case of descending interval
        else:
            new_index = index - index_to_add
            if new_index > 0:
                new_pitch = possible_pitchs[new_index]
            else:
                new_pitch = possible_pitchs[N_pitch+new_index]
                new_octave = self.octave - 1

        # Determining the alteration
        x = note(new_pitch, 'natural', new_octave)
        res = x
        nt_target = interval_values[interval]
        if not descending:
            ntons = x.diff(self)
            if ntons == nt_target:
                res = x
            elif ntons == nt_target + 0.5:
                res = note(new_pitch, 'b' , new_octave)
            elif ntons == nt_target + 1:
                res = note(new_pitch, 'bb', new_octave)
            elif ntons == nt_target - 0.5:
                res = note(new_pitch, '#' , new_octave)
            elif ntons == nt_target - 1:
                res = note(new_pitch, '##', new_octave)
            else:
                txt  = f'\nNote::note_of()::Trying to determine the {interval} of {self}.\n'
                txt += f'                 The ton difference between {self} and the target {x}\n'
                txt += f'                 leads to Delta={ntons-nt_target}, which not correct.\n'
                txt += f'                 Only [+/- 0.5, +/- 1.0] are supported.\n'
                raise NameError(txt)

        # Descending interval
        else:
            print('This part of the function "note_of()" is not written yet.')
        

        # Return the result
        return res


###############
##  2 NOTES  ##
###############

class interval:

    def __init__(self, n1, n2):
        '''
        Construct an interval of two notes.
        '''
        self.n1 = n1
        self.n2 = n2
        self.notes_list = [n1, n2]

    def n_tons(self):
        return self.n2.diff(self.n1)

    def name(self):

        '''
        Return the name of the interval (e.g. 2m, 3M, etc ...).
        If the first note is higher than the second, the note
        are reversed (the interval is considered as descending).

        In 2 cases the result 'N.A.' is returned:
          1. If the two notes have the same name (e.g. E and Eb), 
          2. if the lower note is E#, Fb, B# or Cb
        
        In both cases, it has no sense harmonically:
          1. it would be the anharmony of proper interval (e.g. E Db, a 2m)
          2. those notes the anharmony of F, E, C and B and can only appear 
             as a second note
        '''
        
        # Unisson
        if self.n_tons() == 0:
            return 'un'

        if self.n_tons() == 6:
            return '8J'
        
        if self.n1.pitch == self.n2.pitch:
            return 'N.A.'
        
        # Second note lower than the first one, simply reverse it
        interval_tmp = self
        descending = False
        if self.n_tons() < 0:
            interval_tmp = interval(self.n2, self.n1)
            descending = True

        # if the lower note is E#, Fb, Cb ro B#, return unknown
        lown = interval_tmp.n1
        if lown.is_Esharp() or lown.is_Bsharp() or lown.is_Fflat() or lown.is_Cflat():
            return 'N.A.'
        
        # Get the number of notes between n1 and n2 (w/o # and b)
        i1 = possible_pitchs.index(interval_tmp.n1.pitch)
        i2 = possible_pitchs.index(interval_tmp.n2.pitch)
        
        # Get all the possible interval candidates (without all qualifications)
        inter = i2-i1+1
        if i2 < i1:
            inter = (i2+7) - i1 + 1
        interval_candidates = {k:v for k, v in interval_values.items() if str(inter) in k}
        if len(interval_candidates) == 0:
            txt  = f'INTERVAL::Name():: interval_candidates has a size of 0 for '
            txt += f'(n1, n2)=({interval_tmp.n1}, {interval_tmp.n2}), inter={inter}'
            print(txt)
            raise NameError('INTERVAL::Name():: No interval candidates were found')

        
        # Check which qualification ?
        for int_name in interval_candidates.keys():
            n2_tmp = interval_tmp.n1.note_of(int_name)
            if n2_tmp.diff(interval_tmp.n1) == interval_tmp.n_tons():
                if descending:
                    return 'desc' + int_name
                else:
                    return int_name
        txt  = 'INTERVAL::Name():: Interval name was not found.'
        txt += 'Check if ther is not an {E#, Fb, B#, Cb} as lower note.'         
        raise NameError(txt)
    
    def __str__(self):
        return f'"{self.n1} {self.n2}"'

    def lilypond_str(self, with_name=False, name_color='black'):
        '''
        When with_name is True, it adds the name of the scale
        on top of the first note. 'name_color' allows to change
        the color of the text.
        '''
        if with_name:
            name = self.name().replace('b', '"\\flat"').replace('#', '"\\sharp"')
            txt  = f'^\\markup{{ \\with-color "{name_color}" \\concat{{"{name}"}} }}'
            return f'< {self.n1.lilypond_str()} {self.n2.lilypond_str()} >1' + txt
        else:
            return f'< {self.n1.lilypond_str()} {self.n2.lilypond_str()} >1'
        
    def shift_octave(self, i):
        return interval(self.n1.shift_octave(i), self.n2.shift_octave(i))
    
    @classmethod
    def build(self, fond, nature):
        if nature in possible_intervals:
            return interval(fond, fond.note_of(nature))
        else:
            raise NameError(f'ERROR: interval {nature} is not supported. Only {possible_intervals} are.')
    

###############
##  3 NOTES  ##
###############
    
class triad:

    # Constructor from 3 notes
    def __init__(self, n1, n2, n3):

        '''
        Return a 3-notes (n1, n2, n3) chords.
        '''
        
        # Filling the 3 notes
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.notes_list = [n1, n2, n3]
        
        # Chord nature all initialized at False
        self.minor = False
        self.major = False
        self.aug   = False
        self.dim   = False
        self.sus2  = False
        self.sus4  = False

        # Getting the two intervales values
        a = n2.diff(n1)
        b = n3.diff(n2)

        # What is the nature of the chord ?
        # Major
        if (a==2 and b==1.5):
            self.major = True
        # Augmented
        elif (a==2 and b==2):
            self.aug  = True
        # Minor
        elif (a==1.5 and b==2):
            self.minor = True
        # Dimished
        elif (a==1.5 and b==1.5):
            self.dim  = True
        # Suspended by the 2nd
        elif (a==1 and b==2.5):
            self.sus2  = True
        # Suspended by the 4th
        elif (a==2.5 and b==1.0):
            self.sus4  = True
        else:
            txt = f'These 2 intervals {a} and {b} is not major/minor/augemented/dimished/sus2/sus4'
            raise NameError(txt)

    def __str__(self):
        return self.name()
        
    # Get characteristics of the 3-sounds chord    
    def is_minor(self):
        return self.minor

    def is_major(self):
        return self.major

    def is_sus2(self):
        return self.sus2
    
    def is_sus4(self):
        return self.sus4

    def is_aug(self):
        return self.aug

    def is_dim(self):
        return self.dim

    def name(self):
        # Fondamental note
        txt = self.n1.pitch.upper()
        if self.n1.alteration != 'natural':
            txt += self.n1.alteraction

        if self.minor:
            txt += 'min'

        if self.aug:
            txt += 'aug'

        if self.dim:
            txt += 'dim'

        if self.sus2:
            txt += 'sus2'

        if self.sus4:
            txt += 'sus4'
            
        return txt 

    def lilypond_str(self):
        return  '<' + ' '.join([n.lilypond_str() for n in self.notes_list]) + '>'
    
    def inversion(self, position='root'):
        return 

    def shift_octave(self, i):
        '''
        Shift all the note from i octaves (i: postive/negative integer)
        '''
        return triad(self.n1.shift_octave(i),
                     self.n2.shift_octave(i),
                     self.n3.shift_octave(i))        
        
    @classmethod
    def build(self, I, nature, position='fond'):
        '''
        I        = fondamental of the chords
        nature   = major, minor, augmented, diminished
        position = choice of the lower note (bass = I, III or V) 
        '''
        n1 = I
        nature = nature.lower()
        if nature == 'maj' or nature == 'major':
            n2 = n1.note_of('3M')
            n3 = n1.note_of('5J')
        elif nature == 'min' or nature == 'minor':
            n2 = n1.note_of('3m')
            n3 = n1.note_of('5J')
        elif nature == 'dim' or nature == 'diminished':
            n2 = n1.note_of('3m')
            n3 = n1.note_of('5-')
        elif nature == 'aug' or nature == 'augmented':
            n2 = n1.note_of('3M')
            n3 = n1.note_of('5+')
        elif nature == 'sus2' or nature == 'suspended2':
            n2 = n1.note_of('2M')
            n3 = n1.note_of('5J')
        elif nature == 'sus4' or nature == 'suspended4':
            n2 = n1.note_of('4J')
            n3 = n1.note_of('5J')
        else:
            raise NameError(f'nature of triad cannot be {nature}')

        return triad(n1, n2, n3)

    @classmethod
    def build_from_intervals(self, fond, i1, i2):
        '''
        Build a triad corresponding to a fondamental 
        with 2 intervals with respect to the fondamental.
        e.g. : a Cmajor would be build_from_intervals(C, '3M', '5J')
        '''
        return triad(fond, fond.note_of(i1), fond.note_of(i2))
    
    
###############
##  4 NOTES  ##
###############    

class tetrad:

    # Constructor from the 4 notes
    def __init__(self, n1, n2, n3, n4):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        self.triad = triad(n1, n2, n3)
        self.notes_list = [n1, n2, n3, n4]
        
        # Chord nature related to the 3rd
        self.min3 = False
        self.maj3 = False
        self.sus2 = False
        self.sus4 = False

        # Chord nature related to the fifth
        self.per5 = False
        self.aug5 = False
        self.dim5 = False

        # Chord nature related to the seventh
        self.maj7 = False
        self.min7 = False
        self.dim7 = False

        # Global nature
        self.dim  = False
        self.aug  = False
        self.ddim = False
        
        # Getting the 3 intervals
        a = n2.diff(n1)
        b = n3.diff(n1)
        c = n4.diff(n1)
        
        # Nature related to the 3rd for perfect fifth
        if a==1:
            self.sus2 = True
        if a==1.5:
            self.min3 = True
        if a==2:
            self.maj3 = True
        if a==2.5:
            self.sus4 = True

        # Nature related to the fifth
        if b==3:
            self.dim5 = True
        if b==3.5:
            self.per5 = True
        if b==4:
            self.aug5 = True
        
        # Nature related to the seventh
        if c==5.5:
            self.maj7 = True
        if c==5.0:
            self.min7 = True
        if c==4.5:
            self.dim7 = True
        
        # Global nature (dim v.s. demi-dim)
        if self.min3 and self.dim5 and self.min7:
            self.ddim = True

        if self.min3 and self.dim5 and self.dim7:
            self.dim = True

    # Defining the string operator
    def __str__(self):
        return self.name()
        
    # Get characteristics of the 4-sounds chord    
    def is_minor(self):
        return self.triad.is_minor()

    def is_major(self):
        return self.triad.is_major()
    
    def is_sus2(self):
        return self.triad.is_sus2()

    def is_sus4(self):
        return self.triad.is_sus4()

    def is_aug(self):
        return self.triad.is_aug()
    
    def is_maj7(self):
        return self.maj7
    
    def is_ddim(self):
        return self.triad.is_dim() and self.min7
    
    def is_dim(self):
        return self.triad.is_dim() and self.dim7
    
    def name(self):
        # Fondamental note
        txt = self.n1.pitch.upper()
        if self.n1.alteration != 'natural':
            txt += self.n1.alteration

        # Minor
        if self.is_minor():
            txt += 'min'
            if self.min7:
                txt += '7'
            if self.maj7:
                txt += 'Maj7'
            if self.dim7:
                txt += '[dim7]'
            return txt

        # Major
        if self.is_major():
            if self.min7:
                txt += '7'
            if self.maj7:
                txt += 'Maj7'
            if self.dim7:
                txt += '[dim7]'
            return txt
                
        # Suspended2
        if self.is_sus2():
            txt += 'sus2'
            if self.min7:
                txt += '7'
            if self.maj7:
                txt += 'Maj7'
            return txt

        # Suspended4
        if self.is_sus4():
            txt += 'sus4'
            if self.min7:
                txt += '7'
            if self.maj7:
                txt += 'Maj7'
            return txt
        
        # Augmented
        if self.is_aug():
            txt += 'aug'
            if self.min7:
                txt += '7'
            if self.maj7:
                txt += 'Maj7'
            return txt
        
        # Demi-diminished
        if self.is_ddim():
            txt += 'min7b5'
            return txt

        # Diminished
        if self.is_dim():
            txt += 'dim7'
            return txt

        return 'ton accord est foireux mon pote'
    
    
    def lilypond_str(self):
        return  '<' + ' '.join([n.lilypond_str() for n in self.notes_list]) + '>'
    

    def shift_octave(self, i):
        '''
        Shift all the note from i octaves (i: postive/negative integer)
        '''
        return tetrad(self.n1.shift_octave(i),
                      self.n2.shift_octave(i),
                      self.n3.shift_octave(i),
                      self.n4.shift_octave(i))
    
    @classmethod
    def build_from_triad(self, triad, n4):
        '''
        Build a tetrad from a triad and 4th note
        '''
        return tetrad(triad.n1, triad.n2, triad.n3, n4) 
    
    @classmethod
    def build(self, n1, nature, position='fondamental'):
        '''
        n1       = fondamental of the chords
        nature   = maj_7 , maj_maj7 , min_7 , min_maj7, sus4_7,
                   aug_7 , aug_maj7 , ddim_7  , dim_7, dim_maj7
                   maj_7 , min_6    , min_min6,
                   #sus2_7, sus2_maj7

        position = choice of the lower note (bass = I, III, V or VII) 
        '''

        # Check the nature of the tetrad is one of the possibility
        if nature.lower() not in possible_tetrads:
            raise NameError(f'ERROR: the tetrad nature {nature} is not supported, only {possible_tetrads} are.')
        
        # Initialize notes values
        n2, n3, n4 = n1, n1, n1

        # Majors/minors
        if nature=='maj_7':
            n2 = n1.note_of('3M')
            n3 = n1.note_of('5J')
            n4 = n1.note_of('7m')
        elif nature=='maj_maj7':
            n2 = n1.note_of('3M')
            n3 = n1.note_of('5J')
            n4 = n1.note_of('7M')
        elif nature=='min_7':
            n2 = n1.note_of('3m')
            n3 = n1.note_of('5J')
            n4 = n1.note_of('7m')
        elif nature=='min_maj7':
            n2 = n1.note_of('3m')
            n3 = n1.note_of('5J')
            n4 = n1.note_of('7M')

        # Suspended chords
        elif nature=='sus2_7':
            n2 = n1.note_of('2M')
            n3 = n1.note_of('5J')
            n4 = n1.note_of('7m')
        elif nature=='sus2_maj7':
            n2 = n1.note_of('2M')
            n3 = n1.note_of('5J')
            n4 = n1.note_of('7M')
        elif nature=='sus4_7':
            n2 = n1.note_of('4J')
            n3 = n1.note_of('5J')
            n4 = n1.note_of('7m')
        elif nature=='sus4_maj7':
            n2 = n1.note_of('4J')
            n3 = n1.note_of('5J')
            n4 = n1.note_of('7M')

        # Augmented / (demi)-diminished chords
        elif nature=='aug_7':
            n2 = n1.note_of('3M')
            n3 = n1.note_of('5+')
            n4 = n1.note_of('7m')
        elif nature=='aug_maj7':
            n2 = n1.note_of('3M')
            n3 = n1.note_of('5+')
            n4 = n1.note_of('7M')
        elif nature=='ddim_7':
            n2 = n1.note_of('3m')
            n3 = n1.note_of('5-')
            n4 = n1.note_of('7m')
        elif nature=='dim_7':
            n2 = n1.note_of('3m')
            n3 = n1.note_of('5-')
            n4 = n1.note_of('7-')    
        elif nature=='dim_maj7':
            n2 = n1.note_of('3m')
            n3 = n1.note_of('5-')
            n4 = n1.note_of('7M')    

        # Chords of 6th
        elif nature=='maj_6':
            n2 = n1.note_of('3M')
            n3 = n1.note_of('5J')
            n4 = n1.note_of('6M')
        elif nature=='min_6':
            n2 = n1.note_of('3m')
            n3 = n1.note_of('5J')
            n4 = n1.note_of('6M')
        elif nature=='min_min6':
            n2 = n1.note_of('3m')
            n3 = n1.note_of('5J')
            n4 = n1.note_of('6m')    

        return tetrad(n1, n2, n3, n4)

    
class extended_chords:

    def __init__(self, n1, basis_nature, interval_ext_list):
        '''
        Arguments:
         - n1: tonic of the chords
         - basis_nature: nature of the chords to extend (triad or tetrad)
         - interval_ext_list: list of interval to be added
        '''

        # Chord to be extended
        if basis_nature in possible_triads:
            self.basis_chord = triad.build(n1, basis_nature)
        elif basis_nature in possible_tetrads:
            self.basis_chord = tetrad.build(n1, basis_nature)
        else:
            txt  = f'extended_chords:: {basis_nature} is not supported'
            txt += f', only {possible_triads} and {possible_tetrads} are.'
            raise NameError(txt)
        
        # Extension notes
        self.extensions = [n1.note_of(interval) for interval in interval_ext_list]
        
        # Full list of notes
        self.notes_list = self.basis_chord.notes_list + self.extensions


    def shift_octave(self, i):
        '''
        Shift all the note from i octaves (i: postive/negative integer)
        '''
        ext = copy.deepcopy(self)
        ext.basis_chord = self.basis_chord.shift_octave(i)
        ext.extensions = [n.shift_octave(i) for n in self.extensions]
        ext.notes_list = ext.basis_chord.notes_list + ext.extensions
        return ext

        
    def lilypond_str(self):
        return  '<' + ' '.join([n.lilypond_str() for n in self.notes_list]) + '>'

    @classmethod
    def build(self, n1, nature):

        allowed_chords = possible_ninth + possible_eleventh + possible_thirteenth
        if nature not in allowed_chords:
            txt  = f'extended_chords:: {nature} is not supported'
            txt += f', only {allowed_chords}'
            raise NameError(txt)

        # 9th Chords
        if nature == 'maj_add9':
            return extended_chords(n1, 'maj', ['9M'])
        elif nature == 'maj_maj9':
            return extended_chords(n1, 'maj_maj7', ['9M'])
        elif nature == 'maj_69':
            return extended_chords(n1, 'maj_6', ['9M'])
        elif nature == 'maj_9':
            return extended_chords(n1, 'maj_7', ['9M'])
        elif nature == 'maj_7b9':
            return extended_chords(n1, 'maj_7', ['9m'])
        elif nature == 'maj_7d9':
            return extended_chords(n1, 'maj_7', ['9+'])
        elif nature == 'min_9':
            return extended_chords(n1, 'min_7', ['9M'])
        elif nature == 'ddmin_9':
            return extended_chords(n1, 'ddim_7', ['9M'])
        elif nature == 'min_maj9':
            return extended_chords(n1, 'min_maj7', ['9M'])
        elif nature == 'min_69':
            return extended_chords(n1, 'min_6', ['9M'])
        elif nature == 'sus4_9':
            return extended_chords(n1, 'sus4_7', ['9M'])
        elif nature == 'sus4_b9':
            return extended_chords(n1, 'sus4_7', ['9m'])
                
        # Eleventh chords
        elif nature == 'maj_maj7_d11':
            return extended_chords(n1, 'maj_maj7', ['11+'])
        elif nature == 'maj_maj9_d11':
            return extended_chords(n1, 'maj_maj7', ['9M', '11+'])
        elif nature == 'maj_7_d11':
            return extended_chords(n1, 'maj_7', ['11+'])
        elif nature == 'maj_9_d11':
            return extended_chords(n1, 'maj_7', ['9M', '11+'])
        elif nature == 'maj_7_b9_d11':
            return extended_chords(n1, 'maj_7', ['9m', '11+'])
        elif nature == 'maj_7_d9_d11':
            return extended_chords(n1, 'maj_7', ['9+', '11+'])
        elif nature == 'min_7_add11':
            return extended_chords(n1, 'min_7', ['11J'])
        elif nature == 'min_11':
            return extended_chords(n1, 'min_7', ['9M','11J'])
        elif nature == 'ddmin_11':
            return extended_chords(n1, 'ddim_7', ['11J'])

        # Thirteenth chords
        elif nature == 'maj_maj7_add13':
            return extended_chords(n1, 'maj_maj7', ['13M'])
        elif nature == 'maj_maj13':
            return extended_chords(n1, 'maj_maj7', ['9M', '13M'])
        elif nature == 'maj_maj13_d11':
            return extended_chords(n1, 'maj_maj7', ['9M', '11+', '13M'])
        elif nature == 'maj_7_add13':
            return extended_chords(n1, 'maj_7', ['13M'])
        elif nature == 'maj_13':
            return extended_chords(n1, 'maj_7', ['9M', '13M'])
        elif nature == 'maj_13_b9':
            return extended_chords(n1, 'maj_7', ['9m', '13M'])
        elif nature == 'maj_13_d9':
            return extended_chords(n1, 'maj_7', ['9+', '13M'])        
        elif nature == 'maj_7_b13_b9':
            return extended_chords(n1, 'maj_7', ['9m', '13m'])
        elif nature == 'maj_7_b13_d9':
            return extended_chords(n1, 'maj_7', ['9+', '13m'])
        elif nature == 'min_7_add13':
            return extended_chords(n1, 'min_7', ['13M'])
        elif nature == 'min_13':
            return extended_chords(n1, 'min_7', ['9M', '11J', '13M'])
        elif nature == 'sus4_13':
            return extended_chords(n1, 'sus4_7', ['9M', '13M'])
        elif nature == 'sus4_9_b13':
            return extended_chords(n1, 'sus4_7', ['9M', '13m'])
        elif nature == 'sus4_7_b9_b13':
            return extended_chords(n1, 'sus4_7', ['9m', '13m'])


        
class scale:

    def __init__(self, tonic, name):

        # Checking if the name is supported
        if name not in possible_scales:
            raise NameError(f'{name} is not supported, only {possible_scales} are.')
        
        # Store the nature
        self.nature = name

        # Get all the intervals
        self.intervals = scales_intervals[name]

        # Store the list of note
        self.notes_list = [tonic.note_of(i) for i in self.intervals]
        
    def __str__(self):
        return  ' '.join([str(n) for n in self.notes_list])

    def name(self):
        # Fondamental note
        n1 = self.notes_list[0]
        txt = n1.pitch.upper()
        if n1.alteration != 'natural':
            txt += n1.alteration
        txt += ' ' + nice_scales_names[self.nature]
        return txt

    def lilypond_str(self, with_name=False, name_color='black'):
        '''
        When with_name is True, it adds the name of the scale
        on top of the first note. 'name_color' allows to change
        the color of the text.
        '''
        if with_name:
            name = self.name().replace('b', '"\\flat"').replace('#', '"\\sharp"')
            txt  = f'{self.notes_list[0].lilypond_str()}1^\\markup{{ \\with-color "{name_color}" \\concat{{"{name}"}} }} \\bar "" '
            txt += '1 \\bar "" '.join([n.lilypond_str() for n in self.notes_list[1:]])
            return txt
        else :
            return  '1 \\bar "" '.join([n.lilypond_str() for n in self.notes_list])
