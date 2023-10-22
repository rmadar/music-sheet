import harmony as ha

LA  = ha.note('a')
DO  = ha.note('c')
MId = ha.note('e', '#')

# Basic checks
#print( LA, MId )
#print( LA.absolute_tons() )
#print( LA.diff(DO) )
#print( DO.diff(LA) )
print( f'\nPerfect 5th of LA {LA.note_of("5J", ascending=False)}' )
print( f'Perfect descendant 5th of DO {DO.note_of("5J", ascending=False)}' )



# Testing intervals findings - C major key
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
