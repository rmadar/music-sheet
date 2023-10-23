# Music Sheet with Lilypond and python

This repository holds a simple (WIP) python interface to generate music sheets using [Lylipond](http://lilypond.org/),
and export the corresponding audio file (mp3 format converted from MIDI using [timidity](https://launchpad.net/ubuntu/hirsute/+package/timidity)). This tool depends naturally on these two sofware. Caution: I am discovering Lylipond on the fly while I am writing this tool.

## Practicing bass clef reading

The first use case is to be able to generate random scores with a given level of difficulty for both note range and rythm pattern.
An example can be found [here](exercise-reading/example_random_score.py), producing this score:
![image](reading-bass/example.jpg)

## Practicing triad chords 

The tool offer the possibility to write exercises sheet to find triads names from the 3 notes, or find the 3 notes from the name. The correction can also be generated.

![image](harmony/chords_examples.png)
![image](harmony/chords_correction_example.png)

## Practingin rythm pattern

Another use is to create simple and short phrases from basic pattern, based on 16th notes.

![image](reading-rythm/eg.png)

## TO-DO List

 - [ ] Add tetrads
 - [ ] Add scales

