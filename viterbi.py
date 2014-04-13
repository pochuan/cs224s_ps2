import re
print "Viterbi!"

# Read in files
lexicon = {}
with open('lexicon.txt') as f:
	for line in f:
		split = line.split(' ', 1)
		lexicon[split[0]] = split[1].strip()

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

print B[1]


