import re
from collections import OrderedDict

print "Viterbi!"

# Read in files
Lexicon = OrderedDict()
with open('lexicon.txt') as f:
	for line in f:
		split = re.split(r'\s+', line)
		Lexicon[split[0]] = split[1:-2]

Phonemes = []
with open('phonemes.txt') as f:
	for line in f:
		Phonemes.append(line.strip())

B = {}
#with open('output.txt') as f:
with open('fake.output') as f:
	for line in f:
		split = re.split(r'\s+', line.strip())
		t = int(split[0])
		if t not in B:
			B[t] = {}
		if split[1] not in B[t]:
			B[t][split[1]] = {}
		B[t][split[1]][int(split[2])] = float(split[3])

# Number of time frames 
T = len(B)

# Number of words in the lexicon
N = len(Lexicon)

# List the states and keep track of properties of indexes
states = []
i = 0
firstSubphone = [] # Idxes of the first subphone of a digit
digitOfState = {} # dict of state idx to digit
for digit, phonemeList in Lexicon.iteritems():
	firstSubphone.append(i)
	for phoneme in phonemeList:
		for subphone in range(3):
			states.append((i, digit, phoneme, subphone))
			digitOfState[i] = digit
			i = i + 1 
lastSubphone = firstSubphone[1:] - 1
print firstSubphone
print lastSubphone

# V = [{}]
# path = {}
# print 'Initialize Viterbi Trellis'
# for q in states:
# 	i = q[0]
# 	digit = q[1]
# 	phoneme = q[2]
# 	subphone = q[3]
# 	if i in firstSubphone:
# 		V[0][i] = B[0][phoneme][subphone]
# 	else:
# 		V[0][i] = 0

# print 'Run Viterbi for t > 0'
# for t in range(T):
# 	V.append({})
# 	for q in states:
# 		i = q[0]
# 		digit = q[1]
# 		phoneme = q[2]
# 		subphone = q[3]
# 		cases = []
# 		# Stay in the same state
# 		cases.append(V[t-1][i]+B[t][phone][subphone])
# 		if i in firstSubphone:
# 			# From last state of every digit
# 			cases.append(max(V[t-1][ls]+B[t][phone][subphone] for ls in firstSubphone))

# V = [{}]
# path = {}

# print 'Initialize Viterbi Trellis'
# for digit in Lexicon.keys():
# 	V[0][digit] = OrderedDict()
# 	for i, phoneme in enumerate(Lexicon[digit]):
# 		if i == 0:
# 			V[0][digit][phoneme] = (B[0][phoneme][0], 0, 0)
# 		else:
# 			V[0][digit][phoneme] = (0,0,0)

# print V[0]['seven']


# print 'Run Viterbi for t > 0'
# for t in range(1, T):
# 	V.append({})
# 	p = []
# 	for digit, phonemes in Lexicon:
# 		for phone in phonemes:
# 			for subphone in range(3):
# 				p.append(V[t-1][digit][phone][subphone]+B[t][phone][subphone])





