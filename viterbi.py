import re
from collections import OrderedDict

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
# T = 100

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

lastSubphone = firstSubphone[1:]
lastSubphone.append(i)
lastSubphone = [x - 1 for x in lastSubphone]

V = [{}]
path = {}
print 'Initialize Viterbi Trellis'
for q in states:
	i = q[0]
	digit = q[1]
	phoneme = q[2]
	subphone = q[3]
	if i in firstSubphone:
		V[0][i] = B[0][phoneme][subphone]
	else:
		V[0][i] = float("-inf")
	path[i] = [i]

print 'Run Viterbi for t > 0'
for t in range(1,T):
	V.append({})
	newpath = {}
	for q in states:
		i = q[0]
		digit = q[1]
		phoneme = q[2]
		subphone = q[3]
		cases = []
		stateObsL = B[t][phoneme][subphone]
		# Stay in the same state
		cases.append((V[t-1][i] + stateObsL, i))
		
		if i in firstSubphone:
			# From last state of every digit (word transition)
			temp = max((V[t-1][ls] + stateObsL - 50, ls) for ls in lastSubphone)
			cases.append(temp)
		else:
			# From the previous state in the same digit
			cases.append((V[t-1][i-1] + stateObsL, i-1))
		
		(maxProb, maxState) = max(cases)
		V[t][i] = maxProb
		newpath[i] = path[maxState]+[i]

	# Don't need old paths
	path = newpath
	# print newpath

(finalProb, finalState) = max((V[t][i],i) for i in lastSubphone)
finalPath = [path[finalState][0]]
for i in range(1, len(path[finalState])):
	if path[finalState][i] != finalPath[-1]:
		finalPath = finalPath + [path[finalState][i]]

output = []
for i in finalPath:
	if i in firstSubphone:
		output.append(digitOfState[i])
print finalPath
print finalProb
print output

# # Print out trellis
# s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
# for y in V[0]:
#     s += "%.5s: " % y
#     s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
#     s += "\n"
# print(s)


