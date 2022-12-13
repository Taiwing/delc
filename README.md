# delc

Delete comments in C files (both classic C and C++ type comments) in compliance
with the 42 school standard. Useful if you want to comment your code as much as
you like without the hassle of having to manually remove them when submitting a
42 project.

## Usage

```
usage: delc [-h] [-s count] file ...
options:
	-h | --help:			print this
	-s | --skip count: 		delc will skip the 'count' first lines
							to avoid removing any header
```

By default the 'skip' count is set to 12, which is the length of the 42 header
with the new line, so that it is not removed by delc. Also, delc doesn't just
remove the comments, it also removes any superfluous white characters in the
file. If a comment takes an entire line, it deletes the preceding new line.
It is to be noted that if comments are separated by new lines, they are going
to stay after delc is done, as delc only removes one new line by comment.

## Warning

This project is deprecated because HIGHLY USELESS and even DANGEROUS. This was
only ever useful as a normifyer tool back when comments were forbidden. Thank
god it's not the case anymore.
