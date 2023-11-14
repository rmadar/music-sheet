import sys
sys.path.append("../src")
import numpy as np
import score_creator as sc
import harmony as ha

# Generate the scales
N = 100
fonds = ha.generate_random_piches(N)
natures = np.random.choice(a=ha.possible_scales, size=10*N)
scales = [ha.scale(f, n) for f, n in zip(fonds, natures)]

# Loop over the scales and build
#  - staff string with notes but no scale names
#  - staff string without note with scales names
#  - switch every 2 scales and break the line
str_staff_scales = ''
str_staff_corr   = ''
for i, ss in enumerate(np.array_split(scales, int(N/2))):
    if i%2 == 0:
        str_staff_scales += '\n\\undo \\hide NoteHead \\undo \\hide Accidental \\override NoteHead.no-ledgers = ##f '
        str_staff_scales += ' '.join([s.lilypond_str() for s in ss])
        str_staff_scales += ' \\break\n '

        str_staff_corr += '\override NoteHead.color = #black \override Accidental.color = #black '
        str_staff_corr += ' '.join([s.lilypond_str(with_name=True, name_color='red') for s in ss])
        str_staff_corr +=  ' \\break\n '
        
    else :
        str_staff_scales += '\n\\hide NoteHead \\hide Accidental \\override NoteHead.no-ledgers = ##t '
        str_staff_scales += ' '.join([s.lilypond_str(with_name=True) for s in ss])
        str_staff_scales += ' \\break\n '
        
        str_staff_corr += '\override NoteHead.color = #red \override Accidental.color = #red '
        str_staff_corr += ' '.join([s.lilypond_str(with_name=True) for s in ss])
        str_staff_corr += ' \\break\n '
        
    
# Create the two staffs
staff_scales = sc.staff(str_staff_scales, clef='treble', time=None, tempo=None)
staff_corr   = sc.staff(str_staff_corr  , clef='treble', time=None, tempo=None)

# Mettre cette portee dans une partition
score = sc.score([staff_scales])
score_corr = sc.score([staff_corr])

# Creer le fichier final contenant cette partition
sheet = sc.sheet(score, title='Identification de gammes', composer='',
                 hide_BarNumber=True,
                 hide_TimeSignature=True)
sheet_corr = sc.sheet(score_corr, title='Identification de gammes - CORRECTION', composer='',
                 hide_BarNumber=True,
                 hide_TimeSignature=True)

# Save it with the ly file name
sheet.save(fname='scales_exercies.ly')
sheet_corr.save(fname='scales_exercies_CORRECTION.ly')

