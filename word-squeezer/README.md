# Word Squeezer

Word squeezer (слововыжималка) is a game of finding new words from character subsets of a long source word.

For example the word 'morning' will produce the words 'groin mignon minor morin', of length 5 letters or more, excluding 'morning' itself. 

On a Mac system the command would be `word-squeezer -f /usr/share/dict/words morning -l 5`

## Pick a random word of given minimum length. The length is given in bytes, so for multibyte encodings, the length needs to be adjusted.

cat /usr/share/dict/words | awk '{ if (length($0) > 15 ) print }' | shuf | head -1

# Wordament

Wordament is an online word puzzle from Microsoft, where users need to find words from a word grid.
The words need to be continuous in the grid, including diagonal, without jumps."
    
example:
    l r t l
    f a a n
    g c s t
    l e e l

On a Mac system the command would be `wordament -f /usr/share/dict/words -l 3 'l r t l|f a a n|g c s t|l e e l'`

TODO: Wordament slots can contain alternating letters. This feature is not supported yet. e.g. `wordament -f /usr/share/dict/words -l 3 'l r/d t l|f a a n|g c s t|l e e l'`