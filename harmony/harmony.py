# Accepted pitch
possible_pitchs = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
tons_steps = [1, 1, 0.5, 1, 1, 1, 0.5]
N_pitch = len(possible_pitchs)

# Accepted alterations
possible_alterations = ['b', '#', 'bb', '##', 'natural']
alteration_values = {
    'b' : -0.5,
    '#' : +0.5,
    'bb': -1.0,
    '##': +1.0,
    'natural': 0,
}

# Intervals names
possible_intervals  = ['un']
possible_intervals += ['2m', '2M', '2+']
possible_intervals += ['3m', '3M']
possible_intervals += ['4J', '4+']
possible_intervals += ['5-', '5J', '5+']
possible_intervals += ['6m', '6m', '6+']
possible_intervals += ['7-', '7m', '7M']
possible_intervals += ['8J']

# Scale names - later add other modes
possible_scales = ['major', 'minor_natural', 'minor_harmonic', 'minor_melodic']

# Scales composition
scales_intervals = {
    'major'         : ['un', '2M', '3M', '4J', '5J', '6M', '7M'],
    'minor_natural' : ['un', '2M', '3m', '4J', '5J', '6m', '7m'],
    'minor_harmonic': ['un', '2M', '3m', '4J', '5J', '6m', '7M'],
    'minor_melodic' : ['un', '2M', '3m', '4J', '5J', '6M', '7M'],
}

# Interval values (ton)
# TO-DO :
#   * add 9th, 11th and 13th
interval_values = {
    'un':   0,
    '2m': 0.5,
    '2M':   1,
    '2+': 1.5,
    '3m': 1.5,
    '3M':   2,
    '4J': 2.5,
    '4+':   3,
    '5-':   3,
    '5J': 3.5,
    '5+':   4,
    '6m':   4,
    '6M': 4.5,
    '6+':   5,
    '7-': 4.5,
    '7m':   5,
    '7M': 5.5,
    '8J':   6,
}


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

        # If unisson rerturn the same note
        if interval == 'un':
            return self
            
        # Number of notes to be incremented (eg. 1 for a second)
        index_to_add = int(interval[0])-1

        # diminished, just, augemented, major, minor
        quality = interval[1]

        # get the index of the current note
        index = possible_pitchs.index(self.pitch)

        # Getting the new pitch name
        new_pitch, new_octave  = '', self.octave

        # In case of ascending interval
        if not descending:
            new_index = index + index_to_add
            if new_index < N_pitch:
                new_pitch = possible_pitchs[new_index]
            else:
                new_pitch = possible_pitchs[new_index-N_pitch]
                new_octave = self.octave + 1
                
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
                txt  = f'Trying to determine the {interval} of {self}.'
                txt += f'The ton difference between {self} and the target {x} leads to Delta={ntons-nt_target}, which not correct.'
                txt += f'Only [+/- 0.5, +/- 1.0] are supported.'
                raise NameError(txt)
            
            
        # Return the result
        return res


class triad:

    # Constructor from 3 notes
    def __init__(self, n1, n2, n3):

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

        # Which renversement ?
        # To be implemented
        
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
        nature   = maj_7 , maj_maj7 , min_7 , min_maj7 , 
                   sus2_7, sus2_maj7, sus4_7, sus4_maj7,
                   aug_7 , aug_maj7 , ddim_7  , dim_7,
        position = choice of the lower note (bass = I, III, V or VII) 
        '''

        # Check the nature of the tetrad is one of the possibility
        nature = nature.lower()
        nature_options  = ['maj_7' , 'maj_maj7' , 'min_7' , 'min_maj7' ]
        nature_options += ['sus2_7', 'sus2_maj7', 'sus4_7', 'sus4_maj7']
        nature_options += ['aug_7' , 'aug_maj7' , 'ddim_7', 'dim_7'    ]
        if nature not in nature_options:
            raise NameError(f'ERROR: the tetrad nature {nature} is not supported, only {nature_options} are.')
        
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
        
        return tetrad(n1, n2, n3, n4)

    
class scale:

    def __init__(self, tonic, name):

        # Checking if the name is supported
        if name not in possible_scales:
            raise NameError(f'{name} is not supported, only {possible_scales} are.')
        
        # Get all the intervals
        self.intervals = scales_intervals[name]

        # Store the list of note
        self.notes_list = [tonic.note_of(i) for i in self.intervals]
        
        # Store the 7 degrees of the scale
        self.n1 = tonic.note_of(self.intervals[0])
        self.n2 = tonic.note_of(self.intervals[1])
        self.n3 = tonic.note_of(self.intervals[2])
        self.n4 = tonic.note_of(self.intervals[3])
        self.n5 = tonic.note_of(self.intervals[4])
        self.n6 = tonic.note_of(self.intervals[5])
        self.n7 = tonic.note_of(self.intervals[6])

        
    def __str__(self):
        return  ' '.join([str(n) for n in self.notes_list])
