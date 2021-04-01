import sys
sys.path.append("../src")
import score_creator as sc

pattern = sc.rythm_pattern_16th

# Helper function
def score(note_list, title=''):
    '''
    note_list: list of string, following the lilypond notation.
    title    : title of the score
    return a score object.
    '''
    notes = ' '.join(note_list)
    staff = sc.staff(notes, clef='drum')
    return sc.score([staff], title=title)


# Create a sheet that will contain all patterns
sheet = sc.sheet(title='Rythmic Patterns From 16th Notes')
for k, v in pattern.items():
    n  = [*v, 'r4', *v, 'r4'] * 2
    n += ['\\break']
    n += [*v, *v, 'r4', 'r4']
    n += [*v, *v, *v, 'r4' ]
    sheet.add_score(score(n, title='Pattern with {}'.format(k)))


# Save it
sheet.save(midi=False)
