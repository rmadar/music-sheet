# Accepted pitch
possible_pitch = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
tons_steps = [1, 1, 0.5, 1, 1, 1, 0.5]
N_pitch = 6

# Accepted alterations
possible_alterations = ['b', '#', 'bb', '##', 'natural']

# Intervals names
possible_intervals  = ['un']
possible_intervals += ['2m', '2M', '2+']
possible_intervals += ['3m', '3M']
possible_intervals += ['4J', '4+']
possible_intervals += ['5-', '5J', '5+']
possible_intervals += ['6m', '6m', '6+']
possible_intervals += ['7-', '7m', '7M']
possible_intervals += ['8J']

# Interval values (ton)
# TO-DO :
#   * check the interval values
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
    '7-':   5,
    '7m':   5,
    '7M': 5.5,
    '8J':   6,
}


class note:


    # Constructor of the note
    def __init__(self, pitch, alteration='natural', octave=4):

        '''
        pitch      [string]: do re mi fa sol la si (international notation)
        alteration [string]: natural, b, #, bb, ## (default = 'natural')
        octave     [int]   : octave of the pitch (default 4: middle octave on piano)
        '''
        
        if pitch not in possible_pitch:
            return NameError(f'{pitch} is not supported, only {possible_pitch} are.')

        if alteration not in possible_alterations:
            return NameError(f'{alteration} is not supported, only {possible_alterations} are.')

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


    # Compute the absolute distance (in tone) wrt the first C on a piano
    def absolute_tons(self):
        '''
        Return the absolute number of tons with respect
        to the first C of a piano
        '''
        i = possible_pitch.index(self.pitch)
        rel_ton = sum(tons_steps[:i])
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
    def note_of(self, interval, ascending=True):

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
        index = possible_pitch.index(self.pitch)

        # Getting the new pitch name
        new_pitch, new_octave  = '', self.octave

        # In case of ascending interval
        if ascending:
            new_index = index + index_to_add
            if new_index < N_pitch:
                new_pitch = possible_pitch[new_index]
            else:
                new_pitch = possible_pitch[new_index-N_pitch-1]
                new_octave = self.octave + 1
                
        # In case of descending interval
        else:
            new_index = index - index_to_add
            if new_index > 0:
                new_pitch = possible_pitch[new_index]
            else:
                new_pitch = possible_pitch[N_pitch+new_index+1]
                new_octave = self.octave - 1

        # Determining the alteration
        x = note(new_pitch, 'natural', new_octave)
        res = x
        nt_target = interval_values[interval]
        if ascending:
            ntons = x.diff(self)
            if ntons == nt_target:
                res = x
            elif ntons == nt_target + 0.5:
                res = note(new_pitch, 'b', new_octave)
            elif ntons == nt_target + 1:
                res = note(new_pitch, 'bb', new_octave)
            elif ntons == nt_target - 0.5:
                res = note(new_pitch, '#', new_octave)
            elif ntons == nt_target - 1:
                res = note(new_pitch, '##', new_octave)
            else:
                txt = 'The ton difference is not correct, please investigage'
                NameError(txt)
            
            
        # Return the result
        return res
