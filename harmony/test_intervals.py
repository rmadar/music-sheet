import harmony as ha

LA  = ha.note('a')
DO  = ha.note('c')
MI  = ha.note('e')
MIb = ha.note('e', 'b')
MId = ha.note('e', '#')


# Basic checks on notes
print( LA, MIb )
print( LA.lilypond_str(), MIb.lilypond_str() )
print( LA.absolute_tons() )
print( LA.diff(DO) )
print( DO.diff(LA) )
print( f'\nPerfect 5th of LA {LA.note_of("5J")}' )
print( f'Perfect descendant 5th of DO {DO.note_of("5J", descending=False)}' )


# Testing intervals using notes - C major key
print('')
print('C major')
txt = ''
for interval in ['un', '2M', '3M', '4J', '5J', '6M', '7M', '8J']:
     txt += f' {DO.note_of(interval)}'
print(txt)


# C minor natural key
print('')
print('C minor natural')
txt = ''
for interval in ['un', '2M', '3m', '4J', '5J', '6m', '7m', '8J']:
    txt += f' {DO.note_of(interval)}'
print(txt)


# Test of intervals
i1 = ha.interval(DO, LA)
i2 = ha.interval(LA, DO)
i3 = ha.interval(LA, DO.shift_octave(1))
i4 = ha.interval(LA, ha.note('e', alteration='#', octave=6))
i5 = ha.interval(LA, MIb)
i6 = ha.interval(MI, MIb)
print('')
print('Testing interval:')
for i in [i1, i2, i3, i4, i5, i6]:
     print(i5)
     print(f'  - {i} is {i.name()} and would be writen {i.lilypond_str()} in Lilypond')

