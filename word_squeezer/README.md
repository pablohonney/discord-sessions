# Word Squeezer

Word squeezer (слововыжималка) is a game of finding new words from character subsets of a long source word.

For example the word 'morning' will produce the words 'groin mignon minor morin', of length 5 letters or more, excluding 'morning' itself. 

On a Mac system the command would be `python squeeze.py -f /usr/share/dict/words morning -l 5`

## Pick a random word of given minimum length. The length is given in bytes, so for multibyte encodings, the length needs to be adjusted.

cat /usr/share/dict/words | awk '{ if (length($0) > 15 ) print }' | shuf | head -1