import re
from collections import OrderedDict

print "Viterbi!"

# Read in files
lexicon = {}
with open('lexicon.txt') as f:
	for line in f:
		split = re.split(r'\s+', line)
		lexicon[split[0]] = split[1:-2]

phonemes = []
with open('phonemes.txt') as f:
	for line in f:
		phonemes.append(line.strip())

B = {}
with open('output.txt') as f:
	for line in f:
		split = re.split(r'\s+', line.strip())
		t = int(split[0])
		if t not in B:
			B[t] = {}
		if split[1] not in B[t]:
			B[t][split[1]] = {}
		B[t][split[1]][int(split[2])] = float(split[3])

# Number of time frames 
t = len(B)

# Number of words in the lexicon
N = len(lexicon)

V = [{}]
path = {}

print 'Initialize Viterbi Trellis'
for digit in lexicon.keys():
	V[0][digit] = OrderedDict()
	for i, phoneme in enumerate(lexicon[digit]):
		if i == 0:
			V[0][digit][phoneme] = (B[0][phoneme][0], 0, 0)
		else:
			V[0][digit][phoneme] = (0,0,0)

print V[0]['seven']['S']

