import score_creator as sc

# Generation de 100 mesure de note et rythme aleatoire.
Nmeas  = 100
piches = [sc.notes[i] for i in sc.rnd.randint(low=0, high=len(sc.notes)-5, size=100*4)]
times  = [t for i in range(4*Nmeas) for t in sc.un_temps(2, False)] 
notes  = " ".join(["{}{}".format(p, t) for p, t in zip(piches, times)])

# Creer une portee a partir de ces notes
staff = sc.staff(notes)

# Mettre cette portee dans une partition
score = sc.score([staff])

# Creer le fichier final contenant cette partition
sheet = sc.sheet(score)

# Save it
sheet.save(midi=False)
