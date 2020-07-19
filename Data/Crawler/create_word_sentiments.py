import mysql_queryhandler

def process_index_file(filename='../Database/index.txt'):
	with open(filename) as fp:
		line = fp.readline()
		#cnt = 1
		nouns = {}
		while line:
			#print("Line {}: {}".format(cnt, line.strip()))
			line = fp.readline()
			arr = line.strip().split(' ')
			nouns[arr[0]] = arr[-1]
			#cnt += 1	
		return nouns

def process_synonymset_scores(filename='../Database/SentiWordNet_3.0.0.txt'):
	with open(filename) as fp:
		line = fp.readline()
		scores = {}
		while line:			
			line = fp.readline()
			arr = line.strip().split('\t')
			try:
				scores[arr[1]] = 1.0 - (float(arr[2]) + float(arr[3]))
			except Exception:
				print("OOR")
		return scores

if __name__ == "__main__":
	nouns = process_index_file()
	synset_scores = process_synonymset_scores()
	word_scores = []

	# Process word scores
	for x in nouns:
		try:
			word_scores.append((x, synset_scores[nouns[x]]))
		except Exception:
			print("OOR")

	# Write words and scores to db
	handler = mysql_queryhandler.queryhandler()
	handler.set_word_sentiments(word_scores)

	del handler