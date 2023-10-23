import harmony as ha

# Defining 4 A scales
Amajor = ha.scale(ha.note('a'), 'major')
Aminor = ha.scale(ha.note('a'), 'minor_natural')
AminHa = ha.scale(ha.note('a'), 'minor_harmonic')
AminMe = ha.scale(ha.note('a'), 'minor_melodic')

# Putting them in list with they name
scales = [Amajor, Aminor, AminHa, AminMe]
names  = ['A major', 'Amin Nat', 'Amin Harm', 'Amin Melo']

# Print the scales
for s, n in zip(scales, names):
    print(n+': ', s)
