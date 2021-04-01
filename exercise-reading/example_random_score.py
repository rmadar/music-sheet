import sys
sys.path.append("../src")
import numpy as np
import score_creator as sc


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

# All notes
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



# Generation de 100 mesure de note et rythme aleatoire.
Nmeas  = 100
piches = [notes[i] for i in np.random.randint(low=0, high=len(notes)-5, size=100*4)]
times  = [t for i in range(4*Nmeas) for t in un_temps(2, False)] 
notes  = " ".join(["{}{}".format(p, t) for p, t in zip(piches, times)])

# Creer une portee a partir de ces notes
staff = sc.staff(notes)

# Mettre cette portee dans une partition
score = sc.score([staff])

# Creer le fichier final contenant cette partition
sheet = sc.sheet(score)

# Save it
sheet.save(midi=False)
