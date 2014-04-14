import re
from collections import OrderedDict

lexiconFileName = 'lexicon.txt'
phonemesFileName = 'phonemes.txt'
emissionsFileName = 'output.txt'
# emissionsFileName = 'fake.output'
resultsFileName = 'result.txt'

# Read in lexicon
Lexicon = OrderedDict()
with open(lexiconFileName) as f:
	for line in f:
		split = re.split(r'\s+', line)
		Lexicon[split[0]] = split[1:-2]

# Read in Phonemes
Phonemes = []
with open(phonemesFileName) as f:
	for line in f:
		Phonemes.append(line.strip())

# Read in State Observation Likelihoods (emission probabilities)
B = {}
with open(emissionsFileName) as f:
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

# Idxes of the last subphone of a digit
lastSubphone = firstSubphone[1:]
lastSubphone.append(i)
lastSubphone = [x - 1 for x in lastSubphone] 

# Initialize Viterbi Trellis 
V = [{}]
path = {}
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

# Run Viterbi for t > 0 and fill in trellis
for t in range(1,T):
	# Declare new column in trellis
	V.append({})
	newpath = {}

	for q in states:
		# Fetch state information
		i = q[0]
		digit = q[1]
		phoneme = q[2]
		subphone = q[3]
		cases = []
		stateObsL = B[t][phoneme][subphone]

		# Case 1: Stay in the same state
		cases.append((V[t-1][i] + stateObsL, i))

		# Case 2: Transition from last state of every digit (word transition)		
		if i in firstSubphone:
			temp = max((V[t-1][ls] + stateObsL - 50, ls) for ls in lastSubphone)
			cases.append(temp)
		
		# Case 3: Transition from the previous state in the same digit
		else:
			cases.append((V[t-1][i-1] + stateObsL, i-1))
		
		# Compute max from the three cases and store path
		(maxProb, maxState) = max(cases)
		V[t][i] = maxProb
		newpath[i] = path[maxState]+[i]
	path = newpath

# Track back path, enforce terminating on last subphone
(finalProb, finalState) = max((V[t][i],i) for i in lastSubphone)
finalPath = [path[finalState][0]]
for i in range(1, len(path[finalState])):
	if path[finalState][i] != finalPath[-1]:
		finalPath = finalPath + [path[finalState][i]]

# Fetch the digits corresponding to the path
output = []
for i in finalPath:
	if i in firstSubphone:
		output.append(digitOfState[i])

# Print results and write to txt file
#print finalPath
f = open(resultsFileName, 'w')
for digit in output:
	f.write(digit + '\n')
	print digit
f.write('\n')
print ''
f.write('log probability: ' + str(finalProb) + '\n')
print 'log probability: ' + str(finalProb)



